import joblib
from utils import load_songs
from candidate_generation import generate_candidates

# Load metadata
df = load_songs()
genre_map = dict(zip(df.track_id, df.genre))
pop_map = dict(zip(df.track_id, df.popularity))

# Load user vectors
USER_VECTORS = joblib.load("../artifacts/user_profiles.pkl")

def rank(user_id, k=10):
    if user_id not in USER_VECTORS:
        return []

    user_vec = USER_VECTORS[user_id]

    candidates = generate_candidates(user_vec, 300)

    scored = []
    for track_id, sim in candidates:
        score = (
            0.6 * sim +
            0.3 * (pop_map.get(track_id, 0) / 100)
        )
        scored.append((track_id, score, genre_map.get(track_id)))

    scored.sort(key=lambda x: x[1], reverse=True)

    # 🎯 Diversity constraint
    final = []
    genre_count = {}

    for t, s, g in scored:
        if genre_count.get(g, 0) >= 3:
            continue
        genre_count[g] = genre_count.get(g, 0) + 1
        final.append(t)
        if len(final) == k:
            break

    return final
