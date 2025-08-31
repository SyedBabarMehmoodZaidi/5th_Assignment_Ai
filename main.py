import os
import re
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = "gemini-1.5-flash"

# ---------- Tools ----------
def add(a: int, b: int) -> int:
    return a + b

def get_weather(city: str) -> str:
    weather_data = {
        "Karachi": "30°C, Sunny",
        "Lahore": "28°C, Cloudy",
        "Islamabad": "25°C, Rainy"
    }
    return weather_data.get(city, f"No data for {city}")

# ---------- Agent ----------
async def agent(user_input: str):
    # Weather check
    if "weather" in user_input.lower():
        city = None
        for w in user_input.replace("?", "").split():
            if w.lower() in ["karachi", "lahore", "islamabad"]:
                city = w.capitalize()
                break
        if city:
            return f"Weather in {city}: {get_weather(city)}"
        return "Sorry, I couldn't find the city."

    # Math check
    elif any(op in user_input.lower() for op in ["add", "+", "sum"]):
        nums = [int(n) for n in re.findall(r"\d+", user_input)]
        if len(nums) == 2:
            return f"Result: {add(nums[0], nums[1])}"
        else:
            return "Please provide two numbers."

    # Fallback -> Gemini
    else:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = await model.generate_content_async(user_input)
        return response.text

# ---------- Main ----------
async def main():
    queries = [
        "What is 15 + 37?",
        "What is the weather in Lahore?"
    ]
    for q in queries:
        res = await agent(q)
        print(f"User: {q}")
        print(f"Agent: {res}\n")

if __name__ == "__main__":
    asyncio.run(main())
