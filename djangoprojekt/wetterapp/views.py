from django.shortcuts import render, redirect
from .apimeteo import get_weather_data # apimeteo skript für Daten
from datetime import datetime
from .models import City, LastCities, FavoriteCities
from django.utils import timezone
import pytz
# Create your views here.

def add_favorite(request, city_id):
    if request.method == "POST" and request.user.is_authenticated:
        city = City.objects.get(id=city_id)
        FavoriteCities.objects.get_or_create(
            user=request.user,
            city=city,
            defaults={"username": request.user.username}
        )
    return redirect("cities")

def remove_favorite(request, city_id):
    if request.method == "POST" and request.user.is_authenticated:
        city = City.objects.get(id=city_id)
        FavoriteCities.objects.filter(
            user=request.user,
            city=city
        ).delete()
    return redirect("cities")

def home(request):
    if request.user.is_authenticated:
        last_cities = LastCities.objects.filter(user=request.user).order_by("-vieweddate")[:5]
        favorite_cities = FavoriteCities.objects.filter(user=request.user)
    else:
        favorite_cities = []
        last_cities = []
    return render(request, "home.html", {"last_cities": last_cities, "favorite_cities": favorite_cities})

def weather(request):

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
        

    city_name = request.GET.get("city","")

    if city_name:
        try:
            ort = City.objects.filter(name__iexact=city_name).first()
            latitude = ort.latitude
            longitude = ort.longitude
            if request.user.is_authenticated:
                LastCities.objects.update_or_create(
                user=request.user,
                city=ort,
                defaults={
                    "vieweddate": timezone.now(),
                    "username": request.user.username
                }
            )
        except (City.DoesNotExist, IndexError):
            return render(request, "weather.html", {"city_name": city_name, "city_found": False})
        
        weather_data = get_weather_data(latitude, longitude)
    else:
        return render(request, "weather.html", {"city_name": ""})

    timezone_pytz = pytz.timezone('Europe/Berlin')
    current_hour = datetime.now(timezone_pytz).hour
    current_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour]
    current_pressure_hour = weather_data["hourly"]["surface_pressure"][current_hour]
    current_condition_hour = weather_data["hourly"]["weather_code"][current_hour]
    previous_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour - 1]
    temp_diff = current_temperature_hour - previous_temperature_hour
    daily_min_temperature = weather_data["daily"]["temperature_2m_min"][0]
    daily_max_temperature = weather_data["daily"]["temperature_2m_max"][0]
    daily_condition = weather_data['daily_weather_code']

    data ={
        "city_name": city_name,
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
    return render(request, "weather.html", data)

def cities(request):
    cities = City.objects.all()
    return render(request, "cities.html", {"cities": cities})

def userPage(request):
    return render(request, "user_page.html")