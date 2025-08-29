import requests
import time
import threading
import os
from datetime import datetime

def keep_server_alive():
    """Send GET request to keep server alive every 14 minutes"""
    url = os.environ.get('API_URL', 'https://skilltrail-84ny.onrender.com/keep-alive')
    
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[{datetime.now()}] GET request sent successfully")
            else:
                print(f"[{datetime.now()}] GET request failed: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now()}] Error while sending request: {e}")
        
        # Wait 14 minutes (840 seconds)
        time.sleep(840)

def start_cron_job():
    """Start the cron job in a background thread"""
    thread = threading.Thread(target=keep_server_alive, daemon=True)
    thread.start()
    print("Cron job started - keeping server alive every 14 minutes")
