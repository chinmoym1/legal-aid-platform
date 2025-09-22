import sqlite3
from database.models import create_tables

DB_NAME = "lawyers.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    create_tables()
