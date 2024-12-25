import streamlit as st
import pandas as pd
import altair as alt

# Page configuration for static insights
st.set_page_config(page_title="Static Insights", page_icon="📊")

# Load data (assuming cleaned dataset is already available)
@st.cache_data
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    return df

df = load_data()

# Clean the dataset by removing 'Unknown' values from production_countries and genres
df = df[df['production_countries'] != 'Unknown']
df = df[df['genres'] != 'Unknown']

# Split genres column into lists before exploding
df['genres'] = df['genres'].str.split(',')

def show_static_insights():
    st.header('All-Time Top Insights')

    # Top 10 Highest Production Countries
    st.subheader('All-Time Top 10 Highest Production Countries')
    top_countries = df.explode('production_countries').groupby('production_countries').size().reset_index(name='movie_count')
    top_countries = top_countries.nlargest(10, 'movie_count')

    countries_chart = alt.Chart(top_countries).mark_bar().encode(
        x=alt.X('movie_count:Q', title='Movie Count'),
        y=alt.Y('production_countries:N', title='Production Country'),
        color='production_countries:N'
    ).properties(
        title="Top 10 Highest Production Countries",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(countries_chart, use_container_width=True)

    # Top 10 Highest Genres
    st.subheader('All-Time Top 10 Highest Genres')
    top_genres = df.explode('genres').groupby('genres').size().reset_index(name='genre_count')
    top_genres = top_genres.nlargest(10, 'genre_count')

    genres_chart = alt.Chart(top_genres).mark_bar().encode(
        x=alt.X('genre_count:Q', title='Genre Count'),
        y=alt.Y('genres:N', title='Genre'),
        color='genres:N'
    ).properties(
        title="Top 10 Highest Genres",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(genres_chart, use_container_width=True)

    # Top 10 Highest Original Languages
    st.subheader('All-Time Top 10 Highest Original Languages')
    top_languages = df.groupby('original_language').size().reset_index(name='language_count')
    top_languages = top_languages.nlargest(10, 'language_count')

    languages_chart = alt.Chart(top_languages).mark_bar().encode(
        x=alt.X('language_count:Q', title='Language Count'),
        y=alt.Y('original_language:N', title='Original Language'),
        color='original_language:N'
    ).properties(
        title="Top 10 Highest Original Languages",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(languages_chart, use_container_width=True)

    # Top 10 Highest Popularity
    st.subheader('All-Time Top 10 Highest Popularity Movies')
    top_popularity = df.nlargest(10, 'popularity')[['title', 'popularity']]

    popularity_chart = alt.Chart(top_popularity).mark_bar().encode(
        x=alt.X('popularity:Q', title='Popularity'),
        y=alt.Y('title:N', title='Movie Title'),
        color='title:N'
    ).properties(
        title="Top 10 Highest Popularity Movies",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(popularity_chart, use_container_width=True)

    # Additional Insights

    # Average Budget and Revenue by Genre
    st.subheader('Average Budget and Revenue by Genre')
    avg_budget_revenue = df.explode('genres').groupby('genres')[['budget_musd', 'revenue_musd']].mean().reset_index()
    avg_budget_revenue = avg_budget_revenue.sort_values(by='revenue_musd', ascending=False)

    budget_revenue_chart = alt.Chart(avg_budget_revenue).mark_bar().encode(
        x=alt.X('genres:N', title='Genre'),
        y=alt.Y('revenue_musd:Q', title='Revenue (in million USD)'),
        color='genres:N'
    ).properties(
        title="Average Revenue by Genre",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(budget_revenue_chart, use_container_width=True)

    # Top 10 Movies by Profit
    st.subheader('All-Time Top 10 Highest Profit Movies')
    top_profit_movies = df.nlargest(10, 'profit_musd')[['title', 'profit_musd']]

    profit_chart = alt.Chart(top_profit_movies).mark_bar().encode(
        x=alt.X('profit_musd:Q', title='Profit (in million USD)'),
        y=alt.Y('title:N', title='Movie Title'),
        color='title:N'
    ).properties(
        title="Top 10 Highest Profit Movies",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(profit_chart, use_container_width=True)

    # Revenue vs Budget for Different Genres
    st.subheader('Revenue vs Budget for Different Genres')
    revenue_budget_by_genre = df.explode('genres').groupby('genres')[['revenue_musd', 'budget_musd']].mean().reset_index()

    revenue_budget_chart = alt.Chart(revenue_budget_by_genre).mark_point().encode(
        x=alt.X('budget_musd:Q', title='Average Budget (in million USD)'),
        y=alt.Y('revenue_musd:Q', title='Average Revenue (in million USD)'),
        color='genres:N',
        tooltip=['genres:N', 'budget_musd:Q', 'revenue_musd:Q']
    ).properties(
        title="Revenue vs Budget by Genre",
        width=800,
        height=400
    ).configure_axis(
        labelAngle=45
    )

    st.altair_chart(revenue_budget_chart, use_container_width=True)

# Show the insights
show_static_insights()
