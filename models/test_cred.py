MODEL_ID = "gemini-2.0-flash"
PROJECT_ID = "zeotap-dev-datascience"
LOCATION = "europe-west1"

import vertexai
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel
import json
import re

def extract_java_and_curl(text):
    # Regex for Java code block
    java_match = re.search(r'```java\s+(.*?)```', text, re.DOTALL)

    # Regex for curl command block
    curl_match = re.search(r'```curl\s+(.*?)```', text, re.DOTALL)

    # Extract the groups if found, else empty string
    java_code = java_match.group(1).strip() if java_match else ""
    curl_code = curl_match.group(1).strip() if curl_match else ""

    return {
        "java": java_code,
        "curl": curl_code
    }

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
model1 = GenerativeModel(MODEL_ID)


def test_connection(user_query , json_data) -> str:


    # Combine into a prompt
    prompt = f"""

## Objective
Generate a complete Java implementation for API integration that fully addresses all requirements specified in the `api_info.json` configuration file.

## Input Components
1. **Query**: {user_query}
2. **API Information**: Comprehensive details from {json_data}

## Output
1. java code
2. curl url
## Prompt Instructions

### 1. Parsing API Information
- Thoroughly parse and analyze the {json_data}
- Extract and validate all key requirements, including:
- Authentication mechanisms
- Endpoint details
- Request/response formats
- Error handling specifications
- Any specific installation or dependency requirements

### 2. Code Generation Requirements
#### a. Dependencies and Setup
- Automatically identify and import necessary Java libraries
- Create a Maven or Gradle dependency configuration if external libraries are required
- Implement proper dependency management based on API requirements

#### b. Authentication Handling
- Implement robust authentication mechanisms from {json_data}
- Support various authentication types:
- API Key
- OAuth
- JWT
- Basic Authentication
- Securely manage and store credentials

#### c. API Client Implementation
- Generate a comprehensive API client class
    - Create methods for all specified API endpoints
- Implement type-safe request and response handling
- Include robust error handling and exception management

#### d. Configuration Management
- Create a flexible configuration loader that reads from {json_data}
- Support environment-specific configurations
- Implement configuration validation

#### e. Request Handling
- Generate type-safe request builders
- Support different HTTP methods (GET, POST, PUT, DELETE, etc.)
- Implement request parameter and body serialization
- Handle content type conversions

#### f. Response Processing
- Create robust response parsing mechanisms
- Support various response formats (JSON, XML, etc.)
- Implement type-safe deserialization
- Handle complex response structures

#### g. Error Management
- Implement comprehensive error handling
- Create custom exception classes
- Log errors with meaningful context
- Provide retry mechanisms if specified in API info

### 3. Additional Considerations
- Ensure thread-safety
- Implement proper resource management
- Add comprehensive logging
- Create documentation comments
- Follow Java best practices and design patterns

## Output Expectations
1. Complete, runnable Java source code
2. Fully commented implementation
3. Maven or Gradle configuration file (if external dependencies are needed)
4. README with usage instructions
5. Example usage snippets

## Validation Criteria
- Full compliance with {json_data} requirements
- Robust and production-ready implementation
- Clean, maintainable code
- Comprehensive error handling
- Secure credential management

## Constraints
- Use standard Java libraries where possible
- Minimize external dependencies
- Prioritize type safety and compile-time checks
- Implement defensive programming techniques

## Example Placeholder
```java
public class AutomaticApiIntegration {{
// Placeholder for generated API integration code
}}
```

## Notes for Implementation
- Carefully read and interpret all details in {json_data}
- When in doubt about specific requirements, generate configurable, extensible code
- Provide clear comments explaining design decisions

**output must include java code and curl url**
**Only give Java code and curl url and nothing else**



"""
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

    return extract_java_and_curl(response.text.strip());