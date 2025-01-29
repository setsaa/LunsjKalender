from google_calendar import GCal
from unittest.mock import MagicMock

def test_create_event(mocker):
    """Test that create_event calls the Google Calendar API correctly."""
    # Mock the init function to return a mock service
    mock_service = MagicMock()
    mocker.patch("google_calendar.init", return_value=mock_service)

    # Create an instance of GCal
    gcal = GCal()

    # Mock the events().insert() method
    mock_insert = mock_service.events.return_value.insert
    mock_insert.return_value.execute.return_value = {"htmlLink": "http://example.com"}

    # Call the method
    summary = "Test Event"
    description = "This is a test event."
    start_time = "2023-10-01T10:00:00"
    end_time = "2023-10-01T11:00:00"
    gcal.create_event(summary, description, start_time, end_time)

    # Assert the API was called correctly
    mock_insert.assert_called_once_with(
        calendarId="primary",
        body={
            "summary": summary,
            "location": "Online",
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "Europe/Oslo"},
            "end": {"dateTime": end_time, "timeZone": "Europe/Oslo"},
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "popup", "minutes": 10}],
            },
        },
    )