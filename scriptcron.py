from enum import Enum
import json
from aiohttp import ClientSession
import asyncio
import logging
import random

def generate_random_topics_and_conversations(num_items):
    subjects = [
        "Technology", "Science", "Health", "Education", "Business", "Entertainment", 
        "Sports", "Politics", "Environment", "History", "Travel", "Food", "Music", 
        "Books", "Movies", "Fashion", "Hobbies", "Relationships", "Fitness", "Culture",
        "Games", "Cartoons", "Toys", "Friends", "School", "Holidays"
    ]
    adjectives = [
        "Advanced", "Future", "Modern", "Innovative", "Global", "Revolutionary", 
        "Sustainable", "Digital", "Cutting-edge", "Historic", "Popular", "New", 
        "Classic", "Delicious", "Exciting", "Relaxing", "Challenging", "Famous", 
        "Unique", "Traditional", "Fun", "Cool", "Interesting", "Amazing", "Awesome"
    ]
    nouns = [
        "Trends", "Challenges", "Opportunities", "Developments", "Issues", "Impacts", 
        "Advances", "Techniques", "Strategies", "Breakthroughs", "Destinations", 
        "Recipes", "Genres", "Authors", "Directors", "Styles", "Activities", 
        "Experiences", "Routines", "Practices", "Stories", "Characters", "Episodes", 
        "Toys", "Projects"
    ]
    starters = [
        "What do you think about", "How do you feel about", "What's your opinion on", 
        "Have you heard about", "Can you tell me about", "What are your thoughts on", 
        "Do you like", "Have you tried", "What's your favorite", "How do you enjoy",
        "Do you know", "What's the best", "Tell me about", "Do you have a favorite", 
        "What do you enjoy", "Can you explain", "How did you get into", "What makes you excited about"
    ]
    
    topics_and_conversations = []
    for _ in range(num_items):
        subject = random.choice(subjects)
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        topic = f"{adjective} {subject} {noun}"
        
        starter = random.choice(starters)
        conversation = f"{starter} {topic}?"
        
        topics_and_conversations.append(conversation)
    
    return topics_and_conversations

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

async def fetch_url(url, method: HTTPMethod = HTTPMethod.GET, *args, **kwargs):
    async with ClientSession() as session:
        method_action = {
            HTTPMethod.GET: session.get,
            HTTPMethod.POST: session.post,
            HTTPMethod.DELETE: session.delete,
            HTTPMethod.PUT: session.put,
        }.get(method, session.get)  # Default to GET if method is not found

        async with method_action(url, *args, **kwargs) as response:
            return await response.json()

gpt_servers = ["http://localhost:8080","http://localhost:8081","http://localhost:8082","http://localhost:8083","http://localhost:8084"]
gen_servers = ["http://localhost:8000","http://localhost:8000","http://localhost:8000","http://localhost:8000","http://localhost:8000"]

chatSettings = [
    {
        "server_url": gpt_servers[0],
        "topic": "life",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Lets pretend to have a basic conversation, also don't say that you are an AI, and dont repeat yourself, please respond with short paragraphs and limit to a basic vocabulary and grammar, I will do the same. I repeat respond with short paragraph, Avoid repeating 'Absolutely!'You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    },
    {
        "server_url": gpt_servers[1],
        "topic": "work",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Lets pretend to have a basic conversation with minimal vocabulary, I also want you do limit your response to short paragraphs, I will do the same. I repeat respond with short paragraph, Avoid repeating 'Absolutely!'You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    },
    {
        "server_url": gpt_servers[2],
        "topic": "travel",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Let's have a simple conversation using limited vocabulary. Please keep your responses brief, and I'll do the same. Avoid repeating 'Absolutely!'You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    },
    {
        "server_url": gpt_servers[3],
        "topic": "school",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Let's have a simple conversation using limited vocabulary. Please keep your responses brief, and I'll do the same. Avoid repeating 'Absolutely!'You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    },
    {
        "server_url": gpt_servers[4],
        "topic": "food",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Let's have a simple conversation using limited vocabulary. Please keep your responses brief, and I'll do the same. Avoid repeating 'Absolutely!. You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    }
]

async def fetch_with_retry(url, method, json_data, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            result = await fetch_url(url, method, json=json_data)
            if result is not None:
                return result
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed with error: {e}")
        if attempt < max_retries - 1:
            await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
    return None

async def continuous_fetch(server_index):
    gen_server = gen_servers[server_index]
    chat_setting = chatSettings[server_index]
    
    while True:
        try:
            url = f"{gen_server}/api/generate_conversation"
            result = await fetch_with_retry(url, HTTPMethod.POST, chat_setting)
            
            if result is not None:
                print(f"Successful fetch for server {server_index + 1}")
            else:
                print(f"Fetch failed for server {server_index + 1}")
            
            # Update topic regardless of fetch success
            chat_setting["topic"] = generate_random_topics_and_conversations(1)[0].split()[-1]
        
        except Exception as e:
            logging.error(f"Error in continuous fetch loop for server {server_index + 1}: {e}")
        
        # Optional: Add a small delay between iterations for this specific server
        await asyncio.sleep(0.1)

async def main():
    tasks = [continuous_fetch(i) for i in range(4)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
