import streamlit as st
import pandas as pd

st.write('# Genre Analysis')


@st.cache_data
def load_data():
    return pd.read_csv("movies_complete.csv", parse_dates= ["release_date"])

def show_page():
    st.title("Genre & Popularity Analysis")
    df = load_data()

    # Filter by Genre
    genres = sorted(set("|".join(df["genres"].dropna()).split("|")))
    selected_genres = st.multiselect("Select Genres", genres)

    if selected_genres:
        filtered_df = df[
            df["genres"].fillna("").apply(lambda x: all(g in x for g in selected_genres))
        ]
        st.write(f"Movies matching genres: {', '.join(selected_genres)}")
        st.dataframe(filtered_df[["title", "genres"]].head(10))
    else:
        st.write("No genres selected. Please choose from the list.")

