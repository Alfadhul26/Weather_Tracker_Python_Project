import requests
import pandas as pd
from datetime import date, timedelta
from openai import OpenAI

def load_weather_data():
    """This function reads the dataset in .csv file"""
    return pd.read_csv("weather_tracker.csv", parse_dates=['date'])
    

def record_observation(date, temperature, condition, humidity, wind):
    """This function records new weather observations from the user and stores them to the dataset in .csv file"""
    weather_df = load_weather_data()
    new_data = pd.DataFrame([{"date": pd.to_datetime(date), "temperature": temperature, "weather_conditions": condition, "humidity_percentage": humidity, "wind_speed": wind}])
    weather_df = pd.concat([weather_df, new_data])
    weather_df.to_csv("weather_tracker.csv", index=False)
    return new_data


def calculate_weather_statistics(weather_df):
    return {
        "average_temperature": round(weather_df["temperature"].mean(), 2),
        "minimum_temperature": weather_df["temperature"].min(),
        "maximum_temperature": weather_df["temperature"].max(),
        "most_common_condition": weather_df["weather_conditions"].value_counts().idxmax()}


def search_observations_by_date(weather_df, search_date):
    """Return weather observations recorded on a specific date."""
    return weather_df[weather_df["date"].dt.date == search_date]


def filter_observations_by_month(weather_df, month_number):
    """Return weather observations recorded in a specific month."""
    return weather_df[weather_df["date"].dt.month == month_number]


def filter_observations_by_season(weather_df, selected_season):
    """Return weather observations recorded in a specific season."""
    season_months = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Autumn": [9, 10, 11]}
    return weather_df[weather_df["date"].dt.month.isin(season_months[selected_season])]

def fetch_historical_weather():
    """Fetch historical daily weather data from the Meteostat API."""
    url = "https://meteostat.p.rapidapi.com/point/daily"
    querystring = {"units": "metric","model": "true","alt": "184","lon": "50.5870","lat": "26.2235", "start": "2025-01-01","end": "2026-09-19"}
    headers = {"x-rapidapi-key": "meteostat-key","x-rapidapi-host": "meteostat.p.rapidapi.com"}

    history = requests.get(url,headers=headers,params=querystring)
    h_df = pd.json_normalize(history.json()["data"])
    history_df = pd.DataFrame({"date": h_df["date"],"temperature": h_df["tavg"]})
    history_df["date"] = pd.to_datetime(history_df["date"])
    history_df.to_csv("historical_weather.csv",index=False)
    return history_df


def load_historical_weather_data():
    """Load historical weather data from the historical CSV file."""
    return pd.read_csv("historical_weather.csv",parse_dates=["date"])


def find_previous_year_temperature(historical_df,selected_date):
    """Find the weather observation recorded on the same date one year earlier."""
    previous_year_date = selected_date.replace(year=selected_date.year - 1)
    result = historical_df[historical_df["date"].dt.date == previous_year_date]
    if result.empty:
        return None
    return result
    
def fetch_weather_forecast():
    url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
    querystring = {"lang": "EN","longitude": "50.5870","latitude": "26.2235"}
    headers = {"x-rapidapi-key": "open_weather_key","x-rapidapi-host": "open-weather13.p.rapidapi.com"}
    response = requests.get(url,headers=headers,params=querystring)
    forecast_data = response.json()
    forecast_df = pd.json_normalize(forecast_data["list"])[["dt_txt", "main.temp"]]
    forecast_df["temperature"] = (forecast_df["main.temp"] - 273.15)
    forecast_df = forecast_df.rename(columns={"dt_txt": "date"})
    forecast_df = forecast_df[["date", "temperature"]]
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])
    return forecast_df


def calculate_today_average(forecast_df):
    today = date.today()
    today_forecast = forecast_df[forecast_df["date"].dt.date == today]
    today_average_temperature = round(today_forecast["temperature"].mean(),2)
    return today_average_temperature


def calculate_tomorrow_average(forecast_df):
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_forecast = forecast_df[forecast_df["date"].dt.date == tomorrow]
    tomorrow_average_temperature = round(tomorrow_forecast["temperature"].mean(),2)
    return tomorrow_average_temperature

def get_llm_weather_summary():
    weather = load_weather_data()
    last_7_days = (weather.sort_values("date").tail(7))
    weather_data = last_7_days.to_string(index=False)
    prompt = f"""
You are analyzing recent weather conditions.
Here is the weather data from the past 7 days:
{weather_data}
Based on this data:
Give a concise response with exactly 4 bullet points:
- Weather pattern
- Clothing
- Outdoor activity recommendations in bahrain
- Weather consideration

Keep each bullet to one sentence. Do not provide explanations or extra information.
"""
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="llm_key")
    completion = client.chat.completions.create(
        model="inclusionai/ling-3.0-flash-vl:free",
        messages=[{"role": "system", "content": "You are a meteorologist who provides practical weather advice for bahrain."},
            {"role": "user", "content": prompt}],temperature=0.0)
    return completion.choices[0].message.content