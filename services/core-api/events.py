from fastapi import APIRouter, Depends
from db import get_db
from deps import get_current_user
import uuid

router = APIRouter(prefix="/events")

@router.post("/{track_id}/{event_type}")
def log_event(track_id: str, event_type: str, user_id=Depends(get_current_user)):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_events
            VALUES (%s,%s,%s,%s,NOW())
        """, (
            str(uuid.uuid4()),
            user_id,
            track_id,
            event_type
        ))
    return {"status": "logged"}
