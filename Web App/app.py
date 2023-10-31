import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=cb7f888ffd9fc2fe7612cf57e0505930&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

def recommend_movie(movie):
    # Fetching the movie index
    movie_index = movies[movies['title'] == movie].index[0]
    
    #Vector of similarity scores with other movies
    distances = similarity[movie_index]
    
    # Getting top 5 similar recommended movies by sorting the similarity score
    # In descending order and maintaing the indices in order to fetch the movies
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []

    for movie in movies_list:
        id = movies.iloc[movie[0]].movie_id

        recommended_movies.append(movies.iloc[movie[0]].title) #Getting movie title from index
        recommended_movies_posters.append(fetch_poster(id)) #Fetch movie poster from API

    return recommended_movies, recommended_movies_posters

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity_matrix.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Choose your favorite movie name !!',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend_movie(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])