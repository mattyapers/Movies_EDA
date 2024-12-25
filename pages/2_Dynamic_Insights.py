import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="Dynamic Insights", page_icon="📊", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    return df

df = load_data()

# Data cleaning for dynamic insights
df = df[df['production_countries'] != 'Unknown']
df = df[df['genres'] != 'Unknown']
df['genres'] = df['genres'].str.split(',')

# Dynamic insights page content
def show_dynamic_insights():
    st.title('Dynamic Insights Dashboard')

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_genres = st.sidebar.multiselect(
        "Select Genres",
        options=df['genres'].explode().unique(),
        default=None
    )
    selected_languages = st.sidebar.multiselect(
        "Select Original Languages",
        options=df['original_language'].unique(),
        default=None
    )
    release_year_range = st.sidebar.slider(
        "Select Release Year Range",
        min_value=int(df['release_year'].min()),
        max_value=int(df['release_year'].max()),
        value=(1980, 2024),
        step=1
    )

    # Apply filters
    filtered_df = df[(df['release_year'] >= release_year_range[0]) & (df['release_year'] <= release_year_range[1])]

    if selected_genres:
        filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]

    if selected_languages:
        filtered_df = filtered_df[filtered_df['original_language'].isin(selected_languages)]

    # Visualization: Profit vs. Release Year
    st.subheader("Profit Trends Over Time")
    profit_year = filtered_df.groupby('release_year')['profit_musd'].sum().reset_index()

    profit_year_chart = alt.Chart(profit_year).mark_line(point=True).encode(
        x=alt.X('release_year:O', title='Release Year'),
        y=alt.Y('profit_musd:Q', title='Total Profit (in million USD)'),
        tooltip=['release_year:O', 'profit_musd:Q']
    ).properties(
        title="Profit vs. Release Year",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(profit_year_chart, use_container_width=True)

    # Visualization: Number of Movie Releases by Year
    st.subheader("Number of Movie Releases Over Time")
    releases_year = filtered_df['release_year'].value_counts().reset_index()
    releases_year.columns = ['release_year', 'movie_count']
    releases_year = releases_year.sort_values(by='release_year')

    releases_year_chart = alt.Chart(releases_year).mark_area().encode(
        x=alt.X('release_year:O', title='Release Year'),
        y=alt.Y('movie_count:Q', title='Number of Movie Releases'),
        tooltip=['release_year:O', 'movie_count:Q']
    ).properties(
        title="Movie Releases Over Time",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(releases_year_chart, use_container_width=True)

    # Visualization: Revenue by Production Country and Release Year
    st.subheader("Revenue by Production Country")
    country_revenue = filtered_df.explode('production_countries').groupby(['release_year', 'production_countries'])['revenue_musd'].sum().reset_index()
    top_countries = country_revenue.groupby('production_countries')['revenue_musd'].sum().nlargest(10).index
    country_revenue = country_revenue[country_revenue['production_countries'].isin(top_countries)]

    country_revenue_chart = alt.Chart(country_revenue).mark_bar().encode(
        x=alt.X('release_year:O', title='Release Year'),
        y=alt.Y('revenue_musd:Q', title='Total Revenue (in million USD)'),
        color='production_countries:N',
        tooltip=['release_year:O', 'production_countries:N', 'revenue_musd:Q']
    ).properties(
        title="Revenue by Production Country and Year",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(country_revenue_chart, use_container_width=True)

    # Visualization: Top Genres by Revenue within Selected Years
    st.subheader("Top Genres by Revenue")
    genre_revenue = filtered_df.explode('genres').groupby('genres')['revenue_musd'].sum().reset_index()
    genre_revenue = genre_revenue.sort_values(by='revenue_musd', ascending=False).head(10)

    genre_revenue_chart = alt.Chart(genre_revenue).mark_bar().encode(
        x=alt.X('genres:N', title='Genre', sort='-y'),
        y=alt.Y('revenue_musd:Q', title='Total Revenue (in million USD)'),
        color='genres:N',
        tooltip=['genres:N', 'revenue_musd:Q']
    ).properties(
        title="Top Genres by Revenue",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(genre_revenue_chart, use_container_width=True)

# Display the dynamic insights
show_dynamic_insights()
