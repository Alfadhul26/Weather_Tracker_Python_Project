import streamlit as st
pages = {
    'Weather App': [st.Page("app_pages/0_home_page.py", title="Home", icon="🏠", default = True)],
    'Observations': [st.Page("app_pages/1_record_observations.py",
            title="Record Observations", icon="📝"), 
             st.Page("app_pages/4_view_all_observations.py",
            title="All Observations", icon="📋")],
    'Analysis': [st.Page("app_pages/2_weather_statistics.py",
            title="Weather Statistics", icon="📊"),
    st.Page("app_pages/3_search_by_date.py",
            title="Search by Date", icon="🔎")]}

pg = st.navigation(pages)
pg.run()