from fastapi import FastAPI, HTTPException, BackgroundTasks
import json
import os
import logging
import sqlite3
from pydantic import BaseModel
from typing import Optional
from sdr_crew import SDRPipeline

app = FastAPI(title="SDR Webhook Pipeline")
logging.basicConfig(level=logging.INFO)

# Database Setup
def init_db():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            company TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class LeadPayload(BaseModel):
    id: str
    name: str
    email: str
    role: str
    company: str
    website: Optional[str] = None
    linkedin: Optional[str] = None

# Load ICP schema
try:
    with open("icp_schema.json", "r") as f:
        ICP_DATA = json.load(f)
except FileNotFoundError:
    ICP_DATA = {"minimum_qualification_score": 70}

def process_lead(lead: LeadPayload, mock: bool = False):
    logging.info(f"Starting SDR pipeline for lead: {lead.name} from {lead.company}")
    try:
        if mock:
            logging.info("Running MOCKED pipeline execution...")
            import time
            time.sleep(2) # Simulate work
            result = f"""
[MOCKED] Qualification Score: 85
[MOCKED] Reasoning: Matches ICP criteria perfectly. High growth SaaS.
[MOCKED] Drafted Email:
Hi {lead.name.split()[0]},
I saw Vercel is experiencing rapid growth right now! Given your role as {lead.role}, I imagine you might be running into slow lead response times. Our tool can help you automate this and book meetings instantly. Worth a quick chat?
"""
        else:
            pipeline = SDRPipeline(lead_data=lead.dict(), icp_data=ICP_DATA)
            result = pipeline.run()
            
        logging.info(f"Pipeline completed for {lead.name}.")
        logging.info(f"Result:\n{result}")
        
        # Save result to database
        conn = sqlite3.connect("leads.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO leads (id, name, email, company, result)
            VALUES (?, ?, ?, ?, ?)
        ''', (lead.id, lead.name, lead.email, lead.company, str(result)))
        conn.commit()
        conn.close()
        logging.info(f"Saved result for {lead.name} to database.")
    except Exception as e:
        logging.error(f"Pipeline failed for lead {lead.name}: {str(e)}")
        # Fallback: alert human rep
        alert_human_rep(lead, str(e))

def alert_human_rep(lead, error_msg):
    logging.warning(f"ALERT HUMAN REP: Pipeline failed for {lead.email}. Error: {error_msg}")

@app.post("/webhook/lead")
async def receive_lead(lead: LeadPayload, background_tasks: BackgroundTasks):
    """
    Webhook endpoint to receive new leads from HubSpot/Salesforce.
    Triggers the CrewAI pipeline in the background to ensure response within 5 minutes.
    """
    is_mock = False
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("SERPER_API_KEY"):
        logging.warning("Missing API keys. Falling back to MOCK mode for demonstration.")
        is_mock = True
        
    # Run in background to not block the webhook response
    background_tasks.add_task(process_lead, lead, is_mock)
    return {"status": "success", "message": f"Lead received, processing initiated (Mock={is_mock})."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
