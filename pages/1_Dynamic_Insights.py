import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration for this page
st.set_page_config(page_title="Dynamic Insights", page_icon="📊")

# Load data (same as before, assuming the dataset is already cleaned)
@st.cache_data
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    return df

df = load_data()

# Function to show dynamic insights
def show_dynamic_insights():
    st.title('Dynamic Movie Insights')

    # Slider to filter data by release year
    release_year = st.slider('Select Release Year', min_value=1980, max_value=2024, value=(1980, 2024), step=1)
    filtered_df = df[(df['release_year'] >= release_year[0]) & (df['release_year'] <= release_year[1])]

    # Check if there is any missing runtime data
    if filtered_df['runtime'].isnull().any():
        st.warning("Some movies have missing runtime data, and they will be excluded from the analysis.")

    # Example of Dynamic Insights: Average Runtime by Release Year
    st.subheader(f'Average Runtime from {release_year[0]} to {release_year[1]}')
    
    # Grouping and calculating average runtime by year, excluding NaN values
    avg_runtime_by_year = filtered_df.groupby('release_year')['runtime'].mean().reset_index()
    
    # Make sure to filter out years with NaN values (if any)
    avg_runtime_by_year = avg_runtime_by_year.dropna()

    # Check if there is data to plot
    if avg_runtime_by_year.empty:
        st.warning("No data available for the selected year range.")
    else:
        runtime_chart = alt.Chart(avg_runtime_by_year).mark_line().encode(
            x='release_year:O',
            y='runtime:Q',
            color='release_year:N'
        ).properties(
            title="Average Runtime by Year",
            width=1000,
            height=500
        ).configure_axis(
            labelAngle=45
        )
        
        st.altair_chart(runtime_chart, use_container_width=True)

    # Example of Dynamic Insights: Total Revenue by Genre (Filtered by Year)
    st.subheader(f'Total Revenue by Genre from {release_year[0]} to {release_year[1]}')
    genre_revenue = filtered_df.explode('genres').groupby('genres')['revenue_musd'].sum().reset_index().sort_values(by='revenue_musd', ascending=False)
    
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
    )
    
    st.altair_chart(genre_revenue_chart, use_container_width=True)

# Display dynamic insights on page load
show_dynamic_insights()
