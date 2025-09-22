import sqlite3

def create_tables():
    conn = sqlite3.connect("lawyers.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lawyers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        experience INTEGER NOT NULL,
        rating REAL,
        fees REAL,
        location TEXT,
        contact TEXT
    )
    """)
    
    conn.commit()
    conn.close()
