from django.shortcuts import render
from .apimeteo import get_weather_data # apimeteo skript für Daten
from datetime import datetime
import pytz
# Create your views here.
def home(request):
    return render(request, "home.html")

def weather(request):
    # city_name = 'St.Gallen'
    weather_data = get_weather_data()

    timezone = pytz.timezone('Europe/Berlin')
    current_hour = datetime.now(timezone).hour
    current_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour]
    current_pressure_hour = weather_data["hourly"]["surface_pressure"][current_hour]
    current_condition_hour = weather_data["hourly"]["weather_code"][current_hour]
    daily_min_temperature = weather_data["daily"]["temperature_2m_min"][0]
    daily_max_temperature = weather_data["daily"]["temperature_2m_max"][0]

    data ={
        "current_temp": current_temperature_hour,
        "current_pressure": current_pressure_hour,
        "current_condition": current_condition_hour,
        "daily_min_temp": daily_min_temperature,
        "daily_max_temp": daily_max_temperature,
        "coordinates": weather_data["coordinates"],
        "hourly" : weather_data["hourly"],
        "daily": weather_data["daily"]
    }
    # return render(request, "weather.html")
    return render(request, "weather.html", data)

def citys(request):
    return render(request, "citys.html")

def userPage(request):
    return render(request, "user_page.html")