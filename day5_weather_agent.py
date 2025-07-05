import openai
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fake "weather" tool
def get_weather(city: str) -> str:
    mock_data = {
        "bogotá": "Rainy, 16°C",
        "medellín": "Sunny, 24°C",
        "cartagena": "Humid and hot, 31°C"
    }
    return mock_data.get(city.lower(), "City not found")

# User input
user_input = "What’s the weather like in medellín?"

# First message to GPT with tool description
response = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a helpful assistant that can call tools if needed."},
{"role": "user", "content": user_input}
],
tools=[
{
"type": "function",
"function": {
"name": "get_weather",
"description": "Returns the current weather for a city.",
"parameters": {
"type": "object",
"properties": {
"city": {"type": "string", "description": "The name of the city"}
},
"required": ["city"]
}
}
}
],
tool_choice="auto"
)

# Extract tool call info
tool_call = response.choices[0].message.tool_calls[0]
city_arg = json.loads(tool_call.function.arguments)["city"]

# Use the tool
weather_result = get_weather(city_arg)

# Continue the conversation with tool result
follow_up = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
{"role": "system", "content": "You are a helpful assistant that can call tools if needed."},
{"role": "user", "content": user_input},
{"role": "assistant", "tool_calls": [tool_call], "content": None},
{"role": "tool", "tool_call_id": tool_call.id, "name": "get_weather", "content": weather_result}
]
)

print("💬 Final reply:\n")
print(follow_up.choices[0].message.content)