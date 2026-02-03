import joblib
from sklearn.preprocessing import StandardScaler
from utils import load_songs

FEATURES = [
    "danceability","energy","loudness","speechiness",
    "acousticness","instrumentalness","liveness",
    "valence","tempo"
]

df = load_songs()

scaler = StandardScaler()
X = scaler.fit_transform(df[FEATURES])

song_vectors = {
    track_id: vec
    for track_id, vec in zip(df["track_id"], X)
}

joblib.dump(song_vectors, "../artifacts/song_vectors.pkl")
joblib.dump(scaler, "../artifacts/song_scaler.pkl")

print(" Song vectors saved:", len(song_vectors))
