import json
def load_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)

def generate_payload(mapping):
    lines = []
    lines.append("payload = {")
    
    for source, target in mapping["field_mappings"].items():
        lines.append(f'    "{target}": source_data.get("{source}"),')
    
    lines.append("}")
    return "\n".join(lines)

def generate_integration_code(mapping, target_api):
    payload_code = generate_payload(mapping)
    
    code = f'''
    import requests

    def send_to_billing(source_data):
    url = "https://api.billing-system.com{target_api["endpoint"]}"
    
    headers = {{
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
    }}

    {payload_code}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Integration failed: {{response.text}}")
    '''
    return code

def generate_test_code(mapping):
    test_code = '''
from integration import send_to_billing

def test_send_to_billing():
    source_data = {
    '''
    for source in mapping["field_mappings"].keys():
        test_code += f'        "{source}": "test_value",\n'

    test_code += '''
    }

    result = send_to_billing(source_data)
    assert result is not None
    '''
    return test_code

def run_agent_3():
    mapping = load_json("order_to_billing_mapping.json")
    target_api = load_json("billing_api_summary.json")

    integration_code = generate_integration_code(mapping, target_api)
    test_code = generate_test_code(mapping)

    with open("integration.py", "w") as f:
        f.write(integration_code)

    with open("test_integration.py", "w") as f:
        f.write(test_code)

    print("✔ Integration code and tests generated")

if __name__ == "__main__":
    run_agent_3()
