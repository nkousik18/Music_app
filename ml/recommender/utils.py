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

def safe_json_load(x):
    if x is None:
        return None

    # 🔑 MySQL often returns JSON as bytes
    if isinstance(x, (bytes, bytearray)):
        try:
            x = x.decode("utf-8")
        except Exception:
            return None

    if isinstance(x, dict):
        return x

    if not isinstance(x, str):
        return None

    x = x.strip()
    if x == "" or x.lower() == "null":
        return None

    try:
        return json.loads(x)
    except json.JSONDecodeError:
        return None


from sqlalchemy import create_engine

def load_songs():
    # 1. Use SQLAlchemy to avoid the UserWarning and improve stability
    user = os.getenv("DB_USER")
    pw = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")
    
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}/{db}")
    
    df = pd.read_sql("SELECT track_id, genre, popularity, audio_features FROM songs", engine)

    # 2. Parse JSON
    df["audio_features"] = df["audio_features"].apply(safe_json_load)

    # 3. Drop nulls AND reset index (CRITICAL)
    df = df.dropna(subset=["audio_features"]).reset_index(drop=True)

    # 4. Normalize and Concat
    audio_df = pd.json_normalize(df["audio_features"])
    
    # Since indices are reset, they will align perfectly
    df = pd.concat([df.drop(columns=["audio_features"]), audio_df], axis=1)

    return df

def load_events():
    conn = get_db()
    df = pd.read_sql("""
        SELECT user_id, track_id, event_type, ts
        FROM user_events
    """, conn)
    conn.close()
    return df
