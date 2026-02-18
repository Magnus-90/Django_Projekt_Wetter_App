from django.shortcuts import render
from .apimeteo import get_weather_data # apimeteo skript für Daten
from datetime import datetime
from .models import City
import pytz
# Create your views here.
def home(request):
    return render(request, "home.html")

def weather(request):
    # city_name = 'St.Gallen'
    
    def get_condition_text(code):
        code = int(code)
        if code == 0:
            return "Klar"
        elif code == 2:
            return "Überwiegend Klar"
        elif code == 3:
            return "Teilweise Bewölkt"
        elif code in [45,48]:
            return "Neblig"
        elif code in [51,53,55,61,63,65]:
            return "Regen"
        elif code in [71,73,75,77]:
            return "Schnee"
        elif code in [80,81,82]:
            return "Regen"
        elif code in [95,96,99]:
            return "Gewitter"
        else:
            return "Unbekannt"
        
    weather_data = get_weather_data()

    timezone = pytz.timezone('Europe/Berlin')
    current_hour = datetime.now(timezone).hour
    current_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour]
    current_pressure_hour = weather_data["hourly"]["surface_pressure"][current_hour]
    current_condition_hour = weather_data["hourly"]["weather_code"][current_hour]
    previous_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour - 1]
    temp_diff = current_temperature_hour - previous_temperature_hour
    daily_min_temperature = weather_data["daily"]["temperature_2m_min"][0]
    daily_max_temperature = weather_data["daily"]["temperature_2m_max"][0]
    daily_condition = weather_data['daily_weather_code']

    data ={
        "temp_trend": "up" if temp_diff > 0 else "down",
        "current_condition_text": get_condition_text(current_condition_hour),
        "daily_condition_text": get_condition_text(daily_condition),
        "prev_temp": previous_temperature_hour,
        "current_temp": current_temperature_hour,
        "current_temp": current_temperature_hour,
        "current_pressure": current_pressure_hour,
        "current_condition": current_condition_hour,
        "daily_min_temp": daily_min_temperature,
        "daily_max_temp": daily_max_temperature,
        "coordinates": weather_data["coordinates"],
        "hourly" : weather_data["hourly"],
        "daily": weather_data["daily"],
        "daily_condition": daily_condition
    }
    # return render(request, "weather.html")
    return render(request, "weather.html", data)

def citys(request):
    return render(request, "citys.html")

def userPage(request):
    return render(request, "user_page.html")