from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import re

WEEKDAYS = [
    "Mandag",
    "Tirsdag",
    "Onsdag",
    "Torsdag",
    "Fredag"
]

pattern = r"(Dagens:.*?)(?=\s*(?:Vegetar dagens:|Vegetar:|Suppe|$))|(Vegetar dagens:.*?|Vegetar:.*?)(?=\s*(?:Suppe|$))|(Suppe:.*)"

def scrape_menu():
    menu_json = {}

    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    options.add_argument("--disable-gpu")  # Disable GPU (required for headless)
    options.add_argument("--no-sandbox")  # For CI environments like GitHub Actions
    
    # Create a temporary directory for the user data
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")  # Set custom user data dir

    # Setup WebDriver with custom options
    driver = webdriver.Chrome(options=options)
    url = "https://tullin.munu.shop/meny"
    driver.get(url)

    sleep(1)

    website_text = driver.find_element(By.TAG_NAME, "body").text

    # Remove cookie policy text using regex (add more terms if necessary)
    website_text = re.sub(r"(Suppe:.*?)(Personvern|Salgsbetingelser|Logg inn|Vi bruker cookies).*", r"\1", website_text, flags=re.DOTALL)
    
    sorted_text = split_span(website_text)

    for day, menu_text in sorted_text.items():
        # Extract menu items
        menu_items = re.findall(pattern, menu_text)
        menu_items = [item for group in menu_items for item in group if item]

        # Check that we have the expected number of menu items
        if len(menu_items) != 3:
            raise Exception(f"Unexpected number of menu items for {day}. Found: {menu_items}")
        
        menu_dict = {
            "Dagens": str(menu_items[0]).split(":")[1].strip(),
            "Vegetar dagens": str(menu_items[1]).split(":")[1].strip(),
            "Suppe": str(menu_items[2]).split(":")[1].strip()
        }
        menu_json[day] = menu_dict

    driver.quit()
    return menu_json

def split_span(span: str) -> dict:
    split_list = {}
    span = span.replace("\n", " ")
    
    for i, day in enumerate(WEEKDAYS):
        day_start = span.find(day)
        if day_start == -1:  # Skip if day is not found
            continue
        next_day_start = (
            span.find(WEEKDAYS[i + 1]) if i + 1 < len(WEEKDAYS) else len(span)
        )
        split_list[day] = span[day_start:next_day_start].strip()

    return split_list

if __name__ == "__main__":
    menu = scrape_menu()
    print(menu)