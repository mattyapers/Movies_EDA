import streamlit as st
import pandas as pd
import altair as alt

st.title("📊 Popularity Analysis")

# Load dataset
@st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=["release_date"])
    df['release_year'] = df['release_date'].dt.year
    return df

# Load data
df = load_data("movies_complete.csv")

# Genre Popularity Over Time
st.header("📊 Popularity of Genres Over Time")
genres = df['genres'].str.get_dummies(sep='|')
genres['release_year'] = df['release_year']

genre_trends = genres.groupby('release_year').sum().reset_index()
selected_genres = st.multiselect("Select Genres", options=genre_trends.columns[1:])

if selected_genres:
    genre_chart = alt.Chart(
        genre_trends.melt(id_vars=['release_year'], value_vars=selected_genres)
    ).mark_line().encode(
        x=alt.X("release_year:O", title="Year"),
        y=alt.Y("value:Q", title="Popularity"),
        color="variable:N",
        tooltip=["release_year", "value"]
    ).properties(width=800, height=400)
    st.altair_chart(genre_chart, use_container_width=True)
else:
    st.write("Select genres to view their trends.")


# Actor Popularity Over Time
st.header("🎭 Popularity of Actors Over Time")

# Explode 'cast' column to create individual rows for each actor
actor_data = df['cast'].str.split('|').explode()

# Get the complete list of unique actors
all_actors = sorted([actor for actor in actor_data.dropna().unique() if isinstance(actor, str)])


# Allow user to select multiple actors
selected_actors = st.multiselect(
    "Select Actors", options=all_actors, default=None, placeholder="Type to search for actors..."
)

# Filter data for the selected actors
if selected_actors:
    # Explode 'cast' to create a row for each actor
    exploded_df = df.assign(Actor=df['cast'].str.split('|')).explode('Actor')

    # Filter for selected actors
    filtered_actors = exploded_df[exploded_df['Actor'].isin(selected_actors)]

    # Group by year and actor, then count the number of movies
    actor_trends = (
        filtered_actors.groupby(['release_year', 'Actor'])
        .size()
        .reset_index(name='Movies')
    )

    # Plotting using Altair
    actor_chart = alt.Chart(actor_trends).mark_line().encode(
        x=alt.X("release_year:O", title="Year"),
        y=alt.Y("Movies:Q", title="Number of Movies"),
        color=alt.Color("Actor:N", title="Actor"),
        tooltip=["release_year", "Actor", "Movies"]
    ).properties(width=800, height=400)

    st.altair_chart(actor_chart, use_container_width=True)
else:
    st.write("Select one or more actors to view trends.")

