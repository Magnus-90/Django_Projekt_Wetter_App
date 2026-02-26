import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

def get_uv_index(latitude, longitude):
	cache_session = requests_cache.CachedSession('.cache_uv', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": latitude,
		"longitude": longitude,
		"daily": ["uv_index_max"],
		"timezone": "Europe/Berlin",
		"forecast_days": 1,
	}
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	daily = response.Daily()
	daily_uv_index_max = daily.Variables(0).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["uv_index_max"] = daily_uv_index_max

	daily_dataframe = pd.DataFrame(data = daily_data)
	print("\Daily data\n", daily_dataframe)
	return float(daily_uv_index_max[0])