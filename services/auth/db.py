import pymysql
import os
import time

def get_db():
    retries = 10
    delay = 2

    for attempt in range(retries):
        try:
            conn = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            try:
                yield conn
            finally:
                conn.close()
            return
        except pymysql.err.OperationalError as e:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
