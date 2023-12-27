import os
import requests
from datetime import datetime, timedelta

def get_weather_description_and_temps(forecast):
    weather_description = forecast['weather'][0]['description']
    temp_min = round(forecast["main"]["temp_min"] - 273.15, 2)
    temp_max = round(forecast["main"]["temp_max"] - 273.15, 2)
    return weather_description, temp_min, temp_max

def get_chance_of_precipitation(forecast):
    return forecast.get('pop', 0) * 100

API_KEY = "Api key"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

city = input("Enter a city name: ")


weather_response = requests.get(f"{WEATHER_URL}?appid={API_KEY}&q={city}")
if weather_response.status_code == 200:
    current_data = weather_response.json()
    current_weather, _, current_temp = get_weather_description_and_temps(current_data)
    print(f"Current weather in {city}: {current_weather}, {current_temp}°C")
else:
    print("An error occurred while fetching the current weather.")


forecast_response = requests.get(f"{FORECAST_URL}?appid={API_KEY}&q={city}")
if forecast_response.status_code == 200:
    forecast_data = forecast_response.json()
    
    today_date = datetime.now().date()

    
    today_forecast = None
    tomorrow_forecast = None
    tomorrow_date = today_date + timedelta(days=1)
    for forecast in forecast_data['list']:
        forecast_time = datetime.fromtimestamp(forecast['dt'])
        if forecast_time.date() == today_date and not today_forecast:
            today_forecast = forecast
        if forecast_time.date() == tomorrow_date:
            tomorrow_forecast = forecast
            break

    
    if today_forecast:
        weather, temp_min, temp_max = get_weather_description_and_temps(today_forecast)
        pop = get_chance_of_precipitation(today_forecast)
        print(f"Today's forecast: {weather}")
        print(f"High of {temp_max}°C, low of {temp_min}°C")
        print(f"Chance of precipitation: {pop}%")
    else:
        print("No forecast data available for today.")

    
    if tomorrow_forecast:
        weather, temp_min, temp_max = get_weather_description_and_temps(tomorrow_forecast)
        pop = get_chance_of_precipitation(tomorrow_forecast)
        print(f"Tomorrow's forecast: {weather}")
        print(f"High of {temp_max}°C, low of {temp_min}°C")
        print(f"Chance of precipitation: {pop}%")
    else:
        print("No forecast data available for tomorrow.")
else:
    print("An error occurred while fetching the forecast.")
