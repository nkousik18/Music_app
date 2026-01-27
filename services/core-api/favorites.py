from fastapi import APIRouter, Depends
from db import get_db
from deps import get_current_user

router = APIRouter(prefix="/favorites")

@router.post("/{track_id}")
def add_favorite(track_id: str, user_id=Depends(get_current_user)):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT IGNORE INTO user_favorites (user_id, track_id)
            VALUES (%s,%s)
        """, (user_id, track_id))
    return {"status": "added"}

@router.get("")
def list_favorites(user_id=Depends(get_current_user)):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT s.track_id, s.track_name, s.artist
            FROM user_favorites f
            JOIN songs s ON f.track_id = s.track_id
            WHERE f.user_id=%s
        """, (user_id,))
        return cur.fetchall()
