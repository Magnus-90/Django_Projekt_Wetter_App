from django.contrib import admin
from .models import City, FavoriteCities, LastCities
# Register your models here.
# admin.site.register(User)
admin.site.register(City)
admin.site.register(FavoriteCities)
admin.site.register(LastCities)