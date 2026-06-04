import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "restaurants.sqlite"


SAMPLE_RESTAURANTS = [
    (
        1,
        "Quán A - Phở Nhanh Ocean",
        "Ocean Park 1",
        "pho",
        4.6,
        32000,
        32,
        0.85,
        1,
        "Fast delivery near Ocean Park 1 with many lunch reviews.",
        "https://example.com/restaurants/quan-a",
    ),
    (
        2,
        "Quán B - Bún Bò 45",
        "Ocean Park 1",
        "bun bo",
        4.4,
        38000,
        38,
        0.80,
        1,
        "Good delivery reliability and affordable meals.",
        "https://example.com/restaurants/quan-b",
    ),
    (
        3,
        "Cơm Chay An Lạc",
        "VinUni",
        "vegetarian",
        4.7,
        30000,
        26,
        0.90,
        1,
        "Vegetarian menu with quick delivery around VinUni.",
        "https://example.com/restaurants/com-chay-an-lac",
    ),
    (
        4,
        "Lẩu Thái 5 Anh Em",
        "Ocean Park 2",
        "hotpot",
        4.5,
        120000,
        45,
        0.78,
        1,
        "Group-friendly hotpot option with stable evening demand.",
        "https://example.com/restaurants/lau-thai-5-anh-em",
    ),
    (
        5,
        "Al Fresco's Ocean",
        "Ocean Park 1",
        "european",
        4.1,
        150000,
        None,
        0.25,
        0,
        "Opening hours and delivery ETA are uncertain late at night.",
        "https://example.com/restaurants/al-frescos-ocean",
    ),
    (
        6,
        "Cơm Tấm Sài Gòn OP1",
        "Ocean Park 1",
        "com tam",
        4.5,
        35000,
        25,
        0.88,
        1,
        "Popular broken rice spot with fast delivery and student-friendly prices.",
        "https://example.com/restaurants/com-tam-saigon",
    ),
    (
        7,
        "Bún Chả Hà Nội S1",
        "Ocean Park 1",
        "bun cha",
        4.3,
        40000,
        30,
        0.82,
        1,
        "Authentic Hanoi bun cha with consistent quality and quick service.",
        "https://example.com/restaurants/bun-cha-hanoi",
    ),
    (
        8,
        "Bánh Mì Anh Đông",
        "Ocean Park 1",
        "banh mi",
        4.8,
        20000,
        15,
        0.92,
        1,
        "Best banh mi in the area, very fast delivery under 20 minutes.",
        "https://example.com/restaurants/banh-mi-anh-dong",
    ),
    (
        9,
        "Trà Sữa ToCoToCo OP1",
        "Ocean Park 1",
        "tra sua",
        4.2,
        35000,
        20,
        0.75,
        1,
        "Popular milk tea chain with reliable delivery times.",
        "https://example.com/restaurants/tocotoco-op1",
    ),
    (
        10,
        "Cơm Văn Phòng Nhà Mình",
        "Ocean Park 1",
        "com van phong",
        4.6,
        45000,
        28,
        0.87,
        1,
        "Home-style office lunch boxes with diverse daily menu.",
        "https://example.com/restaurants/com-van-phong",
    ),
    (
        11,
        "Gà Rán Crispy OP1",
        "Ocean Park 1",
        "ga ran",
        4.4,
        55000,
        22,
        0.83,
        1,
        "Crispy fried chicken with fast delivery, popular with families.",
        "https://example.com/restaurants/ga-ran-crispy",
    ),
    (
        12,
        "Mì Quảng Bà Năm",
        "Ocean Park 1",
        "mi quang",
        4.7,
        42000,
        35,
        0.79,
        1,
        "Authentic Mi Quang from Da Nang, generous portions.",
        "https://example.com/restaurants/mi-quang-ba-nam",
    ),
]


def _connect():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            rating REAL NOT NULL,
            avg_price INTEGER NOT NULL,
            predicted_eta INTEGER,
            confidence REAL NOT NULL,
            is_open INTEGER NOT NULL,
            evidence_summary TEXT NOT NULL,
            source_url TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            suggestion_id INTEGER NOT NULL,
            user_rating INTEGER NOT NULL,
            feedback_text TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    count = conn.execute("SELECT COUNT(*) AS count FROM restaurants").fetchone()["count"]
    if count == 0:
        conn.executemany(
            """
            INSERT INTO restaurants (
                id, name, location, cuisine, rating, avg_price, predicted_eta,
                confidence, is_open, evidence_summary, source_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            SAMPLE_RESTAURANTS,
        )
    conn.commit()


def _row_to_restaurant(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "location": row["location"],
        "cuisine": row["cuisine"],
        "rating": row["rating"],
        "avg_price": row["avg_price"],
        "predicted_eta": row["predicted_eta"],
        "confidence": max(0.0, min(1.0, row["confidence"])),
        "is_open": bool(row["is_open"]),
    }


def query_restaurants(location, max_wait_time=None):
    """Return restaurant candidates filtered by location and optional ETA limit."""
    # Normalize: strip sub-location like "Ocean Park 1 - S1.06" → try both full and base
    loc_lower = location.lower().strip()
    base_loc = loc_lower.split(" - ")[0].strip()

    with _connect() as conn:
        sql = "SELECT * FROM restaurants WHERE (lower(location) LIKE ? OR lower(location) LIKE ?)"
        params = [f"%{loc_lower}%", f"%{base_loc}%"]
        if max_wait_time is not None:
            sql += " AND (predicted_eta IS NULL OR predicted_eta <= ?)"
            params.append(int(max_wait_time))
        sql += " ORDER BY is_open DESC, confidence DESC, rating DESC LIMIT 5"
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_restaurant(row) for row in rows]


def get_eta_estimate(restaurant_id):
    """Return predicted delivery ETA and confidence for one restaurant."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, predicted_eta, confidence FROM restaurants WHERE id = ?",
            (int(restaurant_id),),
        ).fetchone()
    if row is None:
        return {"restaurant_id": restaurant_id, "predicted_eta": None, "confidence": 0.0}
    return {
        "restaurant_id": row["id"],
        "predicted_eta": row["predicted_eta"],
        "confidence": max(0.0, min(1.0, row["confidence"])),
    }


def get_evidence(restaurant_id):
    """Return source links and review evidence for one restaurant."""
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT id, name, rating, evidence_summary, source_url
            FROM restaurants
            WHERE id = ?
            """,
            (int(restaurant_id),),
        ).fetchone()
    if row is None:
        return {"restaurant_id": restaurant_id, "source_links": [], "reviews": []}
    return {
        "restaurant_id": row["id"],
        "source_links": [row["source_url"]],
        "reviews": [
            {
                "restaurant": row["name"],
                "rating": row["rating"],
                "summary": row["evidence_summary"],
            }
        ],
    }


def record_feedback(query, suggestion_id, user_rating, feedback_text=""):
    """Persist user feedback for future evaluation."""
    rating = int(user_rating)
    if rating < 1 or rating > 5:
        raise ValueError("user_rating must be an integer from 1 to 5")

    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO feedback (query, suggestion_id, user_rating, feedback_text)
            VALUES (?, ?, ?, ?)
            """,
            (query, int(suggestion_id), rating, feedback_text or ""),
        )
        conn.commit()
        feedback_id = cursor.lastrowid
    return {"status": "recorded", "feedback_id": feedback_id}


def clarify(question):
    """Return a clarification request for the next user turn."""
    return {
        "needs_clarification": True,
        "question": question,
        "instruction": "Ask the user this question before calling search tools.",
    }


TOOL_RUNNERS = {
    "query_restaurants": query_restaurants,
    "get_eta_estimate": get_eta_estimate,
    "get_evidence": get_evidence,
    "record_feedback": record_feedback,
    "clarify": clarify,
}


def execute_tool(tool_name, params):
    """Dispatch a named tool call with JSON params."""
    if tool_name not in TOOL_RUNNERS:
        raise ValueError(f"Unknown tool: {tool_name}")
    if not isinstance(params, dict):
        raise ValueError("Tool params must be a JSON object")
    return TOOL_RUNNERS[tool_name](**params)
