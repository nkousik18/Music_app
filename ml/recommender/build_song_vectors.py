import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from utils import load_songs

FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness",
    "valence", "tempo"
]

df = load_songs()

# Ensure duration_ms exists (from base table, not JSON)
assert "duration_ms" in df.columns

X = df[FEATURES].astype(float)

# 🔒 Drop rows with ANY NaNs
mask = np.isfinite(X).all(axis=1)
X_clean = X[mask]
ids_clean = df.loc[mask, "track_id"].values

print(f"🧹 Dropped {len(X) - len(X_clean)} songs with invalid features")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clean)

# 🔒 Final sanity check
assert np.isfinite(X_scaled).all()

joblib.dump(
    {
        "track_ids": ids_clean,
        "vectors": X_scaled,
        "scaler": scaler
    },
    "../artifacts/song_vectors.pkl"
)

print(f"✅ Song vectors saved: {len(ids_clean)}")
