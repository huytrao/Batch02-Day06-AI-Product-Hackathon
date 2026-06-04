CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    vendor TEXT NOT NULL,
    eta_history_json TEXT,
    cuisine TEXT,
    tags TEXT,
    evidence_links TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS eta_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    eta INTEGER,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE IF NOT EXISTS feedback_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    suggestion_id INTEGER,
    rating INTEGER,
    feedback_text TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
);