import sqlite3

conn = sqlite3.connect("hospital.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    gender TEXT,
    phone TEXT,
    result TEXT,
    confidence TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")