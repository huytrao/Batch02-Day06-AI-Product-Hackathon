#!/usr/bin/env python3
"""
Import sample_data.csv into sample_data.sqlite.
Usage: python scripts/import_csv_to_sqlite.py

Reads: data/sample_data.csv
Writes: data/sample_data.sqlite
"""

import csv
import json
import sqlite3
import os

DATADIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_PATH = os.path.join(DATADIR, "sample_data.csv")
DB_PATH = os.path.join(DATADIR, "sample_data.sqlite")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    vendor TEXT NOT NULL DEFAULT 'GrabFood',
    cuisine TEXT,
    tags TEXT,
    open_time TEXT,
    close_time TEXT,
    base_eta INTEGER DEFAULT 30,
    rating REAL DEFAULT 0.0,
    review_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS eta_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    eta INTEGER NOT NULL,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE IF NOT EXISTS feedback_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_text TEXT,
    suggestion_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    label TEXT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
"""


def import_csv_to_sqlite():
    if not os.path.exists(CSV_PATH):
        print(f"✗ CSV not found: {CSV_PATH}")
        print("  Run `python scripts/generate_seed_data.py` first.")
        return False

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r_id = int(row["id"])
            conn.execute(
                """INSERT INTO restaurants (id, name, vendor, cuisine, tags, open_time, close_time, base_eta, rating, review_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (r_id, row["name"], row["vendor"], row["cuisine"], row["tags"],
                 row["open_time"], row["close_time"], int(row["base_eta"]),
                 float(row["rating"]), int(row["review_count"]))
            )

            # Parse eta_history JSON array
            eta_history = json.loads(row["eta_history"])
            for eta_val in eta_history:
                conn.execute(
                    "INSERT INTO eta_logs (restaurant_id, eta) VALUES (?, ?)",
                    (r_id, eta_val)
                )

            # Parse evidence_links (pipe-separated)
            ev_links = row["evidence_links"].split("|")
            for i, url in enumerate(ev_links):
                url = url.strip()
                if url:
                    conn.execute(
                        "INSERT INTO evidence_links (restaurant_id, url, label) VALUES (?, ?, ?)",
                        (r_id, url, f"source_{i+1}")
                    )

    conn.commit()
    conn.close()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
    eta_count = conn.execute("SELECT COUNT(*) FROM eta_logs").fetchone()[0]
    ev_count = conn.execute("SELECT COUNT(*) FROM evidence_links").fetchone()[0]
    conn.close()

    print(f"✓ Imported to {DB_PATH}")
    print(f"  - {count} restaurants")
    print(f"  - {eta_count} eta_logs")
    print(f"  - {ev_count} evidence_links")
    return True


if __name__ == "__main__":
    import_csv_to_sqlite()
