import joblib
import numpy as np
from collections import defaultdict
from utils import load_events

# --------------------------------------------------
# Config
# --------------------------------------------------

EVENT_WEIGHTS = {
    "play": 1.0,
    "like": 3.0,
    "skip": -2.0
}

# --------------------------------------------------
# Load artifacts
# --------------------------------------------------

data = joblib.load("../artifacts/song_vectors.pkl")
track_ids = data["track_ids"]
vectors = data["vectors"]

# Build fast lookup: track_id -> vector
song_index = {
    tid: vec for tid, vec in zip(track_ids, vectors)
}

events = load_events()

# Normalize event types defensively
events["event_type"] = events["event_type"].str.lower()

# --------------------------------------------------
# Build weighted user profiles
# --------------------------------------------------

user_profiles = defaultdict(list)

for _, row in events.iterrows():
    event = row.event_type

    # Skip unknown events
    if event not in EVENT_WEIGHTS:
        continue

    # Skip tracks not in catalog
    if row.track_id not in song_index:
        continue

    user_profiles[row.user_id].append(
        EVENT_WEIGHTS[event] * song_index[row.track_id]
    )

# --------------------------------------------------
# Aggregate + normalize user embeddings
# --------------------------------------------------

user_embeddings = {}
skipped_users = 0

for user, vecs in user_profiles.items():
    if len(vecs) == 0:
        skipped_users += 1
        continue

    emb = np.mean(vecs, axis=0)

    # Guardrail 1: NaNs / infs
    if not np.all(np.isfinite(emb)):
        skipped_users += 1
        continue

    # Guardrail 2: zero vector
    norm = np.linalg.norm(emb)
    if norm == 0:
        skipped_users += 1
        continue

    user_embeddings[user] = emb / norm

# --------------------------------------------------
# Diagnostics
# --------------------------------------------------

print(events.event_type.value_counts())
print(f"User profiles saved: {len(user_embeddings)}")
print(f"Skipped users (invalid profiles): {skipped_users}")

# --------------------------------------------------
# Persist
# --------------------------------------------------

joblib.dump(user_embeddings, "../artifacts/user_profiles.pkl")

print("User profiles artifact written.")
