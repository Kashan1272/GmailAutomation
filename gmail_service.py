import os
import base64
import google.auth.transport.requests
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import SCOPES, CREDENTIALS_PATH, TOKEN_PATH

def get_gmail_service() -> build:
    """Authenticate and return a Gmail API service instance."""
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"❌ '{CREDENTIALS_PATH}' not found. Download it from Google Cloud Console."
        )

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def send_email(service, sender: str, to: str, subject: str, body: str) -> dict:
    """Construct and send an email via Gmail API. Returns status dict."""
    message = MIMEText(body)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    raw_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        response = service.users().messages().send(userId="me", body=raw_message).execute()
        return {"status": "success", "message_id": response["id"]}
    except HttpError as error:
        return {"status": "error", "error": str(error)}