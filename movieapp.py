import streamlit as st
import pickle
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d2f6755714eb94735ad3e64936b542af"
    response = requests.get(url)
    data = response.json()
    
    # Check if 'poster_path' key exists
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    else:
        # Return a default poster path or a placeholder image if 'poster_path' is missing
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

# Load movies and similarity data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Streamlit interface
st.header("Movie Recommendation System")

# Create a dropdown to select movie
selected_movie = st.selectbox("Select a movie:", movies_list)

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# Display recommendations
if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(selected_movie)
    if movie_names:  # Ensure there are recommendations to display
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.text(movie_names[0])
            st.image(movie_posters[0])
        with col2:
            st.text(movie_names[1])
            st.image(movie_posters[1])
        with col3:
            st.text(movie_names[2])
            st.image(movie_posters[2])
        with col4:
            st.text(movie_names[3])
            st.image(movie_posters[3])
        with col5:
            st.text(movie_names[4])
            st.image(movie_posters[4])
    else:
        st.error("No recommendations available.")
