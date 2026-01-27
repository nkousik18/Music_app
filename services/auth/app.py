from fastapi import FastAPI, HTTPException, Depends
from models import *
from dotenv import load_dotenv
from db import get_db
from auth import create_access_token, create_refresh_token
import bcrypt
import uuid
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(title="Auth Service")

# ----------------------------
# REGISTER
# ----------------------------
@app.post("/auth/register")
def register(req: RegisterRequest, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT 1 FROM users WHERE email=%s", (req.email,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Email already exists")

        user_id = str(uuid.uuid4())
        pw_hash = bcrypt.hashpw(
            req.password.encode(), bcrypt.gensalt()
        ).decode()

        cur.execute(
            "INSERT INTO users (user_id, email, password_hash, created_at) VALUES (%s,%s,%s,NOW())",
            (user_id, req.email, pw_hash),
        )

    return {"message": "User registered"}

# ----------------------------
# LOGIN
# ----------------------------
@app.post("/auth/login")
def login(req: LoginRequest, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email=%s", (req.email,))
        user = cur.fetchone()

        if not user or not bcrypt.checkpw(
            req.password.encode(),
            user["password_hash"].encode(),
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access = create_access_token(user["user_id"])
        refresh = create_refresh_token()

        cur.execute(
            """
            INSERT INTO refresh_tokens
            (token_id, user_id, refresh_token, expires_at, created_at)
            VALUES (%s,%s,%s,%s,NOW())
            """,
            (
                str(uuid.uuid4()),
                user["user_id"],
                refresh,
                datetime.utcnow() + timedelta(days=7),
            ),
        )

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }

# ----------------------------
# REFRESH
# ----------------------------
@app.post("/auth/refresh")
def refresh_token(token: str, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT user_id FROM refresh_tokens
            WHERE refresh_token=%s AND expires_at > NOW()
            """,
            (token,),
        )
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access = create_access_token(row["user_id"])
        return {"access_token": access}

# ----------------------------
# HEALTH
# ----------------------------
@app.get("/db/health")
def health():
    try:
        import pymysql, os
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connect_timeout=2,
        )
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "starting", "detail": str(e)}


@app.post("/auth/logout")
def logout(req: LogoutRequest, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "DELETE FROM refresh_tokens WHERE refresh_token=%s",
            (req.refresh_token,)
        )

        if cur.rowcount == 0:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

    return {"message": "Logged out successfully"}

@app.post("/auth/logout-all")
def logout_all(user_id: str, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            "DELETE FROM refresh_tokens WHERE user_id=%s",
            (user_id,)
        )

    return {"message": "Logged out from all devices"}


from models import RefreshRequest

@app.post("/auth/refresh")
def refresh_token(req: RefreshRequest, db=Depends(get_db)):
    with db.cursor() as cur:
        cur.execute(
            """
            SELECT user_id FROM refresh_tokens
            WHERE refresh_token=%s AND expires_at > NOW()
            """,
            (req.refresh_token,),
        )
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access = create_access_token(row["user_id"])
        return {"access_token": access}
