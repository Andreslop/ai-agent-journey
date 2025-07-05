import json
import requests

# ---------------------------
# 1. Simulate LLM JSON Output
# ---------------------------

llm_response = '{"action": "search", "query": "AI agents for beginners"}'
parsed = json.loads(llm_response)
print("🤖 LLM parsed output:")
print(parsed)
print(f"Action: {parsed['action']} | Query: {parsed['query']}")

# ---------------------------
# 2. Use a dict to route a tool
# ---------------------------

def search_tool(q): return f"Searching for: {q}"
def calculator_tool(expr): return f"Evaluating: {expr} = 42"

TOOLS = {
    "search": search_tool,
    "calc": calculator_tool
}

tool_call = {"type": "calc", "args": "6 * 7"}
tool_fn = TOOLS[tool_call["type"]]
result = tool_fn(tool_call["args"])

print("\n🔧 Tool routing result:")
print(result)

# ---------------------------
# 3. Make a simple API call (GET)
# ---------------------------

response = requests.get("https://api.chucknorris.io/jokes/random")
joke = response.json()["value"]

print("\n🌐 External API call result:")
print("Chuck Norris joke:", joke)
