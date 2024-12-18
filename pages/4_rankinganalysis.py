import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("movies_complete.csv", parse_dates= ["release_date"])

def show_page():
    st.title("Comparative & Ranking Analysis")
    df = load_data()

    # Top Directors by Revenue
    st.header("Top Directors by Average Revenue")
    top_directors = (
        df.groupby("director")["revenue_musd"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_directors)

    # Top Movies
    st.header("Top 10 Movies by Revenue")
    top_movies = df.nlargest(10, "revenue_musd")[["title", "revenue_musd"]]
    st.table(top_movies)

