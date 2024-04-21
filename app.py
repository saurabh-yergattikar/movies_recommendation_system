import streamlit as st
import pickle
import requests
import zipfile
import pandas as pd

movies_list = pickle.load(open("newmovies.pkl" , "rb"))
#similarity = pickle.load(open("similarity.pkl" , "rb"))
with zipfile.ZipFile('similarity.pkl.zip') as z:

    with z.open('similarity.pkl') as f:

        similarity = pd.read_pickle(f)


movies_titles = movies_list['title'].values


st.header("Movie Recommendation System")
selectedValue = st.selectbox("Select Movie Name from Dropdown for Recommendation" , movies_titles)

def fetchPoster(movie_id):
    #print(movie_id)
    url = "https://api.themoviedb.org/3/movie/"+str(movie_id)
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYzYyNmE2MWVmNmFjODFiYjY5OTljOTM3MzA1ZjNkNiIsInN1YiI6IjY2MjRjNmYwNjNkOTM3MDE2NDcxZjkwOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.nAfSmnGNm1F2RkKmPMp1J8Vw2aGpeyObFFYwEMdne2A"
    }
    data = requests.get(url, headers=headers)   
    data = data.json()
    #print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


def recommend(moviename):
    index=movies_list[movies_list['title']==moviename].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True, key=lambda similarity:similarity[1])
    recommended_movie_names = []
    movie_poster_fetched = []
    for i in distance[1:6]:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movie_names.append((movies_list.iloc[i[0]].title))
        movie_poster_fetched.append(fetchPoster(movie_id))
    return recommended_movie_names , movie_poster_fetched

if st.button("Show Recommendation"):
    movie_names_list , movie_poster_fetched = recommend(selectedValue)
    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(movie_names_list[0])
        st.image(movie_poster_fetched[0])
    with col2:
        st.text(movie_names_list[1])     
        st.image(movie_poster_fetched[1])
    with col3:
        st.text(movie_names_list[2])
        st.image(movie_poster_fetched[2])

    with col4:
        st.text(movie_names_list[3])   
        st.image(movie_poster_fetched[3])  

    with col5:
        st.text(movie_names_list[4])
        st.image(movie_poster_fetched[4])

