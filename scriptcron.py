from enum import Enum
from aiohttp import ClientSession
import asyncio
import logging
import random
import argparse

def generate_random_subject():
    subjects = [
        "Technology", "Science", "Health", "Education", "Business", "Entertainment", 
        "Sports", "Politics", "Environment", "History", "Travel", "Food", "Music", 
        "Books", "Movies", "Fashion", "Hobbies", "Relationships", "Fitness", "Culture",
        "Games", "Cartoons", "Toys", "Friends", "School", "Holidays"
    ]
    
    return random.choice(subjects)
    

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

gpt_servers = ["http://localhost:8080","http://localhost:8081","http://localhost:8082","http://localhost:8083","http://localhost:8084","http://localhost:8085","http://localhost:8086"]
gen_servers = ["http://localhost:8000","http://localhost:8000","http://localhost:8000","http://localhost:8000","http://localhost:8000","http://localhost:8000","http://localhost:8000"]

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
    },
        {
        "server_url": gpt_servers[5],
        "topic": "school",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Let's have a simple conversation using limited vocabulary. Please keep your responses brief, and I'll do the same. Avoid repeating 'Absolutely!'You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    },
            {
        "server_url": gpt_servers[6],
        "topic": "life",
        "initial_message": "Respond to the following statement without using the word 'Exactly!', or 'Absolutely!' or 'Definitely!' because it doesn't sound human at the beginning:Lets pretend to have a basic conversation, also don't say that you are an AI, and dont repeat yourself, please respond with short paragraphs and limit to a basic vocabulary and grammar, I will do the same. I repeat respond with short paragraph, Avoid repeating 'Absolutely!'You can also try to change topic if you are starting to just agree with the statement I don't want a loop of conversation just saying 'I agree!' or any statement like that'"
    },
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
            chat_setting["topic"] = generate_random_subject()
        
        except Exception as e:
            logging.error(f"Error in continuous fetch loop for server {server_index + 1}: {e}")
        
        # Optional: Add a small delay between iterations for this specific server
        await asyncio.sleep(0.1)
        
# Create the parser
parser = argparse.ArgumentParser(description="Process some arguments.")

# Add arguments
parser.add_argument('-n', type=int, default=10, help="An integer number (default is 10)")

# Parse the arguments
args = parser.parse_args()

# Access the value of 'n'
n_value = args.n
async def main():
    tasks = [continuous_fetch(i) for i in range(n_value)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
