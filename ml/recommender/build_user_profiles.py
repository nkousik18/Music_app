import joblib
import numpy as np
from collections import defaultdict
from utils import load_events
from sklearn.preprocessing import normalize

EVENT_WEIGHTS = {
    "play": 1.0,
    "like": 3.0,
    "skip": -2.0
}

song_vectors = joblib.load("../artifacts/song_vectors.pkl")
events = load_events()

user_profiles = defaultdict(list)

for _, row in events.iterrows():
    if row.track_id not in song_vectors:
        continue
    w = EVENT_WEIGHTS.get(row.event_type, 0)
    user_profiles[row.user_id].append(
        w * song_vectors[row.track_id]
    )

user_embeddings = {}
for user, vecs in user_profiles.items():
    if len(vecs) == 0:
        continue
    emb = np.mean(vecs, axis=0)
    user_embeddings[user] = normalize(emb.reshape(1,-1))[0]

joblib.dump(user_embeddings, "../artifacts/user_profiles.pkl")

print(" User profiles saved:", len(user_embeddings))
