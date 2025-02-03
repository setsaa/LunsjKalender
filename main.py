from google_calendar import GCal
from webscraper import WebScraper
from datetime import datetime, timedelta
import sys

START_TIME = (11, 00)
END_TIME   = (11, 30)

calendar_api = GCal()
scraper = WebScraper()

def add_menu_to_cal():
    try:
        menu_json = WebScraper.scrape_menu()
        print("Fetched menu:", menu_json)

        for day, menu in menu_json.items():
            try:
                calendar_api.create_event(
                    summary=menu["Dagens"],
                    description=f"Dagens: {menu['Dagens']}\nVegetar: {menu['Vegetar dagens']}\nSuppe: {menu['Suppe']}",
                    start_time=get_day_date(day, hour=START_TIME[0], minute=START_TIME[1]),
                    end_time=get_day_date(day, hour=END_TIME[0], minute=END_TIME[1])
                )
                print(f"Event created for {day}.")
            except Exception as e:
                print(f"Failed to create event for {day}: {e}")
    
    except Exception as e:
        print(f"Error fetcing menu: {e}")
        sys.exit(1)

def get_day_date(day_name, hour, minute):
    days_of_week = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
    today = datetime.today()
    target_day = days_of_week.index(day_name.lower())
    days_until_target = (target_day - today.weekday()) % 7
    target_date = today + timedelta(days=days_until_target)
    target_datetime = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return target_datetime.isoformat()

if __name__ == "__main__":
    add_menu_to_cal()
