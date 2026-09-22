import streamlit as st
from weather_functions import load_weather_data, record_observation

if st.button("Home", icon="🏠"):
    st.switch_page("app_pages/0_home_page.py")
st.title("Record a New Observation!")

weather_df = load_weather_data()

with st.form("user_observation"):
    date = st.date_input("Enter the date of your weather observation: ", value = "today", format="MM/DD/YYYY")
    temperature = st.number_input("Enter the temperature of your observation (celcius): ")
    condition = st.selectbox("what was the weather condition: ", ("sunny", "cold", "cloudy", "rain", "drizzels", "thunderstorm", "snow", "fog", "windy", "dusty"),)
    st.write("You selected:", condition)
    humidity = st.number_input("what was the humidity percentage: ")
    wind = st.number_input("what was the wind speed (km/h): ")
    submitted = st.form_submit_button("Record observation")

if submitted:
    new_data = record_observation(date, temperature, condition, humidity, wind)
    display_data = new_data.copy()
    display_data["date"] = display_data["date"].dt.strftime("%m/%d/%Y")
    st.success("Data saved successfully!")
    st.table(display_data)