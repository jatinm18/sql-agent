import sqlite3
import pathlib

DB_PATH = pathlib.Path("Chinook.db")

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError("Chinook.db not found. Run: python setup.py")
    return sqlite3.connect(DB_PATH)

def list_tables() -> list[str]:
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [row[0] for row in cursor.fetchall() if not row[0].startswith("sqlite_")]
    finally:
        con.close()