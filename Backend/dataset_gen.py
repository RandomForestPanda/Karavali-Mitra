import json
import random
import pandas as pd
from faker import Faker

# Initialize Faker for generating varied human-like text
fake = Faker()

# Define tourist information for Udupi, Mangalore, and South Canara region
tourism_data = {
    "Udupi": {
        "famous_places": [
            {"name": "Sri Krishna Temple",
             "description": "An iconic 13th-century temple dedicated to Lord Krishna, known for its unique method of worship where devotees can only view the deity through a window with nine holes called Navagraha Kitiki."},
            {"name": "Malpe Beach",
             "description": "A pristine beach located 6 km from Udupi, popular for water sports, scenic beauty, and the nearby St. Mary's Island which has unique hexagonal basaltic rock formations."},
            {"name": "St. Mary's Island",
             "description": "A small island off the coast of Malpe with unique geological formations of columnar basaltic lava, one of the few places in the world to observe this phenomenon."},
            {"name": "Kaup Beach and Lighthouse",
             "description": "A serene beach with a 100-year-old lighthouse offering panoramic views of the Arabian Sea. Perfect spot for sunset watching."},
            {"name": "Manipal",
             "description": "An educational hub with Manipal University, featuring End Point Park, Venugopal Temple, and the Museum of Anatomy & Pathology."},
            {"name": "Kodi Beach",
             "description": "A pristine beach with golden sands, ideal for watching sunsets and enjoying the calm sea."}
        ],
        "cuisine": [
            {"name": "Goli Baje",
             "description": "Popular Udupi snack made from maida flour, also known as Mangalore bajji, these are deep-fried fluffy fritters."},
            {"name": "Neer Dosa",
             "description": "A thin, watery rice crepe that is a staple in Udupi cuisine, typically served with coconut chutney or sambar."},
            {"name": "Kadubu",
             "description": "Steamed rice dumplings often filled with a coconut and jaggery mixture."},
            {"name": "Udupi Sambar",
             "description": "A flavorful lentil-based vegetable stew with a unique taste due to the addition of local spices."},
            {"name": "Mangalore Buns",
             "description": "Sweet, fluffy, deep-fried bread made from mashed bananas and flour, typically eaten for breakfast."}
        ],
        "festivals": [
            {"name": "Krishna Janmashtami",
             "description": "Celebrated with great fervor at the Sri Krishna Temple, featuring the Vittal Pindi (Mosaru Kudike) ceremony where pots of curd are broken."},
            {"name": "Paryaya Festival",
             "description": "A biennial festival marking the transfer of worship rights among the eight Udupi Mutts, featuring elaborate ceremonies and processions."}
        ],
        "accommodation": [
            {"name": "Paradise Isle Beach Resort", "type": "Luxury", "location": "Malpe Beach"},
            {"name": "Country Inn & Suites By Radisson", "type": "Luxury", "location": "Manipal"},
            {"name": "The Ocean Pearl", "type": "Mid-range", "location": "Udupi City Center"},
            {"name": "Treebo Trip Kampl", "type": "Budget", "location": "Near Krishna Temple"}
        ],
        "transportation": [
            {"mode": "Bus",
             "details": "KSRTC buses connect Udupi to major cities like Bangalore, Mangalore, and Mysore."},
            {"mode": "Train",
             "details": "Udupi has its own railway station with connections to major cities across India."},
            {"mode": "Nearest Airport", "details": "Mangalore International Airport is about 60 km away."},
            {"mode": "Local Transport",
             "details": "Auto-rickshaws and taxis are readily available for local transportation."}
        ],
        "best_time_to_visit": "October to March when the weather is pleasant and ideal for beach activities."
    },
    "Mangalore": {
        "famous_places": [
            {"name": "Mangaladevi Temple",
             "description": "Ancient temple dedicated to Goddess Mangaladevi, after whom the city is named."},
            {"name": "Panambur Beach",
             "description": "One of the cleanest beaches in Karnataka known for its mesmerizing sunsets and annual kite festival."},
            {"name": "Kadri Manjunath Temple",
             "description": "An ancient temple dating back to 1068 AD, dedicated to Lord Manjunatha (Shiva)."},
            {"name": "St. Aloysius Chapel",
             "description": "Known for its breathtaking paintings and frescoes by Italian Jesuit Antonio Moscheni."},
            {"name": "Tannirbhavi Beach",
             "description": "A serene beach with golden sands, offering boat rides and water sports."},
            {"name": "Pilikula Nisargadhama",
             "description": "A multi-purpose tourist attraction with a biological park, golf course, lake, and science center."}
        ],
        "cuisine": [
            {"name": "Kori Rotti",
             "description": "A coastal Karnataka delicacy consisting of crisp dry rice wafers and chicken curry."},
            {"name": "Neer Dosa", "description": "Thin rice crepes served with coconut chutney or chicken/fish curry."},
            {"name": "Kane Fry",
             "description": "Ladyfish marinated in spices and fried to crispy perfection, a local favorite."},
            {"name": "Chicken Ghee Roast",
             "description": "Spicy chicken dish cooked in ghee with a special blend of spices, originating from Kundapur."},
            {"name": "Mangalore Buns",
             "description": "Sweet, puffed, deep-fried bread made from ripe bananas and flour."}
        ],
        "festivals": [
            {"name": "Mangalore Dasara",
             "description": "Celebrated at the Kudroli Gokarnanatheshwara Temple with processions and cultural events."},
            {"name": "Kambala",
             "description": "Traditional buffalo race held in paddy fields, unique to coastal Karnataka."}
        ],
        "accommodation": [
            {"name": "The Gateway Hotel Old Port Road", "type": "Luxury", "location": "Old Port Road"},
            {"name": "The Ocean Pearl", "type": "Mid-range", "location": "Navabharath Circle"},
            {"name": "Hotel Deepa Comforts", "type": "Mid-range", "location": "Kodialbail"},
            {"name": "Hotel Kumar's International", "type": "Budget", "location": "Near State Bank"}
        ],
        "transportation": [
            {"mode": "Airport",
             "details": "Mangalore International Airport with flights to major Indian cities and Gulf countries."},
            {"mode": "Train",
             "details": "Mangalore Central and Mangalore Junction are well-connected to major cities."},
            {"mode": "Bus",
             "details": "KSRTC and private buses connect Mangalore to Karnataka, Kerala, and other neighboring states."},
            {"mode": "Local Transport",
             "details": "City buses, auto-rickshaws, and taxis are available for local travel."}
        ],
        "best_time_to_visit": "October to February when the weather is pleasant and less humid."
    },
    "South Canara": {
        "famous_places": [
            {"name": "Murudeshwar",
             "description": "Home to the second-tallest Shiva statue in the world and a coastal temple with a 20-story gopuram."},
            {"name": "Gokarna",
             "description": "A temple town with pristine beaches like Om Beach, known for its spiritual significance and laid-back atmosphere."},
            {"name": "Karwar",
             "description": "A coastal town with beautiful beaches, Sadashivgad Fort, and the Naval Maritime Museum."},
            {"name": "Kollur Mookambika Temple",
             "description": "Ancient temple dedicated to Goddess Mookambika, nestled in the Western Ghats."},
            {"name": "Netrani Island",
             "description": "Also known as Pigeon Island, it's a popular spot for scuba diving and snorkeling."},
            {"name": "Yana Rocks",
             "description": "Unique rock formations in the dense forests of the Western Ghats, standing at heights of 390 feet and 300 feet."}
        ],
        "cuisine": [
            {"name": "Fish Curry Rice",
             "description": "Simple yet flavorful fish curry served with boiled rice, a staple along the Karavali coast."},
            {"name": "Pathrode",
             "description": "Steamed colocasia leaf rolls stuffed with rice paste, spices, and jaggery."},
            {"name": "Mangalore Biryani",
             "description": "A unique coastal variant of biryani with distinct flavors from the region."},
            {"name": "Goli Baje", "description": "Deep-fried fluffy balls made from maida flour, a popular snack."},
            {"name": "Anjal Fry", "description": "King fish marinated in local spices and fried, a coastal delicacy."}
        ],
        "festivals": [
            {"name": "Bhuta Kola",
             "description": "Traditional ritual dance that involves spirit worship, performed to appease local deities."},
            {"name": "Aati Kalenja",
             "description": "A harvest festival celebrated in July-August with traditional games and rituals."}
        ],
        "accommodation": [
            {"name": "RNS Residency", "type": "Luxury", "location": "Murudeshwar"},
            {"name": "Namaste Cafe", "type": "Mid-range", "location": "Om Beach, Gokarna"},
            {"name": "Sai Vishram Beach Resort", "type": "Luxury", "location": "Byndoor"},
            {"name": "Om Beach Resort", "type": "Mid-range", "location": "Gokarna"}
        ],
        "transportation": [
            {"mode": "Train", "details": "Konkan Railway runs through South Canara connecting major towns."},
            {"mode": "Bus", "details": "KSRTC and private buses connect various parts of South Canara."},
            {"mode": "Nearest Airport", "details": "Mangalore International Airport serves the South Canara region."},
            {"mode": "Local Transport",
             "details": "Auto-rickshaws, taxis, and local buses are available for transportation within towns."}
        ],
        "best_time_to_visit": "October to March when the weather is pleasant and post-monsoon greenery is at its peak."
    }
}

# Question templates for generating varied questions
general_templates = [
    "What are the top tourist attractions in {place}?",
    "Tell me about {place} and its famous landmarks.",
    "What should I visit if I'm in {place} for a day?",
    "What are the must-see places in {place}?",
    "I'm planning a trip to {place}, what places should I visit?",
    "Give me information about tourism in {place}.",
    "What makes {place} a good tourist destination?",
    "Is {place} worth visiting? What can I see there?",
    "How can I spend 2 days in {place}?",
    "What are some hidden gems in {place} that tourists often miss?"
]

specific_place_templates = [
    "Tell me about {specific_place} in {place}.",
    "What is special about {specific_place}?",
    "How do I get to {specific_place} from {place} center?",
    "Is {specific_place} worth visiting?",
    "What activities can I do at {specific_place}?",
    "What's the history behind {specific_place}?",
    "How much time should I spend at {specific_place}?",
    "What's the best time to visit {specific_place}?",
    "Are there any entrance fees for {specific_place}?",
    "Can you describe what I'll see at {specific_place}?"
]

food_templates = [
    "What are the must-try foods in {place}?",
    "Tell me about {food} from {place}.",
    "Where can I get the best {food} in {place}?",
    "What is {food} and why is it famous in {place}?",
    "What are the traditional dishes of {place}?",
    "Which restaurants in {place} serve authentic local cuisine?",
    "Is {food} vegetarian or non-vegetarian?",
    "What ingredients are used in {food}?",
    "Are there any food festivals in {place}?",
    "What's the street food scene like in {place}?"
]

accommodation_templates = [
    "Where should I stay in {place}?",
    "What are the best hotels in {place}?",
    "Are there budget accommodations in {place}?",
    "Tell me about {hotel} in {place}.",
    "What's the average cost of hotels in {place}?",
    "Are there any beachfront resorts in {place}?",
    "Is it better to stay in the city center or outskirts of {place}?",
    "Do I need to book accommodation in advance for {place}?",
    "Are there homestays available in {place}?",
    "What amenities can I expect in hotels in {place}?"
]

transportation_templates = [
    "How do I reach {place} from Bangalore?",
    "What's the best way to get around in {place}?",
    "Is public transportation reliable in {place}?",
    "How far is {place} from Mangalore Airport?",
    "Are taxis readily available in {place}?",
    "Can I rent a vehicle in {place}?",
    "How is the road connectivity to {place}?",
    "Is there a direct train from Mumbai to {place}?",
    "What's the nearest airport to {place}?",
    "How much would a taxi cost from {place1} to {place2}?"
]

festival_templates = [
    "What festivals are celebrated in {place}?",
    "When is {festival} celebrated in {place}?",
    "Tell me about {festival} in {place}.",
    "What are the cultural events in {place} throughout the year?",
    "Is there a good time to visit {place} for cultural experiences?",
    "How do locals celebrate {festival}?",
    "Are there any unique rituals during {festival}?",
    "Can tourists participate in {festival} celebrations?",
    "What should I expect during {festival} in {place}?",
    "Are there any restrictions during festivals in {place}?"
]

practical_templates = [
    "What's the best time to visit {place}?",
    "How many days should I spend in {place}?",
    "Is {place} suitable for family trips?",
    "What should I pack for a trip to {place}?",
    "Is {place} expensive for tourists?",
    "Are there any local customs I should be aware of in {place}?",
    "Is it safe to travel alone in {place}?",
    "What language is spoken in {place}?",
    "Do I need permits to visit certain areas in {place}?",
    "What's the weather like in {place} during {month}?"
]

comparative_templates = [
    "Which is better to visit, {place1} or {place2}?",
    "How is {place1} different from {place2}?",
    "Should I visit {place1} or {place2} if I only have time for one?",
    "Compare the beaches of {place1} and {place2}.",
    "Is {place1} more expensive than {place2}?",
    "Which has better food, {place1} or {place2}?",
    "Is it easier to travel to {place1} or {place2}?",
    "What are the unique aspects of {place1} compared to {place2}?",
    "Which has better accommodation options, {place1} or {place2}?",
    "If I have 3 days, should I spend more time in {place1} or {place2}?"
]

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def generate_answer(question, region_data):
    """Generate a detailed answer based on the question and available tourism data"""

    # This is a simplified answer generator - a real implementation would use NLP to understand
    # the question and generate appropriate answers from the data

    place = None
    for region in tourism_data:
        if region.lower() in question.lower():
            place = region
            break

    if not place:
        place = list(tourism_data.keys())[random.randint(0, len(tourism_data.keys()) - 1)]

    data = tourism_data[place]

    # Check question type and generate appropriate answer
    if "famous" in question.lower() or "attractions" in question.lower() or "visit" in question.lower():
        places = data["famous_places"]
        answer = f"Here are some famous places to visit in {place}:\n\n"
        for i, p in enumerate(places, 1):
            answer += f"{i}. {p['name']}: {p['description']}\n\n"

    elif "food" in question.lower() or "cuisine" in question.lower() or "eat" in question.lower():
        foods = data["cuisine"]
        answer = f"The cuisine of {place} is delicious and diverse. Here are some must-try dishes:\n\n"
        for i, f in enumerate(foods, 1):
            answer += f"{i}. {f['name']}: {f['description']}\n\n"

    elif "stay" in question.lower() or "hotel" in question.lower() or "accommodation" in question.lower():
        hotels = data["accommodation"]
        answer = f"Here are some accommodation options in {place}:\n\n"
        for i, h in enumerate(hotels, 1):
            answer += f"{i}. {h['name']} ({h['type']}): Located at {h['location']}\n\n"

    elif "transport" in question.lower() or "reach" in question.lower() or "get to" in question.lower():
        transports = data["transportation"]
        answer = f"Here's how you can reach and get around in {place}:\n\n"
        for i, t in enumerate(transports, 1):
            answer += f"{i}. {t['mode']}: {t['details']}\n\n"

    elif "festival" in question.lower() or "celebration" in question.lower() or "cultural" in question.lower():
        festivals = data["festivals"]
        answer = f"Here are important festivals celebrated in {place}:\n\n"
        for i, f in enumerate(festivals, 1):
            answer += f"{i}. {f['name']}: {f['description']}\n\n"

    elif "time" in question.lower() or "when" in question.lower() or "season" in question.lower():
        answer = f"The best time to visit {place} is {data['best_time_to_visit']}"

    else:
        # Generate a general overview
        answer = f"{place} is a beautiful destination in the South Canara region. "
        answer += f"It's known for attractions like {', '.join([p['name'] for p in data['famous_places'][:3]])}. "
        answer += f"The local cuisine features delicacies such as {', '.join([f['name'] for f in data['cuisine'][:3]])}. "
        answer += f"The best time to visit is {data['best_time_to_visit']}"

    return answer


def generate_dataset(num_examples=500):
    """Generate a dataset of questions and answers about South Canara tourism"""
    dataset = []

    all_templates = general_templates + specific_place_templates + food_templates + \
                    accommodation_templates + transportation_templates + \
                    festival_templates + practical_templates + comparative_templates

    for _ in range(num_examples):
        template_list = random.choice([
            general_templates,
            specific_place_templates,
            food_templates,
            accommodation_templates,
            transportation_templates,
            festival_templates,
            practical_templates,
            comparative_templates
        ])

        template = random.choice(template_list)

        # Select random place(s)
        place = random.choice(list(tourism_data.keys()))
        place2 = random.choice([p for p in tourism_data.keys() if p != place])

        # For specific place templates
        if "{specific_place}" in template:
            specific_place = random.choice(tourism_data[place]["famous_places"])["name"]
            question = template.format(specific_place=specific_place, place=place)
        # For food templates
        elif "{food}" in template:
            food = random.choice(tourism_data[place]["cuisine"])["name"]
            question = template.format(food=food, place=place)
        # For festival templates
        elif "{festival}" in template:
            if tourism_data[place]["festivals"]:
                festival = random.choice(tourism_data[place]["festivals"])["name"]
                question = template.format(festival=festival, place=place)
            else:
                # Fallback if no festivals data
                question = f"What cultural events happen in {place}?"
        # For hotel templates
        elif "{hotel}" in template:
            hotel = random.choice(tourism_data[place]["accommodation"])["name"]
            question = template.format(hotel=hotel, place=place)
        # For month templates
        elif "{month}" in template:
            month = random.choice(months)
            question = template.format(place=place, month=month)
        # For comparative templates
        elif "{place1}" in template and "{place2}" in template:
            question = template.format(place1=place, place2=place2)
        # For regular templates
        else:
            question = template.format(place=place)

        # Generate an answer
        answer = generate_answer(question, tourism_data)

        # Sometimes create a conversation history
        if random.random() < 0.3 and len(dataset) > 0:
            # Select 1-3 previous exchanges to form a conversation
            history_size = random.randint(1, min(3, len(dataset)))
            history_indices = random.sample(range(len(dataset)), history_size)
            history = [dataset[i] for i in history_indices]

            # Sort by history indices to maintain chronological order
            history.sort(key=lambda x: history_indices[dataset.index(x)])

            conversation_history = []
            for h in history:
                conversation_history.append(f"User: {h['question']}")
                conversation_history.append(f"Assistant: {h['answer']}")

            dataset.append({
                "question": question,
                "answer": answer,
                "conversation_history": conversation_history
            })
        else:
            dataset.append({
                "question": question,
                "answer": answer,
                "conversation_history": []
            })

    return dataset


# Generate the dataset
tourism_dataset = generate_dataset(500)

# Save to different formats
# JSON format for general use
with open("south_canara_tourism_dataset.json", "w", encoding="utf-8") as f:
    json.dump(tourism_dataset, f, indent=2, ensure_ascii=False)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(tourism_dataset)
df.to_csv("south_canara_tourism_dataset.csv", index=False)

# Create JSONL format for fine-tuning (formatted specifically for model training)
with open("south_canara_tourism_finetune.jsonl", "w", encoding="utf-8") as f:
    for item in tourism_dataset:
        history_text = "\n".join(item["conversation_history"]) if item["conversation_history"] else ""

        # Format for instruction fine-tuning
        finetune_item = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Previous conversation:\n{history_text}\n\nUser question: {item['question']}"
                },
                {
                    "role": "assistant",
                    "content": item["answer"]
                }
            ]
        }
        f.write(json.dumps(finetune_item, ensure_ascii=False) + "\n")

print(f"Generated {len(tourism_dataset)} question-answer pairs")
print(
    "Files saved: south_canara_tourism_dataset.json, south_canara_tourism_dataset.csv, south_canara_tourism_finetune.jsonl")