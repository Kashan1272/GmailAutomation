import schedule
import time
import sys
from config import SCHEDULE_TIMES, RECIPIENT, SUBJECT, BODY
from gmail_service import get_gmail_service, send_email
from logger import setup_logger, log_email

def run_email_task(service, recipient: str, subject: str, body: str) -> None:
    """Wrapper to send email and log results."""
    result = send_email(service, "me", recipient, subject, body)
    log_email(recipient, subject, result["status"], result.get("message_id") or result.get("error"))
    
    status_icon = "✅" if result["status"] == "success" else "❌"
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {status_icon} {result['status'].upper()}")
    if result["status"] == "error":
        print(f"   ↳ {result['error']}")

def main() -> None:
    print("🚀 Initializing Email Automation Script...")
    setup_logger()
    
    try:
        service = get_gmail_service()
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)
        
    print("✅ Gmail API authenticated successfully.")
    print(f"📅 Scheduled times: {', '.join(SCHEDULE_TIMES)}")
    print("⏳ Waiting for scheduled runs... (Press Ctrl+C to stop)\n")

    # Register scheduled jobs
    for time_str in SCHEDULE_TIMES:
        schedule.every().day.at(time_str).do(
            run_email_task, service=service, recipient=RECIPIENT, subject=SUBJECT, body=BODY
        )

    # Scheduler loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()