import streamlit as st
from weather_functions import load_weather_data, calculate_weather_statistics, load_historical_weather_data, find_previous_year_temperature

if st.button("Home", icon="🏠"):
    st.switch_page("app_pages/0_home_page.py")
st.title("View Weather Statistics")

weather_df = load_weather_data()
historical_df = load_historical_weather_data()

statistics = calculate_weather_statistics(weather_df)

col1, col2 = st.columns(2, border=True)
col1.metric("Average Temperature", statistics["average_temperature"])
col2.metric("Minimum Temperature", statistics["minimum_temperature"])

col3, col4 = st.columns(2, border=True)
col3.metric("Most Commonly Recorded Weather Condition", statistics["most_common_condition"])
col4.metric("Maximum Temperature", statistics["maximum_temperature"])

st.subheader("Compare temperature with last year")
selected_date = st.date_input("Select a date to compare with the same date last year:", value="today", format="MM/DD/YYYY")
previous_year_temperature = find_previous_year_temperature(historical_df, selected_date)
if previous_year_temperature is None:
    st.warning("No historical temperature was found for this date.")
else:
    display_data = previous_year_temperature.copy()
    display_data["date"] = display_data["date"].dt.strftime("%m/%d/%Y")
    st.dataframe(display_data)

st.subheader("Temperature Trend")
st.line_chart(weather_df, x = 'date', y = 'temperature', x_label="Date", y_label="Temperature")