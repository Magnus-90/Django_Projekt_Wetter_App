from django.db import models
from datetime import date

# Create your models here.
class User(models.Model):
    username = models.TextField(max_length=64)
    password = models.TextField(max_length=64)
    createddate = models.DateField(default=date.today)
    def __str__(self):
        return str(self.id) + " " + self.username
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class City(models.Model):
    name = models.TextField(max_length=64)
    country = models.TextField(max_length=64, default="ch")
    latitude = models.TextField(max_length=64)
    longitude =models.TextField(max_length=64)
    plz = models.IntegerField(null=True)
    def __str__(self):
        return str(self.id) + " " + self.name
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Citys"
    
class FavoriteCitys(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_cities")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="favorited_by")
    createddate = models.DateField(default=date.today)
    def __str__(self):
        return f"{self.user.username} {self.city.name}"
    class Meta:
        verbose_name = "Favorite City"
        verbose_name_plural = "Favorite Citys"
    
class LastCitys(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_cities")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="last_by_user")
    vieweddate = models.DateField(default=date.today)
    def __str__(self):
        return f"{self.user.username} {self.city.name}"
    class Meta:
        verbose_name = "Last City"
        verbose_name_plural = "Favorite City"