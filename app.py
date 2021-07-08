import pickle
import streamlit as st
import numpy as np
import pandas as pd
import requests

st.header('Movie Recommendation System')

movies=pd.read_pickle(open('models/movies.pkl','rb'))
similarity=pickle.load(open('models/similarity_movies.pkl','rb'))

def fetch_poster(movie_title):
    url= "https://www.omdbapi.com/?apikey=bdfde34&t={}".format(movie_title)
    data = requests.get(url)
    data = data.json()
    try:
        return data['Poster']
    except:
        return ""

def fetch_id(movie_title):
    url="http://www.omdbapi.com/?t={}&apikey=bdfde34".format(movie_title)
    data=requests.get(url)
    data = data.json()
    imdbid=data['imdbID']
    return imdbid

def fetch_trailer(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/videos?api_key=0506e60a3c913c65b6755c3e8a686305&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    try:
        trailer = data['results'][0]['key']
        return "https://www.youtube.com/watch?v={}".format(trailer)
    except:
        return ""

def recommend(movie):
    index=movies[movies['lister-item-header']==movie].index[0]
    distance=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    movie_names=[]
    movie_images_poster=[]
    movie_trailer=[]
    for i in distance[1:6]:
        movie_title=movies.iloc[i[0]].movie_name
        movie_names.append(movies.iloc[i[0]].movie_name)
        id=fetch_id(movie_title)
        movie_images_poster.append(fetch_poster(movie_title))
        movie_trailer.append(fetch_trailer(id))
    return movie_names,movie_images_poster,movie_trailer

unique_list=movies['movie_name'].unique()
movie_list=np.sort(unique_list)

selected_movie = st.selectbox('Search Movie Name',movie_list)

if st.button('Show Recommendation'):
    movie_names,movie_images_poster,movie_trailer=recommend(selected_movie)
    #st.text(movie_trailer)
    col1,col2,col3,col4,col5=st.beta_columns(5)
    with col1:
        st.text(movie_names[0])
        if(movie_images_poster[0]!=""):
            st.image(movie_images_poster[0])
        else:
            st.text("No Image Found!")
        if(movie_trailer[0]!=""):
            st.markdown("[See Trailer](%s)" % movie_trailer[0])

    with col2:
        st.text(movie_names[1])
        if (movie_images_poster[1] != ""):
            st.image(movie_images_poster[1])
        else:
            st.text("No Image Found!")
        if (movie_trailer[1] != ""):
            st.markdown("[See Trailer](%s)" % movie_trailer[1])

    with col3:
        st.text(movie_names[2])
        if (movie_images_poster[2] != ""):
            st.image(movie_images_poster[2])
        else:
            st.text("No Image Found!")
        if (movie_trailer[2] != ""):
            st.markdown("[See Trailer](%s)" % movie_trailer[2])

    with col4:
        st.text(movie_names[3])
        if (movie_images_poster[3] != ""):
            st.image(movie_images_poster[3])
        else:
            st.text("No Image Found!")
        if (movie_trailer[3] != ""):
            st.markdown("[See Trailer](%s)" % movie_trailer[3])

    with col5:
        st.text(movie_names[4])
        if (movie_images_poster[4] != ""):
            st.image(movie_images_poster[4])
        else:
            st.text("No Image Found!")
        if (movie_trailer[4] != ""):
            st.markdown("[See Trailer](%s)" % movie_trailer[4])