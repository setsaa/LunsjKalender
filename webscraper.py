from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import tempfile

WEEKDAYS = [
    "Mandag",
    "Tirsdag",
    "Onsdag",
    "Torsdag",
    "Fredag"
]

pattern = r"(Dagens:.*?)(?=\s*(?:Vegetar dagens:|Vegetar:|Suppe|$))|(Vegetar dagens:.*?|Vegetar:.*?)(?=\s*(?:Suppe|$))|(Suppe:.*)"

class WebScraper:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_dir}")

        self.driver = webdriver.Chrome(options=options)
        self.url = "https://tullin.munu.shop/meny"

    def scrape_menu(self) -> dict:
        menu_json = {}
        
        self.driver.get(self.url)

        sleep(1)  # Avoid race condition

        website_text = self.driver.find_element(By.TAG_NAME, "body").text

        # Remove cookie policy text using regex
        website_text = re.sub(r"(Suppe:.*?)(Personvern|Salgsbetingelser|Logg inn|Vi bruker cookies).*", r"\1", website_text, flags=re.DOTALL)
        
        sorted_text = split_span(website_text)

        for day, menu_text in sorted_text.items():
            try:
                # Extract menu items with regex
                menu_items = re.findall(pattern, menu_text)
                menu_items = [item for group in menu_items for item in group if item]

                # If there are 2 menu items it is likely a "veggie day" at the
                # cantina. `veggie_index` is then set accordingly as the first
                # menu item will be both the "daily" and the "veggie" option.
                if len(menu_items) == 2:
                    veggie_index = 0
                elif len(menu_items) < 2:
                    raise Exception(f"Error: Unexpected number of menu items for {day}. Found: {menu_text}")
                else:
                    veggie_index = 1
                menu_dict = {
                    "Dagens": str(menu_items[0]).split(":")[1].strip(),
                    "Vegetar dagens": str(menu_items[veggie_index]).split(":")[1].strip(),
                    "Suppe": str(menu_items[2]).split(":")[1].strip()
                }
                menu_json[day] = menu_dict
            except Exception as e:
                print(f"Error processing menu for {day}: {e}")
                continue

        self.driver.quit()
        return menu_json

def split_span(span: str) -> dict:
    """Take the span text found on the website and split it into a dict.
    The dict should have each day of the week and it's raw contents.
    """
    split_list = {}
    span = span.replace("\n", " ")
    
    for i, day in enumerate(WEEKDAYS):
        day_start = span.find(day)
        if day_start == -1:  # Skip if day is not found
            raise Exception(f"DayNotFoundException: {day} not found in the menu.")
            continue
        next_day_start = (
            span.find(WEEKDAYS[i + 1]) if i + 1 < len(WEEKDAYS) else len(span)
        )
        split_list[day] = span[day_start:next_day_start].strip()

    return split_list
