import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

from src.data_loader import load_data

# Load and prepare data (only once, globally for all methods)
df = load_data("data/TMDB_movies.csv").reset_index(drop=True)

# Handle nulls and create 'content' column for content-based filtering
df['overview'] = df['overview'].fillna('')
df['genre'] = df['genre'].fillna('')
df['content'] = df['overview'] + " " + df['genre']

# Create index mapping
indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()

# ---------- Content-Based Filtering Setup ----------
tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
tfidf_matrix = tfidf.fit_transform(df['content'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# ---------- Collaborative Filtering Setup ----------
features = df[['vote_average', 'vote_count', 'popularity']].fillna(0)

scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(scaled_features)

# ========== RECOMMENDATION FUNCTIONS ========== #

def recommend_content(title, top_n=5):
    """
    Recommend movies based on plot/genre similarity.
    """
    title = title.lower()
    if title not in indices:
        return f"❌ Movie '{title}' not found in dataset."

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]

    return df[['title', 'genre', 'vote_average', 'popularity']].iloc[movie_indices]


def recommend_collaborative(title, top_n=5):
    """
    Recommend movies based on popularity, ratings (vote_average, vote_count).
    """
    title = title.lower()
    if title not in indices:
        return f"❌ Movie '{title}' not found in dataset."

    idx = indices[title]
    movie_vector = scaled_features[idx].reshape(1, -1)
    _, knn_indices = model_knn.kneighbors(movie_vector, n_neighbors=top_n + 1)

    movie_indices = knn_indices.flatten()[1:]  # Skip the input movie itself
    return df[['title', 'genre', 'vote_average', 'popularity']].iloc[movie_indices]


def hybrid_recommend(title, top_n=5):
    """
    Combine content-based + collaborative-based recommendations.
    """
    title = title.lower()
    if title not in indices:
        return f"❌ Movie '{title}' not found in dataset."

    idx = indices[title]

    # Content-based
    content_sim_scores = list(enumerate(cosine_sim[idx]))
    content_sim_scores = sorted(content_sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    content_indices = [i[0] for i in content_sim_scores]

    # Collaborative-based
    movie_vector = scaled_features[idx].reshape(1, -1)
    _, knn_indices = model_knn.kneighbors(movie_vector, n_neighbors=top_n + 1)
    collaborative_indices = knn_indices.flatten()[1:]

    # Combine both (intersection first, then union)
    combined_indices = list(set(content_indices) & set(collaborative_indices))
    if len(combined_indices) < top_n:
        combined_indices += list(set(content_indices + collaborative_indices) - set(combined_indices))
    combined_indices = combined_indices[:top_n]

    if not combined_indices:
        return "⚠️ Not enough similar movies found using hybrid filtering."

    # Safely drop any out-of-bounds indices
    valid_indices = [i for i in combined_indices if i < len(df)]
    
    return df[['title', 'genre', 'vote_average', 'popularity']].iloc[valid_indices]

