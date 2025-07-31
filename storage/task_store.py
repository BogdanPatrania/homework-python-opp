import sqlite3
from pathlib import Path
from datetime import datetime
from math import log10

DB_FILE = Path("storage") / "background_tasks.db"

def init_task_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                operation TEXT,
                input_data TEXT,
                result TEXT,
                status TEXT,
                created_at TEXT
            )
        """)

def save_task(task_id, operation, input_data):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO tasks (task_id, operation, input_data, status, created_at)
            VALUES (?, ?, ?, 'queued', ?)
        """, (task_id, operation, str(input_data), datetime.utcnow().isoformat()))

def update_task_status(task_id, status):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            UPDATE tasks SET status = ? WHERE task_id = ?
        """, (status, task_id))

def digit_count(n: int) -> int:
    try:
        return int(log10(n)) + 1 if isinstance(n, int) and n > 0 else len(str(n))
    except Exception:
        return -1

def summarize_result(result, max_digits=3000):
    try:
        s = str(result)
        if len(s) > max_digits:
            return f"{s[:max_digits]}... [truncated, {len(s)} digits]"
        return s
    except ValueError:
        if isinstance(result, int):
            return f"[int with {digit_count(result)} digits]"
        return "[unrepresentable result]"
    except Exception as e:
        return f"[error: {str(e)}]"

def update_task_result(task_id, result):
    result_str = summarize_result(result)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            UPDATE tasks SET result = ?, status = 'done' WHERE task_id = ?
        """, (result_str, task_id))


def get_task(task_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT task_id, status, result FROM tasks WHERE task_id = ?
        """, (task_id,))
        row = cursor.fetchone()
        if row:
            return {"task_id": row[0], "status": row[1], "result": row[2]}
        return None

def get_all_tasks():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("""
            SELECT task_id, operation, input_data, status, result FROM tasks
            ORDER BY created_at DESC
        """)
        return [
            {
                "task_id": row[0],
                "operation": row[1],
                "input": row[2],
                "status": row[3],
                "result": row[4]
            }
            for row in cursor.fetchall()
        ]