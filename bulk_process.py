import csv
import requests
import time

webhook_url = "http://localhost:8000/webhook/lead"
csv_file = "sample_leads.csv"

def bulk_process():
    print(f"Reading leads from {csv_file}...")
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            print(f"Triggering webhook for {row['name']} at {row['company']}...")
            response = requests.post(webhook_url, json=row)
            print(f"Status: {response.status_code}, Msg: {response.json()}")
            time.sleep(1) # Prevent flooding

if __name__ == "__main__":
    bulk_process()
    print("Bulk processing initiated! Check the server logs and leads.db for results.")
