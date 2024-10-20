import json
from openai import OpenAI
import time
from pydantic import BaseModel


def get_system_prompt():
    part1 = """
    You are given a list of resources related to disaster recovery, government programs, financial analyses,
    and other related topics. Based on the user’s input or keywords, determine which URL they are likely referring to.
    Choose the most appropriate link by matching the user's input to one of the descriptions. Here is the list of options:
"""
    part2 = json.dumps(knowledge)
    return part1 + part2

with open("urls.json", "r") as file:
    knowledge = json.load(file)

client = OpenAI()

class UrlSchema(BaseModel):
    url: str

start_time = time.time()
completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages = [
        {
            "role": "system", "content": get_system_prompt()
        },
        {
            "role": "user", "content": "public assistance"
        },
    ],
    response_format=UrlSchema,
)
end_time = time.time()

print(completion.choices[0].message.parsed)
print(f"Time taken: {end_time - start_time} seconds")
