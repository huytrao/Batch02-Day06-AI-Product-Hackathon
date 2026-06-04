"""
Executes the tools defined in api/tools.py against a sample SQLite/mock database.
"""
import sqlite3
import json
from typing import List, Dict, Any

# Setup an in-memory SQLite database for demonstration
conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = conn.cursor()

# Create sample tables
cursor.execute('''
CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT,
    base_prep_time INTEGER
)
''')
cursor.execute('''
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    suggestion_id INTEGER,
    user_rating INTEGER,
    feedback_text TEXT
)
''')

# Insert sample data
cursor.executemany('''
INSERT INTO restaurants (id, name, location, base_prep_time) VALUES (?, ?, ?, ?)
''', [
    (1, 'Quán A', 'Ocean Park 1', 20),
    (2, 'Quán B', 'Ocean Park 1', 15),
    (3, 'Quán C', 'Ocean Park 2', 25)
])
conn.commit()


def query_restaurants(location: str, max_wait_time: int) -> List[Dict[str, Any]]:
    # Simple logic: assume base_prep_time + 10 mins delivery <= max_wait_time
    cursor.execute(
        "SELECT id, name, location, base_prep_time FROM restaurants WHERE location = ?",
        (location,)
    )
    results = cursor.fetchall()
    candidates = []
    for row in results:
        r_id, name, loc, prep_time = row
        if prep_time + 10 <= max_wait_time:
            candidates.append({
                "id": r_id,
                "name": name,
                "location": loc,
                "estimated_wait": prep_time + 10
            })
    return candidates


def get_eta_estimate(restaurant_id: int) -> Dict[str, Any]:
    # Mocking an ETA engine
    cursor.execute("SELECT base_prep_time FROM restaurants WHERE id = ?", (restaurant_id,))
    row = cursor.fetchone()
    if row:
        prep_time = row[0]
        # ETA = prep_time + traffic_delay (mocked as 12)
        return {"predicted_eta": prep_time + 12, "confidence": 0.85}
    return {"error": "Restaurant not found"}


def get_evidence(restaurant_id: int) -> Dict[str, Any]:
    # Mock evidence
    if restaurant_id in [1, 2]:
        return {
            "source_links": [f"https://food-delivery.com/restaurant/{restaurant_id}"],
            "reviews": ["Đồ ăn ngon, giao nhanh", "Đóng gói cẩn thận"]
        }
    return {"error": "No evidence found"}


def record_feedback(query: str, suggestion_id: int, user_rating: int, feedback_text: str) -> Dict[str, Any]:
    cursor.execute(
        "INSERT INTO feedback (query, suggestion_id, user_rating, feedback_text) VALUES (?, ?, ?, ?)",
        (query, suggestion_id, user_rating, feedback_text)
    )
    conn.commit()
    return {"status": "success", "message": "Feedback recorded."}


def clarify(question: str) -> Dict[str, Any]:
    # In a real system, this would interrupt execution and prompt the user.
    # Here, we mock a simulated user response or system state.
    return {"status": "waiting_for_user", "question_asked": question}


TOOL_RUNNERS = {
    "query_restaurants": query_restaurants,
    "get_eta_estimate": get_eta_estimate,
    "get_evidence": get_evidence,
    "record_feedback": record_feedback,
    "clarify": clarify
}
