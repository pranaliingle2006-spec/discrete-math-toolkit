import sqlite3

DB_NAME = "discrete_math_toolkit.db"

def init_db(db_path: str = DB_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module TEXT NOT NULL,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_record(module: str, expression: str, result: str, db_path: str = DB_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (module, expression, result) VALUES (?, ?, ?)",
        (module, expression, result)
    )
    conn.commit()
    conn.close()

def get_recent_history(limit: int = 10, db_path: str = DB_NAME):
    """Retrieves the latest calculation records from SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, module, expression, result, timestamp FROM history ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    records = cursor.fetchall()
    conn.close()
    return records