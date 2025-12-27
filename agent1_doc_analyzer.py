print("=== Agent 1 started ===")

import json
import requests
import os

#Function to Call Ollama
def call_mistral(prompt):
    url ="http://localhost:11434/api/generate"
    
    payload = {
       "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
    url,
    json=payload,
    timeout=300   # seconds
    )

    return response.json()["response"]

#Prompt Template
def build_prompt(api_json):
    return f"""
    You are an enterprise API documentation analyzer.

    Analyze the following API definition and extract:
    1. API name
    2. Authentication mechanism
    3. Endpoint
    4. HTTP method
    5. List of request fields
    6. List of response fields

    Return ONLY valid JSON in the format below:

    {{
    "api_name": "",
    "authentication": "",
    "endpoint": "",
    "method": "",
    "request_fields": [],
    "response_fields": []
    }}

    API Definition:
    {json.dumps(api_json, indent=2)[:1500]}

    """

#Analyzer Function
def analyze_api(input_file, output_file):
    with open(input_file, "r") as f:
        api_definition = json.load(f)

    prompt = build_prompt(api_definition)
    ai_output = call_mistral(prompt)
    # Ensure only JSON is saved
    start = ai_output.find("{")
    end = ai_output.rfind("}") + 1
    clean_json = ai_output[start:end]

    # Save structured output
    with open(output_file, "w") as f:
        f.write(clean_json)

    print(f"✔ API analyzed and saved to {output_file}")

if __name__ == "__main__":
    analyze_api("order_api.json", "order_api_summary.json")
    print(">>> Finished Order API, moving to Billing API <<<")
    analyze_api("billing_api.json", "billing_api_summary.json")
