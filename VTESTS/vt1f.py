import base64
import json
from openai import OpenAI
import time

from vt1 import get_audio

audio_filename = "input_audio.wav"

get_audio(audio_filename)


with open("input_audio.wav", "rb") as audio_file:
    wav_data = audio_file.read()
    encoded_string = base64.b64encode(wav_data).decode('utf-8')


print("Sending request to OpenAI...")

def get_system_prompt():
    part1 = """
    You are given a list of resources related to disaster recovery, government programs, financial analyses,
    and other related topics. Based on the user’s input or keywords, determine which URL they are likely referring to.
    Choose the most appropriate link by matching the user's input to one of the descriptions. Here is the list of options:
"""
    part2 = json.dumps(knowledge)
    return part1 + part2

## read the json file
with open("knowledge.json", "r") as file:
    knowledge = json.load(file)

client = OpenAI()
start_time = time.time()
completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "system",
            "content": get_system_prompt()
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_string,
                        "format": "wav"
                    }
                }
            ]
        },
    ]
)
end_time = time.time()

print(completion.choices[0].message)
print(f"Time taken: {end_time - start_time} seconds")
