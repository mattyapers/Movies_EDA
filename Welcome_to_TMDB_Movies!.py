import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Welcome to TMDB Movie Dataset Dashboard!",
    page_icon="🎬",
    layout="centered"
)

# Page title and subtitle
st.title("🎥 Welcome to the TMDB Movie Dataset Dashboard!")
st.markdown(
    """
    <style>
        .main-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }
        .sub-title {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }
        .description {
            font-size: 16px;
            line-height: 1.6;
        }
        .nav-button {
            display: inline-block;
            padding: 10px 20px;
            margin: 10px;
            font-size: 16px;
            font-weight: bold;
            color: white;
            background-color: #4CAF50;
            text-align: center;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .nav-button:hover {
            background-color: #45a049;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Description
st.markdown(
    """
    <div class="sub-title">Explore insightful trends and analytics from the TMDB Movie Dataset!</div>
    <div class="description">
        This dashboard allows you to interact with data on movie revenue, budget, genres, and much more.
        Use the sidebar to navigate between static and dynamic insights.
        *New Dataset contains 897382 entries*
    </div>
    """,
    unsafe_allow_html=True
)

# Add a banner image or GIF
st.image(
    "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExanBzMW1hbHViemhieWFnOHFxcG5rb3Q4b3BxZXRpaXFrcjl0ZGZhMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8Iv5lqKwKsZ2g/giphy.gif",
    use_container_width=True
)

# Footer with acknowledgments
st.markdown(
    """
    <hr>
    <div style="text-align: center; font-size: 14px; color: #555;">
        Data Source: <a href="https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies" target="_blank">Kaggle</a><br>
        Dashboard created with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
