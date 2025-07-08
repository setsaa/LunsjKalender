from datetime import datetime
import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as UserCredentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "sigurdsets@gmail.com"

def init(development=False):
    """Authenticate and initialize the Google Calendar API service."""
    creds = None
    if development:
        # Check if token.json exists for saved credentials
        if os.path.exists("token.json"):
            creds = UserCredentials.from_authorized_user_file("token.json", SCOPES)
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
        creds = ServiceAccountCredentials.from_service_account_file("service_account.json", scopes=SCOPES)

    return build("calendar", "v3", credentials=creds)

class GCal:

    def __init__(self):
        self.service = init()

    def event_exists(self, summary: str, start_time, end_time) -> bool:
        """Check if an event with a given summary already exists."""
        events_result = self.service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        return any(event["summary"] == summary for event in events)


    def create_event(self, summary: str, description: str, start_time, end_time):
        """Create and insert a Google Calendar event."""
        if not self.event_exists(summary, start_time, end_time):
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
		    "overrides": []
		}
            }
            event_result = self.service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print("Event created:", event_result.get("htmlLink"))
        else:
            print("Event already exists. Skipping creation.")

def get_current_time():
    """Get the current time in ISO format."""
    return datetime.now().isoformat()
