import streamlit as st
from weather_functions import (load_weather_data, search_observations_by_date)

if st.button("Home", icon="🏠"):
    st.switch_page("app_pages/0_home_page.py")
st.title("Search Observations By Date")

weather_df = load_weather_data()
date = st.date_input("Enter the date: ", value="today", format="MM/DD/YYYY")
search_date = date
st.write(date.strftime("%m/%d/%Y"))
search_results = search_observations_by_date( weather_df, search_date)

display_results = search_results.copy()
display_results["date"] = display_results["date"].dt.strftime("%m/%d/%Y")
st.dataframe(display_results)