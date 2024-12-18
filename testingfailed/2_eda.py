import streamlit as st
import pandas as pd
import altair as alt

st.write('# EDA')

@st.cache_data
def load_data():
    return pd.read_csv("movies_complete.csv", parse_dates= ["release_date"])

def show_page():
    st.title("Exploratory Data Analysis (EDA)")
    df = load_data()
    
    # Top Genres by Revenue
    st.header("Top Genres by Revenue")
    genre_revenue = (
        df.explode("genres")  # Split genres into separate rows
        .groupby("genres")["revenue_musd"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(genre_revenue)

    # Correlation between ratings and revenue
    st.header("Ratings vs Revenue")
    scatter_chart = alt.Chart(df).mark_circle().encode(
        x="vote_average",
        y="revenue_musd",
        tooltip=["title", "vote_average", "revenue_musd"],
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)

