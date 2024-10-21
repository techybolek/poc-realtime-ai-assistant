import json
from openai import OpenAI
import asyncio
import websockets

def get_system_prompt():
    part1 = """
    You are given a list of URLs related to disaster recovery, government programs, financial analyses,
    and other related topics. Based on the user’s input or keywords, determine the URL and navigate to it.
    Choose the most appropriate URL by matching the user's input to one of the descriptions. Here is the list of URLs:
"""
    part2 = json.dumps(knowledge)
    return part1 + "\n###\n" + part2 + "\n###\n"

with open("urls.json", "r") as file:
    knowledge = json.load(file)

client = OpenAI()


functions = [
    {
                "type": "function",
                "name": "navigate_to_url",
                "description": "Navigate to the specified URL",
                "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to",
                    },
                },
                "required": ["url"],
            },
    }
]


async def init_ws_server():
    print("Initializing WebSocket server...")

async def transmit_url_to_client(url: str):
    print(f"Transmitting URL to client: {url}")

async def call_openai(query: str) -> str:
    # Convert the synchronous OpenAI call to asynchronous
    loop = asyncio.get_event_loop()
    url = await loop.run_in_executor(None, lambda: call_openai_sync(query))
    return url

def call_openai_sync(query: str) -> str:
    # Existing call_openai function renamed to call_openai_sync
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": query},
        ],
        functions=functions
    )

    function_call = completion.choices[0].message.function_call
    url = json.loads(function_call.arguments)["url"]
    return url

if __name__ == "__main__":
    asyncio.run(init_ws_server())