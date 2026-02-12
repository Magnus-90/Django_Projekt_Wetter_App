from django.shortcuts import render
from .apimeteo import get_weather_data # apimeteo skript für Daten
# Create your views here.
def home(request):
    return render(request, "home.html")

def weather(request):
    return render(request, "weather.html")

def citys(request):
    return render(request, "citys.html")

def userPage(request):
    return render(request, "user_page.html")