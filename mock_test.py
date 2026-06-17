import requests
import json
import time

webhook_url = "http://localhost:8000/webhook/lead"

mock_lead = {
    "id": "lead_123",
    "name": "Jane Doe",
    "email": "jane@techcorp.com",
    "role": "VP of Engineering",
    "company": "Vercel",
    "website": "https://vercel.com",
    "linkedin": "https://www.linkedin.com/company/vercel/"
}

print("Sending mock lead to webhook...")
response = requests.post(webhook_url, json=mock_lead)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
print("Check the FastAPI server logs for the pipeline execution.")
