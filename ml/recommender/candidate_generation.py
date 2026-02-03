import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

data = joblib.load("../artifacts/song_vectors.pkl")
TRACK_IDS = data["track_ids"]
MATRIX = data["vectors"]

def generate_candidates(user_vec, top_n=300):
    user_vec = user_vec.reshape(1, -1)

    sims = cosine_similarity(user_vec, MATRIX)[0]
    top_idx = np.argsort(sims)[::-1][:top_n]

    return [
        (TRACK_IDS[i], float(sims[i]))
        for i in top_idx
    ]
