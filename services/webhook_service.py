import requests

def trigger_webhook(request_id):
    from services.database_service import get_webhook  
    
    webhook_data = get_webhook(request_id)
    
    if not webhook_data:  # Ensure data is not None
        print(f"No webhook found for request {request_id}")
        return

    webhook_url = webhook_data.get('webhook_url')  # Extract the actual URL

    if not webhook_url:  # Ensure the URL is valid
        print(f"Webhook URL missing for request {request_id}")
        return

    payload = {
        "request_id": request_id,
        "status": "completed"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"Webhook successfully triggered for request {request_id}")
        else:
            print(f"Webhook failed: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error triggering webhook for request {request_id}: {e}")