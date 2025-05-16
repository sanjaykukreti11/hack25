from chat import query_gemini_with_prompt1

API_KEY = "AIzaSyDSLZp7mAGFCZyjGrAyQ_WFPS16QJzQMq8"
MODEL = "gemini-1.5-flash-latest"  # Only certain models are available via API key
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
import requests

import json
import re

def load_text_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def clean_curl_command(raw_curl: str):
    text = query_gemini_with_prompt1(
        "give me proper formatted curl in the string form, so that i can import it in postman, don't give any extra text in the curl, only the curl text",
        raw_curl
    )
    return text

def extract_java_and_curl(text):
    # Regex for Java code block
    java_match = re.search(r'```java\s+(.*?)```', text, re.DOTALL)

    # Regex for curl command block
    bash_match = re.search(r'```bash\s+(.*?)```', text, re.DOTALL)
    instruction_match = re.search(r'(?<=Instructions:)([\s\S]*)', text , re.DOTALL)

    curl_code = ""
    if bash_match:
        bash_content = bash_match.group(1).strip()
        curl_lines = []
        collecting = False
        for line in bash_content.splitlines():
            if line.strip().startswith("curl"):
                collecting = True
            if collecting:
                curl_lines.append(line.strip())
                if not line.strip().endswith("\\"):
                    break
        raw_curl = " ".join(curl_lines)
        curl_code = clean_curl_command(raw_curl)

    # Extract the groups if found, else empty string
    java_code = java_match.group(1).strip() if java_match else ""
    instructions =instruction_match.group(1).strip() if instruction_match else ""

    return {
        "java": java_code,
        "curl": curl_code,
        "instructions": instructions
    }




def test_connection(user_query , json_data) -> str:
    java_template = load_text_from_file("/Users/sanjaykukreti/Desktop/zeotap_repo/Hack2025/prompts/java_template")

    #     prompt = f"""
    #
    # ## Objective
    # Generate a complete Java implementation for API integration that fully addresses all requirements specified in the `api_info.json` configuration file.
    #
    # ## Input Components
    # 1. **Query**: {user_query}
    # 2. **API Information**: Comprehensive details from {json_data}
    #
    # ## Output
    # 1. java code
    # 2. curl url
    #
    # **output must always include java code and curl url**
    #
    # ## Prompt Instructions
    #
    # ### 1. Parsing API Information
    # - Thoroughly parse and analyze the {json_data}
    # - Extract and validate all key requirements, including:
    # - Authentication mechanisms
    # - Endpoint details
    # - Request/response formats
    # - Error handling specifications
    # - Any specific installation or dependency requirements
    #
    # ### 2. Code Generation Requirements
    # #### a. Dependencies and Setup
    # - Automatically identify and import necessary Java libraries
    # - Create a Maven or Gradle dependency configuration if external libraries are required
    # - Implement proper dependency management based on API requirements
    #
    # #### b. Authentication Handling
    # - Implement robust authentication mechanisms from {json_data}
    # - Support various authentication types:
    # - API Key
    # - OAuth
    # - JWT
    # - Basic Authentication
    # - Securely manage and store credentials
    #
    # #### c. API Client Implementation
    # - Generate a comprehensive API client class
    #     - Create methods for all specified API endpoints
    # - Implement type-safe request and response handling
    # - Include robust error handling and exception management
    #
    # #### d. Configuration Management
    # - Create a flexible configuration loader that reads from {json_data}
    # - Support environment-specific configurations
    # - Implement configuration validation
    #
    # #### e. Request Handling
    # - Generate type-safe request builders
    # - Support different HTTP methods (GET, POST, PUT, DELETE, etc.)
    # - Implement request parameter and body serialization
    # - Handle content type conversions
    #
    # #### f. Response Processing
    # - Create robust response parsing mechanisms
    # - Support various response formats (JSON, XML, etc.)
    # - Implement type-safe deserialization
    # - Handle complex response structures
    #
    # #### g. Error Management
    # - Implement comprehensive error handling
    # - Create custom exception classes
    # - Log errors with meaningful context
    # - Provide retry mechanisms if specified in API info
    #
    #
    # ### 3. Additional Considerations
    # - Ensure thread-safety
    # - Implement proper resource management
    # - Add comprehensive logging
    # - Create documentation comments
    # - Follow Java best practices and design patterns
    #
    # ## Output Expectations
    # 1. Complete, runnable Java source code
    # 2. Fully commented implementation
    # 3. Maven or Gradle configuration file (if external dependencies are needed)
    # 4. README with usage instructions
    # 5. Example usage snippets
    #
    # ## Validation Criteria
    # - Full compliance with {json_data} requirements
    # - Robust and production-ready implementation
    # - Clean, maintainable code
    # - Comprehensive error handling
    # - Secure credential management
    #
    # ## Constraints
    # - Use standard Java libraries where possible
    # - Minimize external dependencies
    # - Prioritize type safety and compile-time checks
    # - Implement defensive programming techniques
    #
    # ## Example Placeholder
    # ```java
    # public class AutomaticApiIntegration {{
    # // Placeholder for generated API integration code
    # }}
    # ```
    #
    # ## Notes for Implementation
    # - Carefully read and interpret all details in {json_data}
    # - When in doubt about specific requirements, generate configurable, extensible code
    # - Provide clear comments explaining design decisions
    #
    #
    # **Only give Java code and curl url and nothing else**
    #
    #
    #
    # """

    prompt = f"""
    
    ## Objective
Generate a complete Java implementation for API integration that fully addresses all requirements specified in the `api_info.json` configuration file.

## Input Components
1. **Query**: {user_query}
2. **API Information**: Comprehensive details from {json_data}
3. **Java Template**: Use the Java code skeleton provided in `java_template.txt` as the base. Populate this template dynamically with correct logic, classes, and methods derived from the API information.{java_template}

## Output
1. java code (based on `Java Template`)
2. curl url
3. instructions to install dependencies and run the code

**output must always include java code and curl url* and instructions*
**java code must be generated by modifying and filling in the 'Java Template', not starting from scratch and do not add unnecessary data**

## Prompt Instructions

### 1. Parsing API Information
- Parse and analyze {json_data}
- Extract and validate all key requirements:
  - Authentication mechanisms
  - Endpoint details
  - Request/response formats
  - Error handling specs
  - Dependency and configuration needs

### 2. Code Generation Guidelines

#### a. Template Filling
- Read and understand 'Java Template'
- Retain structure and comments from the template
- Only fill the data params, headers, url, api type, request body from the data generated by llm using channel info
- Populate placeholders in the template with concrete logic (based on {json_data})
- Do not change the template structure unless required by the API logic only in extreme cases.

#### b. Authentication Handling
- Implement secure authentication as per API (API key, OAuth2, JWT, etc.)
- Insert credentials securely and appropriately in the template
- Ensure thread-safe and secure storage/use of credentials

#### c. HTTP Request Handling
- Replace placeholders for HTTP methods with:
  - Type-safe request builders
  - Support for query params, headers, request bodies
  - Use standard Java HTTP client (or suggest dependencies in pom.xml if needed)

#### d. Response & Error Processing
- Fill in logic for parsing response (JSON, XML, etc.)
- Implement robust error handling
- Populate the template's error blocks and response sections appropriately

#### e. Dependency Management
- If external libraries are required (e.g., Jackson, HttpClient), add Maven/Gradle configuration
- Fill in appropriate build configuration at the start or in a separate block

### 3. Additional Requirements
- Code must be production-ready
- Use best practices (thread safety, defensive coding, modular design)
- All methods must be documented with JavaDoc
- Add inline comments to explain logic added to the template
- Ensure the generated code matches the format and layout of `java_template.txt`

## Output Expectations
1. Fully filled-in Java source code using the given template
2. curl command equivalent of the main API operation (constructed using the same data from {json_data})
3. Maven/Gradle configuration if needed

## Constraints
- Use standard Java libraries where possible
- Prioritize filling and extending the existing template, not overwriting it
- Only output code and curl, nothing else

## Example Placeholder (do not change structure, only fill placeholders)
```java
public class AutomaticApiIntegration {{
    // {{AUTHENTICATION_BLOCK}}

    public static void main(String[] args) {{
    // {{REQUEST_BLOCK}}
    }}

    // {{HELPER_METHODS}}

    // {{ERROR_HANDLING}}
    }}

## Notes
- Focus on filling {{...}} placeholders in the template
- If a placeholder is missing but logic is needed, add it in a new method while keeping the overall template structure intact
- Keep output clean: Java code first, then curl and then the instructions


### Example Inputs You Would Use with This Prompt:
- `{user_query}`: "Retrieve user profile information from the API"
- `{json_data}`: Contents of `api_info.json`
- {java_template}: Template content loaded by your script and injected into the prompt

    
"""
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95,
            "topK": 40
        }
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code} - {response.text}")

    # Extract text response
    result = response.json()
    try:
        text_output = result['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        raise Exception("Unexpected response format")

    print(text_output)

    return extract_java_and_curl(text_output)
    # return text_output