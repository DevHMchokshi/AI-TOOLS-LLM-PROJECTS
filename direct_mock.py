import time

def simulate_pipeline():
    print("INFO: Starting SDR pipeline for lead: Jane Doe from Vercel")
    print("INFO: Running MOCKED pipeline execution...")
    time.sleep(2) # Simulate work
    
    result = """
=========================================
[MOCKED] Qualification Score: 85
[MOCKED] Reasoning: Matches ICP criteria perfectly. High growth SaaS.

[MOCKED] Drafted Email:
Subject: Quick question about Vercel's lead response times

Hi Jane,

I saw Vercel is experiencing rapid growth right now! Given your role as VP of Engineering, I imagine you might be running into slow lead response times with the influx of new sign-ups. 

Our tool can help your team automate this and book meetings instantly so you never miss out on a warm lead. 

Worth a quick chat later this week?

Best,
SDR AI
=========================================
"""
    print(f"INFO: Pipeline completed for Jane Doe.")
    print(f"INFO: Result:\n{result}")

if __name__ == "__main__":
    simulate_pipeline()
