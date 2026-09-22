import streamlit as st
from weather_functions import (fetch_weather_forecast, calculate_today_average, calculate_tomorrow_average, get_llm_weather_summary)

st.title("Welcome to Weather Tracker!")
st.subheader("How does it feel today?")

forecast_df = fetch_weather_forecast()
today_average = calculate_today_average(forecast_df)
tomorrow_average = calculate_tomorrow_average(forecast_df)

col1, col2 = st.columns(2, gap="xsmall", border=True)
col1.metric("Today's Average Temperature",f"{today_average} °C")
col2.metric("Tomorrow's Average Temperature", f"{tomorrow_average} °C")

st.subheader("What would you like to do?")
col1, col2 = st.columns(2, gap="xsmall", border=True)
with col1:
    st.page_link("app_pages/1_record_observations.py", label="Record Observations", icon="📝")
    st.write("Add a new weather observation")
with col2:
    st.page_link("app_pages/4_view_all_observations.py", label="View All Observations", icon="📋")
    st.write("View all recorded weather observations")

col3, col4 = st.columns(2, gap="xsmall", border=True)
with col3:
    st.page_link("app_pages/3_search_by_date.py", label="Search by Date", icon="🔎")
    st.write("Find observations from a specific date")
with col4:
    st.page_link("app_pages/2_weather_statistics.py", label="Weather Statistics", icon="📊")
    st.write("Explore statistics from your weather data")

st.subheader("LLM Weather Summary")
st.write("Starting LLM request...")
weather_summary = get_llm_weather_summary()
st.write(weather_summary)

