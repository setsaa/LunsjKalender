from google_calendar import GCal
from webscraper import scrape_menu
from datetime import datetime, timedelta

calendar_api = GCal()

def add_menu_to_cal():
    menu_json = scrape_menu()
    print(menu_json)

    for day, menu in menu_json.items():
        calendar_api.create_event(
            summary=menu["Dagens"],
            description=f"Dagens: {menu['Dagens']}\nVegetar: {menu['Vegetar dagens']}\nSuppe: {menu['Suppe']}",
            start_time=get_day_date(day, hour=11, minute=00),
            end_time=get_day_date(day, hour=11, minute=30)
        )

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
