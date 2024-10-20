import json
from openai import OpenAI
import time

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


def call_openai(query: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": query},
        ],
        functions=[
            {
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
        ],
    )

    function_call = completion.choices[0].message.function_call
    url = json.loads(function_call.arguments)["url"]
    return url

start_time = time.time()
url = call_openai("public assistance")
print(f"THE URL: {url}")
url = call_openai("hmgp")
print(f"THE URL: {url}")
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
