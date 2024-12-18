import altair as alt
import pandas as pd
import streamlit as st
import re

# Page configuration
st.set_page_config(page_title="Movies Dataset Analysis", page_icon="🎥", layout="wide")

# Load the dataset with caching
@st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["release_date"])
    df['release_date_n'] = df['release_date'].dt.date  # Add formatted date column
    return df

# Function to extract unique genres
def get_unique_genres(genre_column):
    genre_lists = genre_column.dropna().str.split("|")
    unique_genres = set(genre for sublist in genre_lists for genre in sublist)
    return sorted(unique_genres)

# Function to filter the DataFrame based on selected genres
def filter_by_genres(df, selected_genres):
    if selected_genres:
        return df[df['genres'].fillna('').apply(lambda x: all(genre in x for genre in selected_genres))]
    return df

# Function to extract the URL from the img tag
def extract_image_url(img_tag):
    match = re.search(r"src='(.*?)'", img_tag)
    if match:
        return match.group(1)
    return None

# Load dataset
df = load_data("movies_complete.csv")

# Sidebar: Filters
st.sidebar.header("Filter Options")
unique_genres = get_unique_genres(df['genres'])
selected_genres = st.sidebar.multiselect(
    "Select Genres", options=unique_genres, default=None, placeholder="Type to search for genres..."
)
start_year, end_year = st.sidebar.slider(
    "Select Release Year Range",
    min_value=int(df["release_date"].dt.year.min()),
    max_value=int(df["release_date"].dt.year.max()),
    value=(2000, 2020)
)

# Apply filters
filtered_df = df.copy()
filtered_df = filter_by_genres(filtered_df, selected_genres)
filtered_df = filtered_df[
    (filtered_df["release_date"].dt.year >= start_year) &
    (filtered_df["release_date"].dt.year <= end_year)
]

# Title and introduction
st.title("🎥 Movies Dataset Analysis")
st.write(
    """
    Welcome to the Movies Dataset Analysis app! This application explores trends, correlations, and patterns 
    in the movies dataset. Dive into revenue performance, genre analysis, and other movie-related metrics.
    """
)

# Section 1: Dataset Overview
st.header("Dataset Overview")
st.write(f"### Filtered Dataset: {len(filtered_df)} Movies")
st.dataframe(filtered_df[["title", "genres", "release_date_n", "revenue_musd", "vote_average"]].head(10))

# Section 2: Revenue Trends Over Time
st.header("Revenue Trends Over Time")
revenue_trend = (
    filtered_df.groupby(filtered_df["release_date"].dt.year)["revenue_musd"]
    .sum()
    .reset_index()
    .rename(columns={"release_date": "Year", "revenue_musd": "Total Revenue (MUSD)"})
)
revenue_chart = alt.Chart(revenue_trend).mark_line().encode(
    x=alt.X("Year:O", title="Release Year"),
    y=alt.Y("Total Revenue (MUSD):Q", title="Total Revenue (MUSD)"),
    tooltip=["Year", "Total Revenue (MUSD)"]
).properties(width=800, height=400)
st.altair_chart(revenue_chart, use_container_width=True)

# Section 3: Genre Performance
st.header("Genre Performance")
genre_revenue = (
    filtered_df[["genres", "revenue_musd"]]
    .dropna()
    .assign(genres=filtered_df["genres"].str.split('|'))
    .explode("genres")
    .groupby("genres")["revenue_musd"]
    .sum()
    .reset_index()
    .rename(columns={"genres": "Genre", "revenue_musd": "Total Revenue (MUSD)"})
    .sort_values(by="Total Revenue (MUSD)", ascending=False)
)
genre_chart = alt.Chart(genre_revenue).mark_bar().encode(
    x=alt.X("Total Revenue (MUSD):Q", title="Total Revenue (MUSD)"),
    y=alt.Y("Genre:O", sort="-x", title="Genre"),
    tooltip=["Genre", "Total Revenue (MUSD)"]
).properties(width=800, height=400)
st.altair_chart(genre_chart, use_container_width=True)

# Section 4: Ratings vs. Revenue
st.header("Ratings vs. Revenue")
scatter_data = filtered_df[["vote_average", "revenue_musd"]].dropna()
scatter_chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
    x=alt.X("vote_average:Q", title="Average Rating"),
    y=alt.Y("revenue_musd:Q", title="Revenue (MUSD)"),
    tooltip=["vote_average", "revenue_musd"]
).properties(width=800, height=400)
st.altair_chart(scatter_chart, use_container_width=True)

# Section 5: Movies Genre Selector
st.header("🎬 Movies Genre Selector")
if selected_genres:
    st.write(f"Movies matching genres: {', '.join(selected_genres)}")
    for _, row in filtered_df[['title', 'genres', 'poster_path']].head(20).iterrows():
        st.markdown(f"### {row['title']}")
        st.write(f"**Genres:** {row['genres']}")
        poster_url = extract_image_url(row['poster_path'])
        if poster_url:
            st.image(poster_url, width=200, caption=row['title'])
        else:
            st.write("Poster not available.")
        st.write("---")
else:
    st.write("No genres selected.")
