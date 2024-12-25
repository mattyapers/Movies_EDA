#TMDB_movie_dataset_app.py

import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(page_title="All-Time Insights", page_icon="📊", layout="wide")
st.title("Movies Data Analysis!")
st.write("Data obtained from https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies, cleaned by me!")


# Load data (same as before, assuming the dataset is already cleaned)
@st.cache_data
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    return df

df = load_data()

# Displaying static insights
def show_static_insights():
    st.header('All-Time Top 10 Insights')

    # Top 10 Highest Budget Movies
    st.subheader('All-Time Top 10 Highest Budget Movies')
    top_budget_movies = df.nlargest(10, 'budget_musd')[['title', 'budget_musd']]

    top_budget_movies_chart = alt.Chart(top_budget_movies).mark_bar().encode(
        x='title:N',
        y='budget_musd:Q',
        color='title:N'
    ).properties(
        title="All-Time Top 10 Highest Budget Movies",
        width=1000,
        height=500
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(top_budget_movies_chart, use_container_width=True)

    # Top 10 Highest Revenue Movies
    st.subheader('All-Time Top 10 Highest Revenue Movies')
    top_revenue_movies = df.nlargest(10, 'revenue_musd')[['title', 'revenue_musd']]

    top_revenue_movies_chart = alt.Chart(top_revenue_movies).mark_bar().encode(
        x='title:N',
        y='revenue_musd:Q',
        color='title:N'
    ).properties(
        title="All-Time Top 10 Highest Revenue Movies",
        width=1000,
        height=500
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(top_revenue_movies_chart, use_container_width=True)

    # Top 10 Highest Profit Movies
    st.subheader('All-Time Top 10 Highest Profit Movies')
    top_profit_movies = df.nlargest(10, 'profit_musd')[['title', 'profit_musd']]

    top_profit_movies_chart = alt.Chart(top_profit_movies).mark_bar().encode(
        x='title:N',
        y='profit_musd:Q',
        color='title:N'
    ).properties(
        title="All-Time Top 10 Highest Profit Movies",
        width=1000,
        height=500
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(top_profit_movies_chart, use_container_width=True)

# Call the function to display static insights
show_static_insights()
