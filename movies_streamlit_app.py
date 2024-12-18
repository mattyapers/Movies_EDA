import altair as alt
import pandas as pd
import streamlit as st
from IPython.display import HTML
import re

# Page configuration
st.set_page_config(page_title="Movies Dataset Analysis", page_icon="🎥", layout="wide")

# Load the dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv("movies_complete.csv", parse_dates=["release_date"])
    return df

# Load the dataset
df = load_data()

df['release_date_n'] = df['release_date'].dt.date

# Title and introduction
st.title("🎥 Movies Dataset Analysis")
st.write("""
Welcome to the Movies Dataset Analysis app! This application explores trends, correlations, and patterns 
in the movies dataset. Dive into revenue performance, genre analysis, and other movie-related metrics.
""")

# Display the first 5 rows of the dataset
st.write("### Preview of the Dataset")
st.write(df.head(5))

# Sidebar: Filters
st.sidebar.header("Filter Options")
selected_genres = st.sidebar.multiselect(
    "Select Genres", 
    options=df["genres"].dropna().str.split('|').explode().unique(),
    default=None
)
start_year, end_year = st.sidebar.slider(
    "Select Release Year Range",
    min_value=int(df["release_date"].dt.year.min()),
    max_value=int(df["release_date"].dt.year.max()),
    value=(2000, 2020)
)

# Apply filters
filtered_df = df.copy()
if selected_genres:
    filtered_df = filtered_df[filtered_df["genres"].fillna("").apply(
        lambda x: all(genre in x for genre in selected_genres)
    )]
filtered_df = filtered_df[
    (filtered_df["release_date"].dt.year >= start_year) &
    (filtered_df["release_date"].dt.year <= end_year)
]

# Section 1: Overview
st.header("Dataset Overview")
st.write(f"Filtered Dataset: {len(filtered_df)} movies")
st.dataframe(filtered_df[["title", "genres", "release_date_n", "revenue_musd", "vote_average"]].head(10))

# Section 2: Revenue Trends
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
).properties(
    width=800,
    height=400
)
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
).properties(
    width=800,
    height=400
)
st.altair_chart(genre_chart, use_container_width=True)

# Section 4: Ratings vs. Revenue
st.header("Ratings vs. Revenue")
scatter_data = filtered_df[["vote_average", "revenue_musd"]].dropna()
scatter_chart = alt.Chart(scatter_data).mark_circle(size=60).encode(
    x=alt.X("vote_average:Q", title="Average Rating"),
    y=alt.Y("revenue_musd:Q", title="Revenue (MUSD)"),
    tooltip=["vote_average", "revenue_musd"]
).properties(
    width=800,
    height=400
)
st.altair_chart(scatter_chart, use_container_width=True)



# 1. Comparative and Ranking Analysis
st.header("Comparative and Ranking Analysis")

# Which director has the highest average revenue per movie?
director_revenue = (
    df.groupby("director")["revenue_musd"].mean().sort_values(ascending=False).head(10).reset_index()
)
st.subheader("Top 10 Directors by Average Revenue")
st.altair_chart(
    alt.Chart(director_revenue)
    .mark_bar()
    .encode(
        x=alt.X("revenue_musd", title="Average Revenue (Million USD)"),
        y=alt.Y("director", sort="-x", title="Director"),
        tooltip=["director", "revenue_musd"]
    )
    .properties(height=400),
    use_container_width=True
)

# What are the top 10 movies based on revenue and popularity?
st.subheader("Top 10 Movies by Revenue and Popularity")
top_movies = df.sort_values(["revenue_musd", "popularity"], ascending=[False, False]).head(10)
st.write(top_movies[["title", "revenue_musd", "popularity"]])

# Which actors, directors, or franchises consistently produce the highest-grossing movies?
st.subheader("Actors and Franchises with the Highest Average Revenue")
actors_revenue = (
    df["cast"].str.split('|', expand=True).stack()
    .reset_index(level=1, drop=True).to_frame("actor")
    .merge(df[["revenue_musd"]], left_index=True, right_index=True)
    .groupby("actor")["revenue_musd"].mean().sort_values(ascending=False).head(10)
    .reset_index()
)
st.altair_chart(
    alt.Chart(actors_revenue)
    .mark_bar()
    .encode(
        x=alt.X("revenue_musd", title="Average Revenue (Million USD)"),
        y=alt.Y("actor", sort="-x", title="Actor"),
        tooltip=["actor", "revenue_musd"]
    )
    .properties(height=400),
    use_container_width=True
)

# 2. Genre and Popularity Analysis
st.header("Genre and Popularity Analysis")

# How does movie genre correlate with box office success?
st.subheader("Movie Genre vs Box Office Success")
genre_revenue = (
    df["genres"].str.split('|', expand=True).stack()
    .reset_index(level=1, drop=True).to_frame("genre")
    .merge(df[["revenue_musd"]], left_index=True, right_index=True)
    .groupby("genre")["revenue_musd"].mean().sort_values(ascending=False).reset_index()
)
st.altair_chart(
    alt.Chart(genre_revenue)
    .mark_bar()
    .encode(
        x=alt.X("revenue_musd", title="Average Revenue (Million USD)"),
        y=alt.Y("genre", sort="-x", title="Genre"),
        tooltip=["genre", "revenue_musd"]
    )
    .properties(height=400),
    use_container_width=True
)

# Which genre has the highest average revenue per movie?
st.write("\nThe table below shows the average revenue for each genre:")
st.write(genre_revenue)

# How does the popularity of certain genres evolve over time?
st.subheader("Genre Popularity Over Time")
genre_popularity = (
    df["genres"].str.split('|', expand=True).stack()
    .reset_index(level=1, drop=True).to_frame("genre")
    .merge(df[["release_date", "popularity"]], left_index=True, right_index=True)
    .groupby(["release_date", "genre"])["popularity"].mean().reset_index()
)
st.altair_chart(
    alt.Chart(genre_popularity)
    .mark_line()
    .encode(
        x=alt.X("release_date:T", title="Year"),
        y=alt.Y("popularity", title="Average Popularity"),
        color="genre",
        tooltip=["release_date", "genre", "popularity"]
    )
    .properties(height=400),
    use_container_width=True
)


# Extract and clean the genres
def get_unique_genres(genre_column):
    genre = genre_column.dropna().str.split("|")
    unique_genres = set(genre for sublist in genre for genre in sublist)
    return sorted(unique_genres)

# Get unique genres
unique_genres = get_unique_genres(df['genres'])

# Function to extract the URL from the img tag
def extract_image_url(img_tag):
    match = re.search(r"src='(.*?)'", img_tag)
    if match:
        return match.group(1)
    return None


# Multi-select widget
st.title("🎬 Movies Genre Selector")
st.write("Select one or more genres from the list:")

selected_genres = st.multiselect(
    "Choose genres:",
    options=unique_genres,
    placeholder="Type to search for a genre..."
)


# Filter the DataFrame based on selected genres
if selected_genres:
    # Drop NaN or replace them with empty strings before applying the check
    filtered_df = df[df['genres'].fillna('').apply(lambda x: all(genre in x for genre in selected_genres))]
    
    st.write(f"Movies matching genres: {', '.join(selected_genres)}")

    # Display movie details with poster images
    for index, row in filtered_df[['title', 'genres', 'poster_path']].head(20).iterrows():
        st.markdown(f"### {row['title']}")
        st.write(f"**Genres:** {row['genres']}")
        
        # Extract the URL from the poster_path HTML tag
        poster_url = extract_image_url(row['poster_path'])
        if poster_url:
            st.image(poster_url, width=200, caption=row['title'])  # Display the poster image
        else:
            st.write("Poster not available.")
        
        st.write("---")  # Add a separator
else:
    st.write("No genres selected. Please choose from the list.")