import pandas as pd
import json
import unicodedata
from datetime import datetime

INPUT_FILE = "/Users/kousiknandury/Desktop/Spotify_demo/ml/data/songs.csv"
OUTPUT_FILE = "/Users/kousiknandury/Desktop/Spotify_demo/ml/data/songs.csv"

# -----------------------------
# Helpers
# -----------------------------
def normalize_text(x):
    if pd.isna(x):
        return None
    x = str(x)
    x = unicodedata.normalize("NFKC", x)
    x = x.replace("\x00", "")  # remove null bytes
    return x.strip()

def parse_date(x):
    if pd.isna(x):
        return None
    try:
        return pd.to_datetime(x, errors="coerce").date()
    except:
        return None

def to_int(x):
    try:
        return int(float(x))
    except:
        return None

def to_json(x):
    if pd.isna(x) or x == "":
        return None
    try:
        if isinstance(x, dict):
            return json.dumps(x)
        return json.dumps(json.loads(x))
    except:
        return None

# -----------------------------
# Load safely (UTF-8)
# -----------------------------
df = pd.read_csv(
    INPUT_FILE,
    encoding="utf-8",
    engine="python"
)

# -----------------------------
# Column normalization
# -----------------------------
TEXT_COLS = [
    "track_id", "track_name", "artist",
    "album_id", "album_name",
    "genre", "subgenre"
]

for col in TEXT_COLS:
    if col in df.columns:
        df[col] = df[col].apply(normalize_text)

# -----------------------------
# Type enforcement
# -----------------------------
df["release_date"] = df.get("release_date").apply(parse_date)
df["popularity"] = df.get("popularity").apply(to_int)
df["duration_ms"] = df.get("duration_ms").apply(to_int)
df["audio_features"] = df.get("audio_features").apply(to_json)

# -----------------------------
# Hard constraints
# -----------------------------
df = df[df["track_id"].notna()]          # PK cannot be NULL
df = df.drop_duplicates(subset=["track_id"])

# Trim overflows (MySQL safety)
df["track_name"] = df["track_name"].str.slice(0, 255)
df["artist"] = df["artist"].str.slice(0, 255)
df["album_name"] = df["album_name"].str.slice(0, 255)
df["genre"] = df["genre"].str.slice(0, 64)
df["subgenre"] = df["subgenre"].str.slice(0, 128)

# -----------------------------
# Export clean UTF-8 CSV
# -----------------------------
df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8",
    quoting=1  # QUOTE_ALL → safer for Workbench
)

print(f"Cleaned file written to: {OUTPUT_FILE}")
print(f"Rows ready for import: {len(df)}")
