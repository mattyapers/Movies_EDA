import streamlit as st
import pandas as pd
import altair as alt

# Page configuration for dynamic insights
st.set_page_config(page_title="Dynamic Insights", page_icon="📊")

# Load data (assuming cleaned dataset is already available)
@st.cache_data
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    return df

df = load_data()

def show_dynamic_insights():
    st.title('Dynamic Movie Insights')

    # Filter data by release year
    release_year = st.slider('Select Release Year', min_value=1980, max_value=2024, value=(1980, 2024), step=1)
    filtered_df = df[(df['release_year'] >= release_year[0]) & (df['release_year'] <= release_year[1])]

    # Genre and Language Selections
    options = df['genres'].str.split(",").explode().unique()
    selected_genres = st.multiselect('Select Genres', options=options, default=None)
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: all(genre in x for genre in selected_genres))]

    language_options = df['original_language'].unique()
    selected_languages = st.multiselect('Select Languages', options=language_options, default=None)
    if selected_languages:
        filtered_df = filtered_df[filtered_df['original_language'].isin(selected_languages)]

    # Display filtered data for debugging purposes (optional)
    st.write(f"Filtered data from {release_year[0]} to {release_year[1]}:")
    st.write(filtered_df.head())

# Display dynamic insights on page load
show_dynamic_insights()
