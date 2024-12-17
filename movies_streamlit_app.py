import altair as alt
import pandas as pd
import streamlit as st
from IPython.display import HTML
import re

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🎬")
st.title("🎬 Movies dataset")
st.write(
    """
    This app visualizes data from the Movie Database.
    It shows which movie genre performed best at the box office over the years. 
    Click on the widgets below to explore!
    """
)

# Load the data from a CSV with caching.
@st.cache_data
def load_data():
    df = pd.read_csv("movies_complete.csv", parse_dates= ["release_date"])
    return df

# Load the data
df = load_data()

# Display the first 5 rows of the dataset
st.write("### Preview of the Dataset")
st.write(df.head(5))

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

# # Filter the DataFrame based on selected genres
# if selected_genres:
#     # Drop NaN or replace them with empty strings before applying the check
#     filtered_df = df[df['genres'].fillna('').apply(lambda x: any(genre in x for genre in selected_genres))]
    
#     st.write(f"Movies matching genres: {', '.join(selected_genres)}")
#     st.dataframe(filtered_df[['title', 'genres']].head(20)) # Show first 20 results
# else:
#     st.write("No genres selected. Please choose from the list.")


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



# Show the Movies that contain that genre


# # Show a multiselect widget with the genres using `st.multiselect`.
# genres = st.multiselect(
#     "Genre",
#     df['.genres.unique(),
#     ["Action", "Adventure", "Biography", "Comedy", "Drama", "Horror"]'],
# )

# # Show a slider widget with the years using `st.slider`.
# years = st.slider("Years", 1986, 2006, (2000, 2016))

# # Filter the dataframe based on the widget input and reshape it.
# df_filtered = df[(df["genres"].isin(genres)) & (df["year"].between(years[0], years[1]))]
# df_reshaped = df_filtered.pivot_table(
#     index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0
# )
# df_reshaped = df_reshaped.sort_values(by="year", ascending=False)


# # Display the data as a table using `st.dataframe`.
# st.dataframe(
#     df_reshaped,
#     use_container_width=True,
#     column_config={"year": st.column_config.TextColumn("Year")},
# )

# # Display the data as an Altair chart using `st.altair_chart`.
# df_chart = pd.melt(
#     df_reshaped.reset_index(), id_vars="year", var_name="genre", value_name="gross"
# )
# chart = (
#     alt.Chart(df_chart)
#     .mark_line()
#     .encode(
#         x=alt.X("year:N", title="Year"),
#         y=alt.Y("gross:Q", title="Gross earnings ($)"),
#         color="genre:N",
#     )
#     .properties(height=320)
# )
# st.altair_chart(chart, use_container_width=True)