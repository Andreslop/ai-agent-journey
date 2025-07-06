import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tool functions
def tell_joke(_):
    response = requests.get("https://api.chucknorris.io/jokes/random")
    return response.json()["value"]

def do_math(expr):
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Math error: {e}"

def search(_):
    return "Pretend I'm searching the web (real API coming soon)."

# Available tools
TOOLS = {
    "joke": tell_joke,
    "math": do_math,
    "search": search
}

# User prompt
user_input = input("💬 Ask the agent something (e.g. tell a joke, 6*7): ").strip()

# GPT decides tool to use
tool_selector = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """
You're an agent controller. Given a user message, reply ONLY in valid JSON like:
{"tool": "math", "input": "456*34"}
Do NOT add explanation, markdown, or extra text.
Available tools:
- joke
- math
- search
""" },
        {"role": "user", "content": user_input}
    ]
)

# Parse GPT's JSON reply
try:
    tool_choice = json.loads(tool_selector.choices[0].message.content)
    tool_name = tool_choice.get("tool", "")
    tool_input = tool_choice.get("input", "")
except Exception as e:
    print("❌ Failed to parse GPT tool selection.")
    print("Raw GPT output:", tool_selector.choices[0].message.content)
    tool_name = ""
    tool_input = ""

# Run the selected tool
if tool_name not in TOOLS:
    result = "I didn't recognize a valid tool to use."
else:
    print(f"🧠 Tool selected: {tool_name} | Input: {tool_input}")
    result = TOOLS[tool_name](tool_input)

# Final agent reply using the tool result
final_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You're a helpful AI assistant. When I give you a result from a tool, explain it clearly and directly to the user."},
        {"role": "user", "content": f"The tool returned: {result}. Tell the user what this means."}
    ]
)

# Print final answer
print("\n🤖 Agent says:\n")
print(final_response.choices[0].message.content)
