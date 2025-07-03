import openai
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What's one beginner-friendly AI agent project I could build?"}
    ]
)

print("💬 Assistant says:\n")
print(response.choices[0].message.content)
