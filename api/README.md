# Ocean Park 1 Eats — API

ReAct-agent-powered restaurant recommendation system for Ocean Park 1 residents.

## Quick Start

```bash
# 1. Install dependencies
pip install -r api/requirements.txt

# 2. Generate seed data (first time)
python scripts/generate_seed_data.py

# 3. Start the server
python api/app.py
# → http://localhost:8000
# → docs at http://localhost:8000/docs
```

## API Endpoints

### `POST /api/query`

Run the ReAct agent to get restaurant suggestions for a user query.

**Request:**

```json
{
  "query": "Giao nhanh",
  "location": "Ocean Park 1"
}
```

| Field    | Type   | Required | Description                     |
| -------- | ------ | -------- | ------------------------------- |
| `query`  | string | yes      | User's food request (1–500 chr) |
| `location` | string | no    | Delivery location (default: `"Ocean Park 1"`) |

**Response:**

```json
{
  "suggestions": [
    {
      "id": 20,
      "name": "Trà Chanh 1989",
      "vendor": "ShopeeFood",
      "predicted_eta": 11,
      "confidence": 0.87,
      "evidence_links": [
        "https://shopeefood.vn/ha-noi/tra-chanh-1989-ocp1",
        "https://www.facebook.com/groups/vinhomesocp1/permalink/12357/"
      ],
      "cuisine": "Đồ uống",
      "tags": ["giaonhanh", "giá-rẻ"]
    }
  ],
  "action_trace": [
    {
      "step": 1,
      "type": "think",
      "thought": "User wants: 'Giao nhanh' near Ocean Park 1..."
    },
    {
      "step": 2,
      "type": "action",
      "tool": "query_restaurants",
      "params": { "location": "Ocean Park 1", "max_wait_time": 45, "limit": 20 },
      "result": { "count": 20, "sample_ids": [20, 33, 18, 29, 16] }
    }
  ],
  "execution_time_ms": 3
}
```

| Field              | Type   | Description                              |
| ------------------ | ------ | ---------------------------------------- |
| `suggestions`      | array  | Ranked restaurant recommendations (≤ 2)  |
| `action_trace`     | array  | Step-by-step reasoning + tool calls      |
| `execution_time_ms` | int   | Total agent execution time in ms         |

Each suggestion contains:
- `id` — restaurant ID
- `name` — restaurant name
- `vendor` — delivery platform (ShopeeFood / GrabFood / Baemin)
- `predicted_eta` — estimated delivery time in minutes
- `confidence` — confidence score (0.0 – 0.95)
- `evidence_links` — URLs supporting the suggestion
- `cuisine` — cuisine category
- `tags` — descriptive tags

---

### `POST /api/feedback`

Submit feedback on a suggestion (helps improve future recommendations).

**Request:**

```json
{
  "query_text": "Giao nhanh",
  "suggestion_id": 20,
  "rating": 5,
  "feedback_text": "Tuyệt vời!"
}
```

| Field            | Type   | Required | Description                  |
| ---------------- | ------ | -------- | ---------------------------- |
| `query_text`     | string | yes      | Original user query          |
| `suggestion_id`  | int    | yes      | ID of the suggested restaurant |
| `rating`         | int    | yes      | Rating 1–5                   |
| `feedback_text`  | string | no       | Optional free-text feedback  |

**Response:**

```json
{
  "status": "ok",
  "feedback_id": 1
}
```

---

### `GET /api/health`

Health check and database connectivity verification.

**Response:**

```json
{
  "status": "ok",
  "version": "1.0.0-prototype",
  "database_restaurants_count": 37
}
```

## Interactive Docs

FastAPI auto-generates Swagger UI and ReDoc:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Architecture

```
api/
├── __init__.py         # Package init (empty)
├── app.py              # FastAPI app, middleware, startup
├── routes.py           # Endpoint handlers + Pydantic schemas
├── agent.py            # ReAct agent: reasoning loop + tool dispatch
├── db.py               # SQLite database helpers
├── version.py          # Version constants
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

### Agent Flow

```
User query
  → POST /api/query
    → ReActAgent.run(query, location)
      → [Think]    Reason about user intent
      → [Act]      query_restaurants() via DB
      → [Observe]  Collect results
      → [Act]      get_eta_estimate() + get_evidence() per restaurant
      → [Act]      Score & rank candidates
      → [Think]    Select top-K
      → Return { suggestions, action_trace, execution_time_ms }
```

### Database

The agent reads from `data/sample_data.sqlite` (SQLite) with tables:
- `restaurants` — restaurant catalog (37 restaurants)
- `eta_logs` — historical ETA records for confidence calibration
- `evidence_links` — supporting URLs per restaurant
- `feedback_submissions` — user feedback (written by `POST /api/feedback`)

## Production

```bash
# Run with uvicorn directly:
uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

CORS is configured to allow all origins (`*`) for development. Restrict in production.
