import sqlite3
from datetime import datetime

DB_PATH = "cravify.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            addiction_type TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            emotion TEXT NOT NULL,
            unmet_need TEXT NOT NULL,
            relapsed INTEGER NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intensity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            minute INTEGER NOT NULL,
            intensity INTEGER NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)

    conn.commit()
    conn.close()

def create_user(name, addiction_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, addiction_type, created_at) VALUES (?, ?, ?)",
        (name, addiction_type, datetime.now().isoformat())
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    return user

def log_session(user_id, emotion, unmet_need, relapsed, notes=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO sessions 
        (user_id, timestamp, emotion, unmet_need, relapsed, notes) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, datetime.now().isoformat(), emotion, unmet_need, relapsed, notes)
    )
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id

def log_intensity(session_id, minute, intensity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO intensity_log (session_id, minute, intensity) VALUES (?, ?, ?)",
        (session_id, minute, intensity)
    )
    conn.commit()
    conn.close()

def get_all_sessions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM sessions WHERE user_id = ? ORDER BY timestamp DESC",
        (user_id,)
    )
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def get_intensity_log(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT minute, intensity FROM intensity_log WHERE session_id = ? ORDER BY minute",
        (session_id,)
    )
    log = cursor.fetchall()
    conn.close()
    return log

def get_streak(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT DATE(timestamp), MIN(relapsed) 
        FROM sessions 
        WHERE user_id = ? 
        GROUP BY DATE(timestamp) 
        ORDER BY DATE(timestamp) DESC""",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    streak = 0
    for row in rows:
        if row[1] == 0:
            streak += 1
        else:
            break
    return streak

if __name__ == "__main__":
    create_tables()
    print("Database created successfully.")



