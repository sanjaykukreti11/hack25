import re

MODEL_ID = "gemini-2.0-flash"
PROJECT_ID = "zeotap-dev-datascience"
LOCATION = "europe-west1"

import vertexai
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel
import json

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
model1 = GenerativeModel(MODEL_ID)

def load_text_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_custom_prompt(file_name) -> str:
    file1_text = load_text_from_file("/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/channel_info.txt")
    file2_text = load_text_from_file(file_name)

    # Combine into a prompt
    prompt = f"""
### Context from File 1:

### Context from File 2:
{file1_text}
{file2_text}

### Task:
Based on the content above, provide your analysis or answer the following question (if applicable):
"""

    # Generation settings
    generation_config = generative_models.GenerationConfig(
        temperature=0.2,
        top_p=0.95,
        top_k=40
    )

    # Generate content
    response = model1.generate_content(
        prompt,
        generation_config=generation_config,
        stream=False
    )
    print(response.text)
    cleaned_json_str = re.sub(r"^```json\n|```$", "", response.text.strip())
    return cleaned_json_str

# Run the function
# print(generate_custom_prompt())
