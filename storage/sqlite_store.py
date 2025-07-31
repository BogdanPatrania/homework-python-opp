# storage/sqlite_store.py

import sqlite3
from pathlib import Path
from math import log10

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

def digit_count(n: int) -> int:
    return int(log10(n)) + 1 if n > 0 else 1


# ...existing code...

def store_request_sqlite(operation: str, input_data: dict, result: int | float):
    try:
        # Try to convert result to string (may fail for huge ints)
        result_str = str(result)
    except ValueError:
        # If too large, store a message or just the digit count
        if isinstance(result, int):
            result_str = f"[int with {digit_count(result)} digits]"
        else:
            result_str = "[unrepresentable result]"
    except Exception as e:
        # Catch-all for any other conversion errors
        result_str = f"[error: {str(e)}]"
    print(f"[SQLITE] Writing: {operation=}, {input_data=}, result has {digit_count(result) if isinstance(result, int) else 'N/A'} digits")
    print(f"[SQLITE] Using DB: {DB_FILE.resolve()}")
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO requests (operation, input_data, result)
            VALUES (?, ?, ?)
        """, (operation, str(input_data), result_str))

def get_all_requests_sqlite():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT id, operation, input_data, result, timestamp
            FROM requests
            ORDER BY timestamp DESC
        """)
        return cursor.fetchall()
