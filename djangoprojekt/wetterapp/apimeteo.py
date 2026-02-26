import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

def get_weather_data(latitude, longitude):
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max"],
		"hourly": ["temperature_2m", "weather_code", "surface_pressure", "precipitation", "wind_speed_10m"],
		"models": "meteoswiss_icon_ch1",
		"timezone": "Europe/Berlin",
		"forecast_days": 1,
	}
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
	hourly_surface_pressure = hourly.Variables(2).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["weather_code"] = hourly_weather_code
	hourly_data["surface_pressure"] = hourly_surface_pressure
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	print("\nHourly data\n", hourly_dataframe)

	daily = response.Daily()
	daily_weather_code = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
	daily_sunrise = pd.to_datetime(
    	daily.Variables(3).ValuesInt64AsNumpy(),
    	unit="s",
    	utc=True
	)

	daily_sunset = pd.to_datetime(
    	daily.Variables(4).ValuesInt64AsNumpy(),
    	unit="s",
    	utc=True
	)
	daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()
	daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()
	daily_uv_index_max = daily.Variables(7).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}

	daily_data["weather_code"] = daily_weather_code
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["sunrise"] = daily_sunrise
	daily_data["sunset"] = daily_sunset
	daily_data["daylight_duration"] = daily_daylight_duration
	daily_data["sunshine_duration"] = daily_sunshine_duration
	daily_data["uv_index_max"] = daily_uv_index_max

	daily_dataframe = pd.DataFrame(data = daily_data)
	print("\Daily data\n", daily_dataframe)
	return {
        'coordinates': {
            'latitude': response.Latitude(),
            'longitude': response.Longitude(),
            'elevation': response.Elevation()
        },
        'hourly': hourly_dataframe,
        'daily': daily_dataframe,
		'daily_weather_code': int(daily_weather_code[0]),
    }