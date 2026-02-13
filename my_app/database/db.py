# database/db.py
import sqlite3
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "legal_advisor.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Create Lawyers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lawyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            experience INTEGER,
            rating REAL,
            fees REAL,
            location TEXT,
            contact TEXT
        )
    """)

    # 2. Create Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    # 3. Create Default Admin (SECURE VERSION)
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        # Get password strictly from Environment Variable
        admin_plain_pass = os.getenv("ADMIN_PASSWORD")
        
        if admin_plain_pass:
            # Hash the secure password
            admin_pass_hash = hashlib.sha256(admin_plain_pass.encode()).hexdigest()
            
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           ("admin", admin_pass_hash, "admin"))
            print("✅ Admin account created using secure credentials.")
        else:
            print("⚠️ WARNING: 'ADMIN_PASSWORD' not found in environment variables.")
            print("   -> Admin account was NOT created. Please set the variable in .env or Streamlit Secrets.")

    conn.commit()
    conn.close()

# --- HELPER FUNCTIONS FOR AUTH ---

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role="user"):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Username already exists
    finally:
        conn.close()

def verify_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return user[0] # Return the role (e.g., 'admin' or 'user')
    return None