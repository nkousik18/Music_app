import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

song_vectors = joblib.load("../artifacts/song_vectors.pkl")
user_profiles = joblib.load("../artifacts/user_profiles.pkl")

def generate_candidates(user_id, top_k=200):
    if user_id not in user_profiles:
        return []

    user_vec = user_profiles[user_id].reshape(1,-1)
    tracks = list(song_vectors.keys())
    matrix = np.vstack([song_vectors[t] for t in tracks])

    sims = cosine_similarity(user_vec, matrix)[0]
    ranked = sorted(zip(tracks, sims), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
