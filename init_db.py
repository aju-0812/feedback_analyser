import sqlite3

DB_NAME = "feedback.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    business TEXT,
    industry TEXT,
    password TEXT NOT NULL
);
""")

print("✅ Users table created successfully in feedback.db")

conn.commit()
conn.close()
