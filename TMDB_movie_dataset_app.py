import streamlit as st
import pandas as pd
import altair as alt

# Load data
@st.cache
def load_data():
    df = pd.read_parquet('TMDB_movie_dataset_v11_cleaned.parquet')
    return df