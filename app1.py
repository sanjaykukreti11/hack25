import requests
import json
import re

API_KEY = "AIzaSyDSLZp7mAGFCZyjGrAyQ_WFPS16QJzQMq8"
MODEL = "gemini-1.5-flash-latest"  # Only certain models are available via API key
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def load_text_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_custom_prompt(file_name, int_id, action_id) -> str:
    file1_text = load_text_from_file("/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/test_channel_info.txt")
    file2_text = load_text_from_file(file_name)
    prompt = f"""
### Context from File 1:

### Context from File 2:
{file1_text}
{int_id}
{action_id}
{file2_text}

### Task:
Based on the content above, provide your analysis or answer the following question (if applicable):
"""

    # Gemini API expects the prompt as a structured object
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}],
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
        raise Exception(f"Request failed: {response.status_code} - {response.text}")

    result = response.json()
    text_response = result["candidates"][0]["content"]["parts"][0]["text"]
    print(text_response)

    cleaned_json_str = re.sub(r"^```json\n|```$", "", text_response.strip())
    return cleaned_json_str

# Example usage
# print(generate_custom_prompt("/path/to/your/second_file.txt"))
