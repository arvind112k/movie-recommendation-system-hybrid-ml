# app.py

import streamlit as st
import pandas as pd

from src.recommendation import recommend_content, recommend_collaborative, hybrid_recommend
from src.data_loader import load_data

# Load dataset
df = load_data("data/TMDB_movies.csv")

# --- UI ---
st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("🎬 Movie Recommendation System")

# --- Sidebar ---
st.sidebar.title("Settings")
selected_model = st.sidebar.radio("Choose Recommendation Method", 
                                  ("Content-Based", "Collaborative-Based", "Hybrid"))

top_n = st.sidebar.slider("Number of Recommendations", 1, 10, 5)

# --- Dropdown for movie selection ---
movie_list = df['title'].dropna().unique().tolist()
movie_list.sort()
selected_movie = st.selectbox("Select a Movie", movie_list)

# --- Trigger ---
if st.button("Recommend"):
    st.write(f"### Recommendations for: {selected_movie}")
    
    if selected_model == "Content-Based":
        results = recommend_content(selected_movie, top_n)
    elif selected_model == "Collaborative-Based":
        results = recommend_collaborative(selected_movie, top_n)
    else:
        results = hybrid_recommend(selected_movie, top_n)

    # Display results
    if isinstance(results, str):
        st.error(results)
    else:
        st.table(results.reset_index(drop=True))
