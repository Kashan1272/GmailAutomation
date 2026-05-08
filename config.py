import os

# OAuth 2.0 Scopes (send only)
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# File Paths
CREDENTIALS_PATH = "credentials.json"
TOKEN_PATH = "token.json"
LOG_PATH = "logs/email_history.csv"

# Email Configuration (override via environment variables in production)
RECIPIENT = os.getenv("EMAIL_RECIPIENT", "recipient@example.com")
SUBJECT = os.getenv("EMAIL_SUBJECT", "Automated Daily Report")
BODY = os.getenv("EMAIL_BODY", "This is an automated email sent via Gmail API.")

# Schedule Times (24h format, system timezone)
SCHEDULE_TIMES = ["09:00", "14:30", "18:00"]