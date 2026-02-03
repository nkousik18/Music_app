# routes/events.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from auth import get_current_user
from auth.models import Song, UserEvent
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])

ALLOWED_EVENTS = {"play", "like", "skip"}

@router.post("/{track_id}/{event_type}")
def log_event(
    track_id: str,
    event_type: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if event_type not in ALLOWED_EVENTS:
        raise HTTPException(status_code=400, detail="Invalid event type")

    # 🔒 HARD VALIDATION
    song_exists = db.query(Song).filter(Song.track_id == track_id).first()
    if not song_exists:
        raise HTTPException(
            status_code=404,
            detail=f"Track ID {track_id} does not exist"
        )

    event = UserEvent(
        user_id=user.id,
        track_id=track_id,
        event_type=event_type,
        ts=datetime.utcnow()
    )

    db.add(event)
    db.commit()

    return {"status": "logged"}
