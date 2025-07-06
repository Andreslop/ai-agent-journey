import os
from openai import OpenAI
from dotenv import load_dotenv

# Load secret
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Load document
with open("d.txt", "r") as f:
    content = f.read()

# Step 2: Send to GPT for explanation
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You explain complex text in very simple terms."},
        {"role": "user", "content": f"Can you explain this text to me like I'm new to AI?\n\n{content}"}
    ]
)

# Step 3: Print result
print("💡 Explanation:\n")
print(response.choices[0].message.content)
