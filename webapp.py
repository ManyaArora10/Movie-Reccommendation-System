import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    # Debugging: Print the response to check if 'poster_path' exists
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    else:
        # If 'poster_path' is missing, return a placeholder image URL
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Load data
movies = pickle.load(open("new_data.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))  # Ensure the file name and path are correct

# Extract movie titles
new_data = movies['title'].values

# Streamlit header
st.header('Movie Recommendation System')

# Dropdown for selecting movies
selectvalue = st.selectbox("Select movies from dropdown", new_data)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movies = []
    recommend_poster = []
    for i in distances[1:6]:  # Get the top 5 recommendations, skipping the first one as it's the movie itself
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_poster

# Show recommendations on button click
if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(selectvalue)
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
