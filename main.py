import pickle
import requests


def fetch_poster(movie_id):
    API_KEY = '7c80d789262eb3bdc88dbcbd089efc45'
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,API_KEY))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

movies_df = pickle.load(open('movies_df.pkl','rb'))
movies_list = movies_df.title.values
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    recommended_movies = []
    recommended_movies_poster = []
    movie_index = movies_df[movies_df.title == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]

    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].id
        recommended_movies_poster.append(fetch_poster(movie_id))
        

        recommended_movies.append(movies_df.iloc[i[0]].title)
    return recommended_movies, recommended_movies_poster

import streamlit as st

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'What are you looking for today',
    movies_list)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    for i,col in enumerate(st.beta_columns(5)):
        with col:
            st.text(names[i])
            st.image(posters[i]) 
