import sqlite3
import csv
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/sample_data.sqlite')
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/sample_data.csv')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '../data/schema.sql')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    return conn

def import_data(conn):
    cursor = conn.cursor()
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    if cursor.fetchone()[0] > 0:
        print("Data already exists. Skipping import.")
        return

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """
                INSERT INTO restaurants (name, vendor, eta_history_json, cuisine, tags, evidence_links, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row['name'],
                    row['vendor'],
                    row['eta_history_json'],
                    row['cuisine'],
                    row['tags'],
                    row['evidence_links'],
                    row['location']
                )
            )
            # Insert some fake logs based on eta_history
            restaurant_id = cursor.lastrowid
            etas = json.loads(row['eta_history_json'])
            for eta in etas:
                cursor.execute(
                    "INSERT INTO eta_logs (restaurant_id, eta) VALUES (?, ?)",
                    (restaurant_id, eta)
                )

    conn.commit()
    print("Data imported successfully.")

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = init_db()
    import_data(conn)
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    print(f"Total restaurants: {cursor.fetchone()[0]}")
    conn.close()