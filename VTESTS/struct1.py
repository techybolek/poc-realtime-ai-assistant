import json
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ],
    response_format=MathReasoning,
)

def pretty_print_json(obj):
    """
    Pretty print any JSON-serializable object.
    If the object is not directly JSON-serializable (like a Pydantic model),
    it attempts to convert it to a dict first.
    """
    try:
        # If it's a Pydantic model, convert to dict first
        if isinstance(obj, BaseModel):
            obj_dict = obj.model_dump()
        else:
            obj_dict = obj

        # Pretty print the JSON
        print(json.dumps(obj_dict, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error pretty printing object: {e}")

math_reasoning = completion.choices[0].message.parsed
pretty_print_json(math_reasoning)
