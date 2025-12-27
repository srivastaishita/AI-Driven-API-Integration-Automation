
import requests

def send_to_billing(source_data):
    url = "https://api.billing-system.com/transactions"
    
    headers = {
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
    }

    payload = {
    "order_reference": source_data.get("order_id"),
    "customer_id": source_data.get("customer_id"),
    "order_date": source_data.get("order_date"),
    "total_amount": source_data.get("order_amount"),
    "currency": source_data.get("currency"),
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Integration failed: {response.text}")
    