from django.db import models
from datetime import date

# Create your models here.
class User(models.Model):
    username = models.TextField(max_length=64)
    password = models.TextField(max_length=64)
    def __str__(self):
        return str(self.id) + " " + self.username

class City(models.Model):
    name = models.TextField(max_length=64)
    country = models.TextField(max_length=64)
    latitude = models.TextField(max_length=64)
    longitude =models.TextField(max_length=64)
    def __str__(self):
        return str(self.id) + " " + self.name
    
class FavoriteCities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_cities")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="favorited_by")
    def __str__(self):
        return f"{self.user.username} {self.city.name}"
    
class LastCities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_cities")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="last_by_user")
    date = models.DateField(default=date.today)
    def __str__(self):
        return f"{self.user.username} {self.city.name}"