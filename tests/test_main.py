from main import add_menu_to_cal, convert_to_iso
from unittest.mock import MagicMock, patch
from datetime import datetime

def test_add_menu_to_cal(mocker):
    """Test that add_menu_to_cal creates calendar events correctly."""
    # Mock the scraped menu
    mock_scrape_menu = mocker.patch("main.scrape_menu")
    mock_scrape_menu.return_value = {
        "Mandag": {
            "Dagens": "Pizza",
            "Vegetar dagens": "Salad",
            "Suppe": "Tomato",
        }
    }

    # Mock the GCal instance
    mock_gcal_instance = MagicMock()
    mocker.patch("main.GCal", return_value=mock_gcal_instance)

    # Call the function
    add_menu_to_cal()

    # Assert the event was created
    mock_gcal_instance.create_event.assert_called_once_with(
        summary="Pizza",
        description="Dagens: Pizza\nVegetar: Salad\nSuppe: Tomato",
        start_time=datetime.now().replace(hour=11, minute=30, second=0, microsecond=0).isoformat(),
        end_time=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0).isoformat(),
    )

def test_get_day_date(mocker):
    """Test that get_day_date returns the correct ISO formatted date."""
    # Mock today as Monday
    mock_datetime = mocker.patch("main.datetime")
    mock_datetime.today.return_value = datetime(2023, 10, 2)  # Monday
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Test for Tuesday
    result = convert_to_iso("tirsdag", hour=11, minute=30)
    expected = datetime(2023, 10, 3, 11, 30).isoformat()
    assert result == expected