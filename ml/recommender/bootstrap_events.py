import random
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
         f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(DB_URL)

USERS = list(range(1, 11))   # 10 users
EVENTS = ["play", "like", "skip"]
EVENT_WEIGHTS = [0.7, 0.2, 0.1]
EVENTS_PER_USER = 500

with engine.connect() as conn:
    songs = conn.execute(
        text("SELECT track_id FROM songs")
    ).fetchall()

    song_ids = [s[0] for s in songs]

    inserts = []

    for user in USERS:
        sampled_tracks = random.sample(song_ids, EVENTS_PER_USER)
        for track_id in sampled_tracks:
            event = random.choices(EVENTS, EVENT_WEIGHTS)[0]
            inserts.append({
                "user_id": user,
                "track_id": track_id,
                "event_type": event
            })

    conn.execute(
        text("""
        INSERT INTO user_events (user_id, track_id, event_type)
        VALUES (:user_id, :track_id, :event_type)
        """),
        inserts
    )

    conn.commit()

print(f"✅ Inserted {len(inserts)} events")
