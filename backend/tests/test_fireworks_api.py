import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_fireworks():
    api_key = os.getenv("FIREWORKS_API_KEY", "fw_WFZwGf4HUBhkotefpw4BkX")
    endpoint = "https://api.fireworks.ai/inference/v1"
    model = os.getenv("FIREWORKS_MODEL", "accounts/fireworks/models/deepseek-v4-pro")
    
    print(f"Testing Fireworks API...")
    print(f"Model: {model}")
    print(f"Key: {api_key[:10]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello, write a 1 sentence greeting."}
        ],
        "max_tokens": 100,
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(f"{endpoint}/chat/completions", json=payload, headers=headers)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()['choices'][0]['message']['content']}")
            else:
                print(f"Error Response: {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")

asyncio.run(test_fireworks())
