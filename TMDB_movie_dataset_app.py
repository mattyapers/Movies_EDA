#TMDB_movie_dataset_app.py

import streamlit as st
from static_insights import show_static_insights
from dynamic_insights import show_dynamic_insights

# Page configuration
st.set_page_config(page_title="Movies Data Analysis", layout="wide")
st.title("Movies Data Analysis!")
st.write("Data obtained from https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies, cleaned by me!")

# Sidebar page selector
page = st.sidebar.selectbox('Select a page', ['Static Insights', 'Dynamic Insights'])

# Display content based on the selected page
if page == 'Static Insights':
    show_static_insights()
elif page == 'Dynamic Insights':
    show_dynamic_insights()
