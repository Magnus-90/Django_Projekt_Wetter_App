from django.shortcuts import render, redirect
from .apimeteo import get_weather_data
from .uv_index_skript import get_uv_index
from .pollen_skript import get_pollen_data
from datetime import datetime
from .models import City, LastCities, FavoriteCities
from django.utils import timezone
from datetime import datetime
import pytz

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
        
    def get_beaufort(wind_kmh):
        if wind_kmh < 1:
            return 0
        elif wind_kmh <= 5:
            return 1
        elif wind_kmh <= 11:
            return 2
        elif wind_kmh <= 19:
            return 3
        elif wind_kmh <= 28:
            return 4
        elif wind_kmh <= 38:
            return 5
        elif wind_kmh <= 49:
            return 6
        elif wind_kmh <= 61:
            return 7
        elif wind_kmh <= 74:
            return 8
        elif wind_kmh <= 88:
            return 9
        elif wind_kmh <= 102:
            return 10
        elif wind_kmh <= 117:
            return 11
        else:
            return 12
        

    def get_uv_category(uv):
        if uv is None:
            return "Keine Daten"
        elif uv < 2:
            return "Niedrig"
        elif uv < 5:
            return "Mittel"
        elif uv < 7:
            return "Hoch"
        elif uv < 10:
            return "Sehr Hoch"
        else:
            return "Extrem"
        
    def get_current_condition(code):
        match code:
            case 0:
                return "clear-day"
            case 1:
                return "cloudy"
            case 2:
                return "partly-cloudy-day"
            case 3:
                return "overcast"
            case 45 | 48:
                return "fog"
            case 51 | 53 | 55 | 61 | 63 | 65 | 80 | 81 | 82:
                return "rain"
            case 71 | 73 | 75 | 77:
                return "snow"
            case 95 | 96 | 99:
                return "thunderstorms"
            case _ :
                return "not-available"
            
    def get_current_alder(pollen_load):
        if pollen_load <= 10:
            return "Schwach"
        elif pollen_load <= 69:
            return "Mässig"
        elif pollen_load <= 249:
            return "Stark"
        else:
            return "Sehr Stark"

    def get_current_birch(pollen_load):
        if pollen_load <= 10:
            return "Schwach"
        elif pollen_load <= 69:
            return "Mässig"
        elif pollen_load <= 299:
            return "Stark"
        else:
            return "Sehr Stark"
        
    def get_current_grass(pollen_load):
        if pollen_load <= 19:
            return "Schwach"
        elif pollen_load <= 29:
            return "Mässig"
        elif pollen_load <= 149:
            return "Stark"
        else:
            return "Sehr Stark"

    def get_current_mugwort(pollen_load):
        if pollen_load <= 5:
            return "Schwach"
        elif pollen_load <= 14:
            return "Mässig"
        elif pollen_load <= 49:
            return "Stark"
        else:
            return "Sehr Stark"

    def get_current_ragweed(pollen_load):
        if pollen_load <= 5:
            return "Schwach"
        elif pollen_load <= 10:
            return "Mässig"
        elif pollen_load <= 39:
            return "Stark"
        else:
            return "Sehr Stark"


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
        except (City.DoesNotExist, IndexError, AttributeError):
            return render(request, "weather.html", {"city_name": city_name, "city_found": False})
        
        weather_data = get_weather_data(latitude, longitude)
        uv_index = get_uv_index(latitude, longitude)
        pollen_data = get_pollen_data(latitude, longitude)
    else:
        return render(request, "weather.html", {"city_name": ""})

    timezone_pytz = pytz.timezone('Europe/Berlin')
    current_hour = datetime.now(timezone_pytz).hour
    pollen_hourly = pollen_data["hourly"]
    alder_pollen = pollen_hourly["alder_pollen"].tolist()
    birch_pollen = pollen_hourly["birch_pollen"].tolist()
    grass_pollen = pollen_hourly["grass_pollen"].tolist()
    mugwort_pollen = pollen_hourly["mugwort_pollen"].tolist()
    ragweed_pollen = pollen_hourly["ragweed_pollen"].tolist()
    current_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour]
    current_pressure_hour = weather_data["hourly"]["surface_pressure"][current_hour]
    current_condition_hour = weather_data["hourly"]["weather_code"][current_hour]
    previous_temperature_hour = weather_data["hourly"]["temperature_2m"][current_hour - 1]
    temp_diff = current_temperature_hour - previous_temperature_hour
    daily_min_temperature = weather_data["daily"]["temperature_2m_min"][0]
    daily_max_temperature = weather_data["daily"]["temperature_2m_max"][0]
    daily_condition = weather_data['daily_weather_code']
    hourly_temps = weather_data["hourly"]["temperature_2m"].tolist()
    hourly_precipitation = weather_data["hourly"]["precipitation"].tolist()
    hourly_wind = weather_data["hourly"]["wind_speed_10m"][current_hour]
    daily_sunrise = weather_data["daily"]["sunrise"][0]
    daily_sunset = weather_data["daily"]["sunset"][0]
    beaufort = get_beaufort(hourly_wind)

    data ={
        "city_name": city_name,
        "temp_trend": "up" if temp_diff > 0 else "down",
        "current_condition_text": get_condition_text(current_condition_hour),
        "daily_condition_text": get_condition_text(daily_condition),
        "condition_icon_hourly": get_current_condition(current_condition_hour),
        "condition_icon_daily": get_current_condition(daily_condition),
        "prev_temp": previous_temperature_hour,
        "current_temp": current_temperature_hour,
        "current_pressure": current_pressure_hour,
        "current_condition": current_condition_hour,
        "daily_min_temp": daily_min_temperature,
        "daily_max_temp": daily_max_temperature,
        "coordinates": weather_data["coordinates"],
        "hourly" : weather_data["hourly"],
        "daily": weather_data["daily"],
        "daily_condition": daily_condition,
        "hourly_temps": hourly_temps,
        "hourly_precipitation": hourly_precipitation,
        "hourly_wind": hourly_wind,
        "sunrise": daily_sunrise,
        "sunset": daily_sunset,
        "beaufort": beaufort,
        "uv_index": uv_index,
        "uv_category": get_uv_category(uv_index),
        "pollen_alder": alder_pollen,
        "pollen_birch": birch_pollen,
        "pollen_grass": grass_pollen,
        "pollen_mugwort": mugwort_pollen,
        "pollen_ragweed": ragweed_pollen,
        "current_pollen_alder": get_current_alder(alder_pollen[current_hour]),
        "current_pollen_birch": get_current_birch(birch_pollen[current_hour]),
        "current_pollen_grass": get_current_grass(grass_pollen[current_hour]),
        "current_pollen_mugwort": get_current_mugwort(mugwort_pollen[current_hour]),
        "current_pollen_ragweed": get_current_ragweed(ragweed_pollen[current_hour])
    }
    return render(request, "weather.html", data)

def cities(request):
    search = request.GET.get("city","")
    if search:
        cities = City.objects.filter(name__icontains=search)
    else:
        cities = City.objects.all()
    return render(request, "cities.html", {"cities": cities, "search": search})
        

def userPage(request):
    return render(request, "user_page.html")