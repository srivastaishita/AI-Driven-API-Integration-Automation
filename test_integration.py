
from integration import send_to_billing

def test_send_to_billing():
    source_data = {
            "order_id": "test_value",
        "customer_id": "test_value",
        "order_date": "test_value",
        "order_amount": "test_value",
        "currency": "test_value",

    }

    result = send_to_billing(source_data)
    assert result is not None
    