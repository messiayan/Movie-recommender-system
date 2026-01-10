import streamlit as st
import pickle
import pandas as pd
import requests

OMDB_API_KEY = "a93811a6"   # <-- REPLACE WITH YOUR FREE API KEY


def fetch_poster(title):
    """Fetch movie poster using OMDb API."""
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Poster") and response["Poster"] != "N/A":
        return response["Poster"]
    else:
        # fallback image
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎥 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)




