from datetime import datetime
import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def init(development=False):
    """Authenticate and initialize the Google Calendar API service."""
    creds = None
    if development:
        # Check if token.json exists for saved credentials
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Run the OAuth flow to create new credentials
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for future use
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
    else:
        creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)

    return build("calendar", "v3", credentials=creds)

class GCal:
    def __init__(self):
        self.service = init()

    def create_event(self, summary: str, description: str, start_time, end_time, reminder_len=10):
        """Create and insert a Google Calendar event."""
        event = {
            "summary": summary,
            "location": "Online",
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "Europe/Oslo",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Europe/Oslo",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": reminder_len},
                ],
            },
        }
        event_result = self.service.events().insert(calendarId="primary", body=event).execute()
        print("Event created:", event_result.get("htmlLink"))

def get_current_time():
    """Get the current time in ISO format."""
    return datetime.now().isoformat()
