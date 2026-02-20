"""
URL configuration for dangoprojekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wetterapp.views import home, weather, cities, userPage
from django.urls import path, include
from wetterapp.views import home, weather, cities, userPage, add_favorite, remove_favorite

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path("weather/", weather, name="weather"),
    path("cities/", cities, name="cities"),
    path("userpage/", userPage, name="userpage"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("cities/favorites/<int:city_id>/", add_favorite, name="add_favorite"),
    path("cities/favorites/remove/<int:city_id>/", remove_favorite, name="remove_favorite")
]
