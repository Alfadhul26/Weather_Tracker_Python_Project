import streamlit as st
import pandas as pd

from weather_functions import load_weather_data, filter_observations_by_month, filter_observations_by_season

if st.button("Home", icon="🏠"):
    st.switch_page("app_pages/0_home_page.py")
st.title("View All Observations")

weather_df = load_weather_data ()
filter_by = st.selectbox("Filter Observations by:", ["None", "Month", "Season"])

if filter_by == "Month":
    selected_month = st.selectbox("Select a month:",["January", "February", "March", "April","May", "June", "July", "August", "September", "October", "November", "December"])
    month_number = pd.to_datetime(selected_month, format="%B").month
    filtered_df = filter_observations_by_month(weather_df, month_number)

elif filter_by == "Season":
    selected_season = st.selectbox("Select a season:",["Winter", "Spring", "Summer", "Autumn"])
    filtered_df = filter_observations_by_season(weather_df, selected_season)


if filter_by in ["Month", "Season"]:
    display_df = filtered_df.copy()
else:
    display_df = weather_df.copy()

display_df["date"] = display_df["date"].dt.strftime("%m-%d-%Y")
st.dataframe(display_df)