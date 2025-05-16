import requests
import json

API_KEY = "AIzaSyDSLZp7mAGFCZyjGrAyQ_WFPS16QJzQMq8"
MODEL = "gemini-1.5-flash-latest"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def query_gemini_with_prompt(prompt: str, query: str) -> dict:
    combined_text = f"{prompt.strip()}\n\n{query.strip()}"

    payload = {
        "contents": [
            {
                "parts": [{"text": combined_text}],
                "role": "user"
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95,
            "topK": 40
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return { "message": f"Error: {response.status_code} - {response.text}" }

    try:
        result = response.json()
        text_response = result["candidates"][0]["content"]["parts"][0]["text"]
        with open("/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/channel_info2.txt", "a", encoding="utf-8") as file:
            file.write(text_response + "\n")
        return { "message": text_response }
    except (KeyError, IndexError):
        return { "message": "Unexpected response format from Gemini API." }



def query_gemini_with_prompt1(prompt: str, query: str) -> str:
    combined_text = f"{prompt.strip()}\n\n{query.strip()}"

    payload = {
        "contents": [
            {
                "parts": [{"text": combined_text}],
                "role": "user"
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95,
            "topK": 40
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        return response.text

    result = response.json()
    text_response = result["candidates"][0]["content"]["parts"][0]["text"]
    return text_response
