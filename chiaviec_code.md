# Kế Hoạch Code (reAct Agent) — Ocean Park 1 Eats Prototype

**Mục tiêu:** Xây dựng prototype **professional-ready** với reAct agent, UI tracing đầy đủ, feedback system, và monetization-ready design.

---

## Timeline & Milestones

- **T+60 phút**: Dataset hoàn thành, reAct agent core + first tool
- **T+120 phút**: API endpoints ready, UI skeleton started
- **T+180 phút**: Full UI + agent tracing display hoàn thành
- **T+210 phút**: Feedback system hoàn thành, integration test
- **T+240 phút**: Demo, final touches, rehearsal

---

## Phân Công (5 Người — Mỗi Người 1 Task Chính)

### 1. Member A — Lê Hữu Đạt — **Dataset & Data Infrastructure**

**Nhiệm vụ:** Tạo dataset mẫu, SQLite schema, và import pipeline — foundation cho agent data fetching.

**Input:**
- Evidence tính năng (ETA samples, venue info, tags, source links từ evidence_pack.md)
- Schema định nghĩa (restaurants, eta_history, feedback logs)

**Output:**
- `data/sample_data.csv` (30+ rows: id, name, vendor, eta_history_json, cuisine, tags, evidence_links)
- `data/schema.sql` (bảng restaurants, eta_logs, feedback_submissions)
- `data/sample_data.sqlite` (import hoàn thành)
- `scripts/import_csv_to_sqlite.py` (executable script)
- `data/README.md` (data format & schema notes)

**Acceptance Criteria:**
- SQLite có ≥30 restaurants với fields đầy đủ
- Mỗi record có `eta_history` (JSON array hoặc pipe-separated numbers)
- `evidence_links` với ≥2 links/record
- Script import chạy được: `python scripts/import_csv_to_sqlite.py`
- Query sample thành công: `SELECT COUNT(*) FROM restaurants` ≥ 30

**Timeline:** T+0 → T+60 phút

---

### 2. Member B — Nguyễn Đông Anh — **reAct Agent Core & Tools Implementation**

**Nhiệm vụ:** Implement reAct agent logic, tool definitions, và tool execution framework.

**Input:**
- reAct pattern spec (reasoning loop + action selection)
- Use case: user query "Giao nhanh ở Ocean Park 1" → agent reason → call tools → final answer
- Tool interfaces:
  - `query_restaurants` (params: location, max_wait_time) → list candidates
  - `get_eta_estimate` (params: restaurant_id) → predicted_eta, confidence
  - `get_evidence` (params: restaurant_id) → source links, reviews
  - `record_feedback` (params: query, suggestion_id, user_rating, feedback_text)
  - `clarify` (params: question) → user responds next turn

**Output:**
- `api/agent.py` (Agent class: think loop, tool selection, execution)
- `api/tools.py` (tool definitions + docstrings)
- `api/tool_runners.py` (execute tools on SQLite + feedback DB)
- `artifacts/tools.yaml` (tool registry with schemas)
- `artifacts/system_prompt.md` (reAct reasoning prompts)
- JSON example: action trace with step-by-step reasoning

**Action Trace Example Output:**
```json
{
  "query": "Giao nhanh ở Ocean Park 1",
  "action_trace": [
    {
      "step": 1,
      "type": "think",
      "thought": "User wants fast delivery near Ocean Park 1. I need to query restaurants and estimate delivery time."
    },
    {
      "step": 2,
      "type": "action",
      "tool": "query_restaurants",
      "params": {"location": "Ocean Park 1", "max_wait_time": 45},
      "result": [{"id": 1, "name": "Quán A", ...}, {"id": 2, "name": "Quán B", ...}]
    }
  ],
  "final_answer": {
    "suggestions": [
      {"id": 1, "name": "Quán A", "eta": 32, "confidence": 0.85}
    ]
  }
}
```

**Acceptance Criteria:**
- Agent outputs valid action_trace with ≥2 actions per query
- Tool calls contain correct params and get valid results
- Confidence score 0.0-1.0 and reasoning clear
- reAct loop completes in <2s for sample DB

**Timeline:** T+0 → T+120 phút

---

### 3. Member C — Công Thái — **Backend API & Tool Endpoints**

**Nhiệm vụ:** Implement REST API routes, serve agent via HTTP, connect tools to DB.

**Input:**
- Agent interface (từ Member B)
- API contract spec:
  - `POST /api/query` → {query, location} → {final_answer, suggestions, action_trace}
  - `POST /api/feedback` → {query, suggestion_id, rating, text} → {status}
  - Tool endpoints for agent internal use

**Output:**
- `api/app.py` (FastAPI server)
- `api/routes.py` (endpoint handlers)
- `api/db.py` (DB connection, queries)
- `api/requirements.txt` (dependencies)
- `api/README.md` (API docs)

**API Response Example:**
```json
POST /api/query
{"query": "Giao nhanh", "location": "Ocean Park 1"}

→ Response:
{
  "suggestions": [
    {"id": 1, "name": "Quán A", "predicted_eta": 32, "confidence": 0.85, "evidence_links": [...]}
  ],
  "action_trace": [...],
  "execution_time_ms": 1200
}
```

**Acceptance Criteria:**
- API server starts: `python api/app.py`
- `/api/query` returns valid JSON with action_trace in <2s
- `/api/feedback` accepts and logs feedback to DB
- CORS headers allow frontend access

**Timeline:** T+60 → T+180 phút

---

### 4. Member D — Nguyễn Đức Mạnh — **Frontend UI (Professional & Tracing-Ready)**

**Nhiệm vụ:** Build beautiful, professional UI với agent tracing visualization, confidence display, monetization signals.

**Input:**
- API contract (Member C)
- Design requirements: professional, responsive, trust signals, tracing display

**Output:**
- `web/index.html` (main page)
- `web/styles.css` (professional styling, responsive)
- `web/app.js` (fetch API, render UI, toggle tracing)
- `web/components.js` (card component, trace viewer)

**UI Components:**

1. **Suggestion Card**:
```
┌─────────────────────────────┐
│ 🍜 Quán A (GrabFood)        │
│ ⏱️ Dự kiến: 32 phút          │
│ ⭐ Độ tin cậy: Cao (85%)    │
│ 📍 [Link nguồn]  [Mở menu]   │
│ [Xem chi tiết]               │
└─────────────────────────────┘
```

2. **Agent Trace Viewer** (collapsible):
```
▼ Chi tiết quyết định (3 bước)
  [1] Tìm quán ở Ocean Park 1
  [2] Ước tính ETA từ lịch sử
  [3] Chọn 2 tốt nhất
```

**Acceptance Criteria:**
- UI responsive on mobile/desktop
- Render suggestions in <500ms
- Toggle to show/hide action trace
- Professional design
- Confidence badges: High (0.7-1.0), Medium (0.4-0.7), Low (<0.4)

**Timeline:** T+120 → T+210 phút

---

### 5. Member E — Trảo An Huy — **Feedback System & Monetization Layer**

**Nhiệm vụ:** Build feedback collection, analytics, user rating pipeline, monetization hooks.

**Input:**
- API interface (Member C)
- Use case: capture user behavior, continuous learning, retention

**Output:**
- `api/feedback_db.py` (feedback schema)
- `web/feedback-widget.js` (post-suggestion feedback form)
- `api/analytics.py` (aggregation: accuracy, NPS, trending)
- `data/feedback.sqlite` (persistent feedback logs)
- `scripts/generate_report.py` (weekly report)
- `api/monetization.py` (partner integration hooks)
- `README_FEEDBACK.md` (feedback workflow)

**Feedback Form** (after suggestion):
```
┌──────────────────────────────────┐
│ Kết quả có hữu ích không?        │
│ ⭐⭐⭐⭐⭐ [rating 1-5]          │
│ Bình luận (tùy chọn):            │
│ [text input]                     │
│ [Gửi] [Bỏ qua]                   │
└──────────────────────────────────┘
```

**Analytics Dashboard:**
- Accuracy rate: % suggestions → successful order
- NPS: likelihood to recommend
- Top queries (trending)
- Partner performance metrics

**Monetization Hooks:**
- `GET /api/partner-stats?partner=GrabFood` → metrics
- Framework for sponsored recommendations (transparent)

**Acceptance Criteria:**
- Feedback form appears after suggestion
- POST `/api/feedback` saves to feedback.sqlite
- Analytics script generates weekly JSON report
- Monetization hooks documented
- Privacy-compliant: no PII logged

**Timeline:** T+180 → T+240 phút

---

## Task Independence & No Conflict

| Person | Responsibility | Database Tables | API Routes | Frontend Modules |
|--------|-----------------|-----------------|-----------|-----------------|
| A      | Dataset & schema | restaurants, eta_logs | — | — |
| B      | reAct agent | — | — | — |
| C      | API server & routing | (read from A) | /api/query, /api/feedback | — |
| D      | UI rendering | — | (calls C) | index.html, app.js |
| E      | Feedback & analytics | feedback | /api/feedback, /api/analytics | feedback-widget.js |

**Key separation:** A owns data layer; B owns agent logic; C owns API; D owns UI; E owns feedback/monetization.

---

## Definition of Done (DoD)

**Member A:**
- [ ] `data/sample_data.sqlite` with 30+ valid records
- [ ] Import script runs without error

**Member B:**
- [ ] Agent produces action_trace with ≥2 steps per query
- [ ] All 5 tools declared and functional
- [ ] System prompt guides reasoning clearly

**Member C:**
- [ ] `/api/query` endpoint returns suggestions + action_trace
- [ ] `/api/feedback` saves to DB
- [ ] Server latency <2s

**Member D:**
- [ ] UI responsive (mobile/desktop)
- [ ] Suggestions render with all fields
- [ ] Action trace toggleable
- [ ] Professional design

**Member E:**
- [ ] Feedback form appears after suggestion
- [ ] Analytics report generated
- [ ] Monetization hooks documented
- [ ] Privacy compliant

---

## Integration Checklist

- [ ] Backend starts: `python api/app.py`
- [ ] Frontend loads: open `web/index.html`
- [ ] Submit query → agent produces trace
- [ ] UI displays suggestions + trace
- [ ] Submit feedback → saved to DB
- [ ] All 5 components working together

**Next step:** Each member starts their task independently. Sync points: T+60, T+120, T+180.
