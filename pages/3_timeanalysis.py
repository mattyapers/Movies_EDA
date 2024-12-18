import streamlit as st
import pandas as pd
import altair as alt

st.write('# Time Analysis')

@st.cache_data
def load_data():
    return pd.read_csv("movies_complete.csv", parse_dates= ["release_date"])

def show_page():
    st.title("Time-based Analysis")
    df = load_data()

    # Revenue Over Time
    st.header("Movie Revenue Over Time")
    revenue_trend = (
        df.groupby("release_year")["revenue_musd"]
        .mean()
        .reset_index()
    )
    line_chart = alt.Chart(revenue_trend).mark_line().encode(
        x="release_year",
        y="revenue_musd",
    )
    st.altair_chart(line_chart, use_container_width=True)

    # Popular Genres Over Time
    st.header("Popular Genres Over Time")
    df["release_year"] = pd.to_datetime(df["release_date"]).dt.year
    genre_popularity = (
        df.explode("genres")
        .groupby(["release_year", "genres"])["popularity"]
        .mean()
        .reset_index()
    )
    heatmap = alt.Chart(genre_popularity).mark_rect().encode(
        x="release_year:O",
        y="genres:O",
        color="popularity:Q",
    )
    st.altair_chart(heatmap, use_container_width=True)

