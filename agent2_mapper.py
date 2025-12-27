import json
import requests

def call_llm(prompt):
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload, timeout=300)
    return response.json()["response"]

def build_mapping_prompt(source_api, target_api):
        return f"""
    You are an enterprise API integration expert.

    Given the SOURCE API and TARGET API summaries, generate:
    1. Field-to-field mappings
    2. Required data transformations
    3. Unmapped fields (if any)

    Return ONLY valid JSON in the format below:

    {{
    "field_mappings": {{
        "source_field": "target_field"
    }},
    "transformations": {{
        "field": "transformation_rule"
    }},
    "unmapped_fields": {{
        "source_only": [],
        "target_only": []
    }}
    }}

    SOURCE API SUMMARY:
    {json.dumps(source_api, indent=2)}

    TARGET API SUMMARY:
    {json.dumps(target_api, indent=2)}
    """
def generate_mapping(source_file, target_file, output_file):
    with open(source_file, "r") as f:
        source_api = json.load(f)

    with open(target_file, "r") as f:
        target_api = json.load(f)

    prompt = build_mapping_prompt(source_api, target_api)
    ai_output = call_llm(prompt)

    # Clean JSON output
    start = ai_output.find("{")
    end = ai_output.rfind("}") + 1
    clean_json = ai_output[start:end]

    with open(output_file, "w") as f:
        f.write(clean_json)

    print(f"✔ Mapping generated and saved to {output_file}")

if __name__ == "__main__":
    generate_mapping(
        "order_api_summary.json",
        "billing_api_summary.json",
        "api_field_mapping.json"
    )
