import sqlite3
import os

DB_PATH = "/data/crew_logs.db"
os.makedirs("/data", exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS log_muon_do (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    target TEXT,
    item TEXT,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS log_donate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    target TEXT,
    amount TEXT,
    time TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS log_xe_giap (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    target TEXT,
    vehicle TEXT,
    time TEXT
)
""")

conn.commit()
