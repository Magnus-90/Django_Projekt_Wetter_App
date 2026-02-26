import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

def get_pollen_data(latitude, longitude):
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
    	"latitude": latitude,
    	"longitude": longitude,
    	"hourly": ["alder_pollen", "birch_pollen", "grass_pollen", "mugwort_pollen", "ragweed_pollen"],
    	"forecast_days": 1,
    	"domains": "cams_europe",
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    hourly = response.Hourly()
    hourly_alder_pollen = hourly.Variables(0).ValuesAsNumpy()
    hourly_birch_pollen = hourly.Variables(1).ValuesAsNumpy()
    hourly_grass_pollen = hourly.Variables(2).ValuesAsNumpy()
    hourly_mugwort_pollen = hourly.Variables(3).ValuesAsNumpy()
    hourly_ragweed_pollen = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
    	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}

    hourly_data["alder_pollen"] = hourly_alder_pollen
    hourly_data["birch_pollen"] = hourly_birch_pollen
    hourly_data["grass_pollen"] = hourly_grass_pollen
    hourly_data["mugwort_pollen"] = hourly_mugwort_pollen
    hourly_data["ragweed_pollen"] = hourly_ragweed_pollen

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    # print("\nHourly data\n", hourly_dataframe)
    return {
        'coordinates': {
            'latitude': response.Latitude(),
            'longitude': response.Longitude(),
            'elevation': response.Elevation()
        },
        'hourly': hourly_dataframe,
    }