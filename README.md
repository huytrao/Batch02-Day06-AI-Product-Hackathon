# Ocean Park 1 Eats — API

# Tên thành viên

Lưu Công Thái - 2A202600949
Nguyễn Đông Anh - 2A20600760
Lê Hữu Đạt - 2A202600630
Nguyễn Đức Mạnh - 2A20260724
Trảo An Huy - 2A202600819

API server for Ocean Park 1 Eats, một prototype đề xuất quán ăn giao nhanh tại Ocean Park 1.

## Quick Start

Sau khi chạy, truy cập:
- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment

Optional nếu bạn muốn gọi model trực tiếp từ backend:
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL` (mặc định `https://api.openai.com/v1`)
- `OPENAI_MODEL` (mặc định `gpt-3.5-turbo`)
- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL` (mặc định `https://openrouter.ai/api/v1`)
- `OPENROUTER_MODEL` (mặc định `openai/gpt-4o-mini`)

## API Endpoints

### `POST /api/query`

Chạy ReAct agent để lấy gợi ý quán ăn theo query của người dùng.

**Request:**

```json
{
  "query": "Giao nhanh",
  "location": "Ocean Park 1"
}
```

| Field       | Type   | Required | Description                                    |
| ----------- | ------ | -------- | ---------------------------------------------- |
| `query`     | string | yes      | Yêu cầu của người dùng                         |
| `location`  | string | no       | Vị trí giao hàng (mặc định: `Ocean Park 1`)    |

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
        "https://shopeefood.vn/...",
        "https://facebook.com/..."
      ],
      "cuisine": "Đồ uống",
      "tags": ["Giao nhanh", "Giá rẻ"]
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

| Field               | Type   | Description                                |
| ------------------- | ------ | ------------------------------------------ |
| `suggestions`       | array  | Gợi ý quán ăn được xếp hạng                |
| `action_trace`      | array  | Lịch sử suy nghĩ và tool call của agent     |
| `execution_time_ms` | int    | Thời gian thực hiện agent (ms)             |

Mỗi suggestion chứa:
- `id` — ID nhà hàng
- `name` — tên nhà hàng
- `vendor` — nền tảng giao hàng
- `predicted_eta` — ETA dự đoán (phút)
- `confidence` — độ tin cậy
- `evidence_links` — nguồn chứng thực
- `cuisine` — loại ẩm thực
- `tags` — nhãn hỗ trợ

---

### `POST /api/model`

Gửi prompt đến model AI nếu bạn muốn thử call trực tiếp.

**Request:**

```json
{
  "prompt": "Tóm tắt lại 3 quán ăn giao nhanh gần Ocean Park 1",
  "model": "gpt-3.5-turbo",
  "temperature": 0.2
}
```

| Field       | Type    | Required | Description                                 |
| ----------- | ------- | -------- | ------------------------------------------- |
| `prompt`    | string  | yes      | Nội dung gửi cho model                      |
| `model`     | string  | no       | Model override                               |
| `temperature` | number | no      | Độ ngẫu nhiên của model                      |

**Response:**

```json
{
  "output": "...",
  "model": "gpt-3.5-turbo",
  "usage": { ... }
}
```

---

### `POST /api/feedback`

Gửi phản hồi cho gợi ý đã nhận.

**Request:**

```json
{
  "query": "Giao nhanh",
  "suggestion_id": 20,
  "user_rating": 5,
  "feedback_text": "Rất phù hợp!"
}
```

| Field           | Type   | Required | Description                           |
| --------------- | ------ | -------- | ------------------------------------- |
| `query`         | string | yes      | Query ban đầu của người dùng          |
| `suggestion_id` | int    | yes      | ID gợi ý được phản hồi                |
| `user_rating`   | int    | yes      | Điểm 1–5                             |
| `feedback_text` | string | no       | Ghi chú thêm                         |

**Response:**

```json
{
  "status": "ok",
  "feedback_id": 1
}
```

---

### `GET /api/health`

Kiểm tra tình trạng API và kết nối database.

**Response:**

```json
{
  "status": "ok",
  "version": "1.0.0-prototype",
  "database_restaurants_count": 37
}
```

## Interactive Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Kiến trúc

```
api/
├── __init__.py        # Package init
├── app.py             # FastAPI app + CORS + startup checks
├── routes.py          # Endpoint handler + Pydantic schema
├── agent.py           # ReAct agent logic + tool calls
├── db.py              # SQLite helper, query logic
├── model.py           # Optional model call wrapper
├── version.py         # Version constant
├── requirements.txt   # Python dependencies
└── README.md          # Tài liệu này
```

## Luồng agent

```
User query
  → POST /api/query
    → ReActAgent.run(query, location)
      → [Think]    Hiểu intent người dùng
      → [Act]      query_restaurants() từ DB
      → [Observe]  Thu thập kết quả
      → [Act]      get_eta_estimate() + get_evidence()
      → [Act]      Score & rank
      → [Think]    Chọn top suggestions
      → Return { suggestions, action_trace, execution_time_ms }
```

## Database

Backend đọc dữ liệu từ `data/sample_data.sqlite` với các bảng:
- `restaurants` — danh sách nhà hàng
- `eta_logs` — lịch sử ETA để tính độ tin cậy
- `feedback_submissions` — lưu phản hồi người dùng

## Chạy production

```bash
uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

> Lưu ý: CORS hiện đang mở (`*`) cho mục đích phát triển. Nếu deploy thật thì cần hạn chế origin.