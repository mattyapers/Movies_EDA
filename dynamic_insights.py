# dynamic_insights.py

import streamlit as st
import pandas as pd
import altair as alt

# Load data
@st.cache_data
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    df['genres'] = df['genres'].str.split(",")
    return df

df = load_data()

# Explode genres to handle genre-based aggregation
df_exploded = df.explode('genres')

def show_dynamic_insights():
    st.header('Dynamic Insights Based on Selected Genres and Time')

    # Sidebar with genre multi-select and release year slider
    st.sidebar.title('Movie Data Dashboard')

    # Extract all unique genres for the multi-select dropdown
    options = df['genres'].explode().unique()

    # Multi-select widget for genre combinations
    selected_genres = st.sidebar.multiselect(
        'Select Genres',
        options=options,
        default=None
    )

    # Slider for selecting the release year range
    year_range = st.sidebar.slider(
        "Select Release Year Range",
        min_value=int(df['release_year'].min()),
        max_value=int(df['release_year'].max()),
        value=(int(df['release_year'].min()), int(df['release_year'].max())),
        step=1
    )

    # Filter the DataFrame based on selected genres and year range
    filtered_df = df_exploded[
        df_exploded['release_year'].between(year_range[0], year_range[1])
    ]

    if selected_genres:
        # Filter based on whether all selected genres are present in the genre list for each movie
        filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: all(genre in x for genre in selected_genres))]

    # Total Revenue by Genre (Reversed Axis)
    st.subheader('Total Revenue by Genre')
    genre_revenue = filtered_df.groupby('genres')['revenue_musd'].sum().reset_index().sort_values(by='revenue_musd', ascending=True)  # Reversed sorting

    genre_revenue_chart = alt.Chart(genre_revenue).mark_bar().encode(
        x=alt.X('genres:N', sort='-y'),
        y='revenue_musd:Q',
        color='genres:N'
    ).properties(
        title="Total Revenue by Genre",
        width=1000,
        height=500
    ).configure_axis(
        labelAngle=45
    ).configure_legend(
        orient='none',  # Hide legend
        labelFontSize=10,
        titleFontSize=12
    )

    st.altair_chart(genre_revenue_chart, use_container_width=True)

    # Runtime vs Revenue
    st.subheader('Runtime vs Revenue')
    runtime_revenue = filtered_df[['runtime', 'revenue_musd']].dropna()

    runtime_revenue_chart = alt.Chart(runtime_revenue).mark_point().encode(
        x='runtime:Q',
        y='revenue_musd:Q',
        color=alt.value('green'),
        tooltip=['runtime', 'revenue_musd']
    ).properties(
        title="Runtime vs Revenue",
        width=1000,
        height=500
    )

    st.altair_chart(runtime_revenue_chart, use_container_width=True)

    # Movie Releases by Year
    st.subheader('Movie Releases by Year')
    releases_by_year = filtered_df.groupby('release_year').size().reset_index(name='movie_count')

    releases_by_year_chart = alt.Chart(releases_by_year).mark_line().encode(
        x='release_year:O',
        y='movie_count:Q',
        color=alt.value('orange')
    ).properties(
        title="Number of Movie Releases by Year",
        width=1000,
        height=500
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(releases_by_year_chart, use_container_width=True)

    # Movie Releases by Month
    st.subheader('Movie Releases by Month')
    releases_by_month = filtered_df.groupby('release_month').size().reset_index(name='movie_count')

    releases_by_month_chart = alt.Chart(releases_by_month).mark_line().encode(
        x='release_month:O',
        y='movie_count:Q',
        color=alt.value('blue')
    ).properties(
        title="Number of Movie Releases by Month",
        width=1000,
        height=500
    ).configure_axis(
        labelAngle=0
    )

    st.altair_chart(releases_by_month_chart, use_container_width=True)
