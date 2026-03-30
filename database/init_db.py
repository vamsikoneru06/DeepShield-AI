import sqlite3

conn = sqlite3.connect('deepshield.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    file_type TEXT,
    result TEXT,
    confidence_score REAL,
    risk_level TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ DB Ready")