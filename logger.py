# logger.py
import os
import csv
from datetime import datetime
from config import LOG_PATH

def setup_logger() -> None:
    """Create log directory and initialize CSV header if missing."""
    # Ensure directory exists
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        print(f"✅ Created directory: {log_dir}")
    
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Recipient", "Subject", "Status", "Message_ID/Error"])
        print(f"✅ Created new log file: {LOG_PATH}")
    else:
        print(f"📁 Log file exists: {LOG_PATH}")

def log_email(recipient: str, subject: str, status: str, detail: str) -> None:
    """Append email send result to history log."""
    try:
        # Ensure directory exists
        log_dir = os.path.dirname(LOG_PATH)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), recipient, subject, status, detail])
        print(f"✅ Logged email to {recipient} - Status: {status}")
    except Exception as e:
        print(f"❌ Error logging email: {e}")
        raise