from django.contrib import admin
from .models import City, FavoriteCities, LastCities
admin.site.register(City)
admin.site.register(FavoriteCities)
admin.site.register(LastCities)