from webscraper import scrape_menu, split_span
from unittest.mock import MagicMock

def test_scrape_menu(mocker):
    """Test that scrape_menu extracts the menu correctly."""
    # Mock the WebDriver and its methods
    mock_driver = MagicMock()
    mock_driver.find_element.return_value.text = """
        Mandag Dagens: Pizza Vegetar dagens: Salad Suppe: Tomato
        Tirsdag Dagens: Pasta Vegetar dagens: Soup Suppe: Lentil
    """
    mocker.patch("webscraper.webdriver.Chrome", return_value=mock_driver)

    # Call the function
    menu = scrape_menu()

    # Assert the result
    expected_menu = {
        "Mandag": {
            "Dagens": "Pizza",
            "Vegetar dagens": "Salad",
            "Suppe": "Tomato",
        },
        "Tirsdag": {
            "Dagens": "Pasta",
            "Vegetar dagens": "Soup",
            "Suppe": "Lentil",
        },
    }
    assert menu == expected_menu

def test_split_span():
    """Test that split_span correctly splits the text by weekdays."""
    input_text = "Mandag Dagens: Pizza Tirsdag Dagens: Pasta"
    expected_output = {
        "Mandag": "Mandag Dagens: Pizza",
        "Tirsdag": "Tirsdag Dagens: Pasta",
    }
    print(split_span(input_text))
    print(expected_output)
    assert split_span(input_text) == expected_output