import pymysql
import os
import pandas as pd
import json
from dotenv import load_dotenv

load_dotenv()

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

import os
import json
import pandas as pd
from sqlalchemy import create_engine

def safe_json_load(x):
    try:
        return json.loads(x) if x else None
    except Exception:
        return None

def load_songs():
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")

    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")

    # 🔑 duration_ms INCLUDED explicitly
    df = pd.read_sql("""
        SELECT
            track_id,
            genre,
            popularity,
            duration_ms,
            audio_features
        FROM songs
        WHERE audio_features IS NOT NULL
    """, engine)

    # Parse JSON safely
    df["audio_features"] = df["audio_features"].apply(safe_json_load)

    # Drop rows where JSON failed
    df = df.dropna(subset=["audio_features"]).reset_index(drop=True)

    # Normalize JSON → columns
    audio_df = pd.json_normalize(df["audio_features"])

    # Merge
    df = pd.concat(
        [df.drop(columns=["audio_features"]), audio_df],
        axis=1
    )

    return df


from sqlalchemy import create_engine
import os

def load_events():
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")

    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")

    df = pd.read_sql(
        "SELECT user_id, track_id, event_type, ts FROM user_events",
        engine
    )

    return df

