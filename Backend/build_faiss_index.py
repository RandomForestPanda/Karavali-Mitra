import json
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Load dataset, you can choose to use your own dataset (by importing it here as a json file and building the knowledge base) or use the existing knowledge base
with open('south_canara_tourism_dataset.json', 'r') as f:
    dataset = json.load(f)

texts = [item['answer'] for item in dataset]

# Embed texts
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and texts
faiss.write_index(index, 'knowledge_base_semantic.index')
with open('text_mapping.pkl', 'wb') as f:
    pickle.dump(texts, f)

print("FAISS index built!")
