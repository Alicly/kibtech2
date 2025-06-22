import sqlite3

# Path to your SQLite database
DB_PATH = 'app.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("DROP TABLE IF EXISTS system_settings;")
    print("Dropped system_settings table if it existed.")
except Exception as e:
    print("Error:", e)

conn.commit()
conn.close() 