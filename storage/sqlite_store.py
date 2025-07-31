# storage/sqlite_store.py

import sqlite3
from pathlib import Path

DB_FILE = Path("storage") / "math_requests.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                input_data TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def store_request_sqlite(operation: str, input_data: dict, result: int | float):
    print(f"[SQLITE] Writing: {operation=}, {input_data=}, {result=}")
    print(f"[SQLITE] Using DB: {DB_FILE.resolve()}")
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO requests (operation, input_data, result)
            VALUES (?, ?, ?)
        """, (operation, str(input_data), str(result)))

def get_all_requests_sqlite():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT id, operation, input_data, result, timestamp
            FROM requests
            ORDER BY timestamp DESC
        """)
        return cursor.fetchall()
    
def get_all_requests_sqlite():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT id, operation, input_data, result, timestamp
            FROM requests
            ORDER BY timestamp DESC
        """)
        return cursor.fetchall()
