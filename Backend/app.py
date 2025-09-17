from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import redis
import json
import traceback
from huggingface_hub import InferenceClient
import requests  # Added for Tavily API

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

try:
    redis_client.ping()
    print("Connected to Redis!")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")

# Load FAISS index and text mapping
faiss_index = faiss.read_index("knowledge_base_semantic.index")
with open("text_mapping.pkl", "rb") as f:
    texts = pickle.load(f)

# Initialize FastAPI app
app = FastAPI()

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Hugging Face API Key and Client
HF_API_KEY = 'Your Hf key Here'  # Replace with your actual HF API key
client = InferenceClient(api_key=HF_API_KEY)

# Tavily API Key (Replace with your own key)
TAVILY_API_KEY = "Your Tvaily Key Here"


# Define the prompt template
def generate_prompt(query, documents):
    return f"""You are a tour guide. The user is a tourist. Based on the situation provided, generate detailed one page travel plans, itineraries, and tourist spots to guide the user in exploring the places.
Answer in a clear, helpful, and actionable format:

**Tourist's Query:** {query}

**Relevant Information:**
{documents}

**Travel Recommendations:**
"""


# Function to query Hugging Face Inference API using Mistral
def generate_answer_with_mistral(query, documents):
    prompt = generate_prompt(query, documents)
    messages = [{"role": "user", "content": prompt}]

    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=messages,
            max_tokens=500
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Hugging Face API: {str(e)}")


# Function to query Tavily API when FAISS retrieval fails
def search_tavily(query):
    cache_key = f"tavily:cache:{query}"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        print("Returning cached Tavily response!")
        return json.loads(cached_response)

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "num_results": 3},
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}"}
        )

        if response.status_code == 200:
            search_results = response.json()
            print("Tavily API response:", json.dumps(search_results, indent=4))  # Debugging step

            if "results" not in search_results:
                raise HTTPException(status_code=500, detail="Unexpected Tavily API response format")

            # Extract content properly (check actual key names)
            documents = "\n".join([
                result.get("snippet", result.get("content", "No relevant information available"))
                for result in search_results["results"]
            ])

            # Cache the result
            redis_client.setex(cache_key, 3600, json.dumps(documents))  # Cache for 1 hour
            return documents
        else:
            raise HTTPException(status_code=500, detail=f"Tavily API error: {response.text}")
    except Exception as e:
        print(f"Error fetching from Tavily: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error retrieving data from Tavily API")


# Define Retriever
class FAISSRetriever:
    def __init__(self, faiss_index, texts, threshold=1.0):
        self.faiss_index = faiss_index
        self.texts = texts
        self.threshold = threshold  # Define similarity threshold

    def invoke(self, query, n_results=3):
        query_embedding = embedding_model.encode([query])
        distances, indices = self.faiss_index.search(query_embedding, n_results)

        # Filter results based on distance threshold
        documents = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts) and distances[0][i] < self.threshold:
                documents.append(self.texts[idx])

        return documents  # Return only relevant docs


retriever = FAISSRetriever(faiss_index, texts)


# Define RAGApplication with Tavily fallback
class RAGApplication:
    def __init__(self, retriever, faiss_weight=0.7, tavily_weight=0.3):
        self.retriever = retriever
        self.faiss_weight = faiss_weight  # Weight for FAISS results
        self.tavily_weight = tavily_weight  # Weight for Tavily results

    def run(self, query, user_id):
        try:
            cache_key = f"user:{user_id}:cache:{query}"
            cached_response = redis_client.get(cache_key)
            if cached_response:
                print("Returning cached response!")
                return json.loads(cached_response)

            # Step 1: Retrieve from FAISS
            faiss_docs = self.retriever.invoke(query)
            faiss_texts = "\n".join(faiss_docs)

            # Step 2: Retrieve from Tavily
            tavily_texts = search_tavily(query)

            # Step 3: Merge FAISS and Tavily results with weighted importance
            merged_docs = self._merge_sources(faiss_texts, tavily_texts)

            # Step 4: Generate the final response using Mistral
            answer = generate_answer_with_mistral(query, merged_docs)

            # Cache response
            redis_client.setex(cache_key, 3600, json.dumps(answer))

            return answer
        except Exception as e:
            print(f"Error in RAG application: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Error processing query.")

    def _merge_sources(self, faiss_text, tavily_text):
        """Hybrid merging function with weighted priority."""
        faiss_weighted = self.faiss_weight * len(faiss_text.split())
        tavily_weighted = self.tavily_weight * len(tavily_text.split())

        # Balance content by relative weighting
        total_weight = faiss_weighted + tavily_weighted
        faiss_ratio = faiss_weighted / total_weight if total_weight > 0 else 0.5
        tavily_ratio = tavily_weighted / total_weight if total_weight > 0 else 0.5

        faiss_limit = int(faiss_ratio * 500)  # Adjust based on max tokens
        tavily_limit = int(tavily_ratio * 500)

        return f"FAISS Results:\n{faiss_text[:faiss_limit]}\n\nTavily Results:\n{tavily_text[:tavily_limit]}"

# Allow CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

rag_application = RAGApplication(retriever)
print("RAG application created")


# Define request model
class QueryRequest(BaseModel):
    user_id: str
    query: str


# Search endpoint (Accept JSON instead of Form data)
@app.post("/search")
async def receive_search(request: QueryRequest):
    try:
        answer = rag_application.run(request.query, request.user_id)
        print(answer)
        return {"response": answer}
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")


# Location endpoint (Optional)
@app.post("/location")
async def receive_location(latitude: float, longitude: float):
    print(f"Received location: {latitude}, {longitude}")
    return {"message": "Location received", "latitude": latitude, "longitude": longitude}
