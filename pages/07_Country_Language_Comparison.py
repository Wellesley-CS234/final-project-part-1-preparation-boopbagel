import streamlit as st
import pandas as pd
import plotly.express as px


# The actual page content is executed here by Streamlit
st.title("Alisa Zamora: Country/Language Pageview Comparisons")
st.markdown("---")

# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st07_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df1 = st.session_state['student_data']['st07_df']
    df = pd.DataFrame(df1)
    df['date']=pd.to_datetime(df['date'])

    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** This dataset contains **pageview data** for Climate Change articles across all countries and languages represented in the Wikipedia pageview data set from February 2015 thru October 2025.
        
        **Question:** How does engagement in climate change articles vary across languages in given countries?
        
        **Interaction:** Use the selection boxes below to select a country and languages, then and compare views across a chosen date range.
            Only countries with at least 10 entries per month are included.
    """)
    st.markdown("---")
    
    # --- Analysis Controls (Moved from Sidebar to Main Page) ---
    col_country, col_langs, col_dates, = st.columns(3)
    with col_country:
        country_filter = st.selectbox(
            "Select country to analyze:", 
            sorted(df['country'].unique())
        )

    country_df = df[df['country'] == country_filter]
    countries = sorted(country_df['langWiki'].unique())
    with col_langs:
        lang_Choices = st.multiselect(
            "Select language wikipedias to compare:",
            countries,
            default=[countries[0]],
            max_selections=6
        )

    with col_dates:
        dateRange_start = st.date_input(
            "Select a start date:",
            value = '2024-10-06',
            min_value="2023-02-06",
            max_value="2025-10-06"
        )
        dateRange_end = st.date_input(
            "Select an end date:",
            min_value="2023-02-06",
            max_value="2025-10-06"
        )
        
    
    # --- Analysis Content ---
    filtered = df[
        (df['country'] == country_filter) &
        (df['langWiki'].isin(lang_Choices)) &
        (df['date'] >= pd.to_datetime(dateRange_start)) &
        (df['date'] <= pd.to_datetime(dateRange_end))
    ]    
    if filtered.empty:
        st.info(f"No pageview data for '{country_filter}' available.")
    else:
        # --- Weekly Aggregation ---
        weekly = (
        filtered
        .set_index('date')
        .groupby([pd.Grouper(freq='W'), 'langWiki'])['views']
        .sum()
        .reset_index()
    )
        
    # --- Chart ---
        st.subheader("Climate Change Article Views by Language Wiki")
        fig = px.line(
            weekly,
            x="date",
            y="views",
            color="langWiki",
            markers=True,
            title="Weekly Views by Language",
            labels={"date": "Week", "views": "Views"}
        )
        st.plotly_chart(fig, use_container_width=True)