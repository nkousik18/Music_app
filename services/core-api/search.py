from fastapi import APIRouter, Query
from db import get_db

router = APIRouter(prefix="/search")

@router.get("")
def search(q: str = Query(...)):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT track_id, track_name, artist, genre, popularity
            FROM songs
            WHERE MATCH(track_name, artist, album_name, genre, subgenre)
            AGAINST (%s IN NATURAL LANGUAGE MODE)
            ORDER BY popularity DESC
            LIMIT 50
        """, (q,))
        return cur.fetchall()
