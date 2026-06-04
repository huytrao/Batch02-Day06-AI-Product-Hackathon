# Kế hoạch Triển khai Dự án (Project Plan)

Dựa trên cấu trúc phân công 5 thành viên cho dự án "Ocean Park 1 — Aggregated Dining Info" (Slice B: Fast Delivery Suggestion).

## 1. Phân Công & Nhiệm Vụ (5 Người)

### Member A — Lê Hữu Đạt — **Dataset & Data Infrastructure**
- **Nhiệm vụ:** Tạo dataset mẫu, SQLite schema, và import pipeline — foundation cho agent data fetching.
- **Output:** 
  - `data/sample_data.csv` (30+ rows: id, name, vendor, eta_history_json, cuisine, tags, evidence_links)
  - `data/schema.sql` (bảng restaurants, eta_logs, feedback_submissions)
  - `data/sample_data.sqlite` (import hoàn thành)
  - `scripts/import_csv_to_sqlite.py` (executable script)
  - `data/README.md` (data format & schema notes)
- **Timeline:** T+0 → T+60 phút.

### Member B — Nguyễn Đông Anh — **reAct Agent Core & Tools Implementation**
- **Nhiệm vụ:** Implement reAct agent logic, tool definitions, và tool execution framework.
- **Output:**
  - `api/agent.py` (Agent class: think loop, tool selection, execution)
  - `api/tools.py` (tool definitions + docstrings)
  - `api/tool_runners.py` (execute tools on SQLite + feedback DB)
  - `artifacts/tools.yaml` (tool registry with schemas)
  - `artifacts/system_prompt.md` (reAct reasoning prompts)
- **Timeline:** T+0 → T+120 phút.

### Member C — Công Thái — **Backend API & Tool Endpoints**
- **Nhiệm vụ:** Implement REST API routes, serve agent via HTTP, connect tools to DB.
- **Output:**
  - `api/app.py` (FastAPI server)
  - `api/routes.py` (endpoint handlers)
  - `api/db.py` (DB connection, queries)
  - `api/requirements.txt` (dependencies)
  - `api/README.md` (API docs)
- **Timeline:** T+60 → T+180 phút.

### Member D — Nguyễn Đức Mạnh — **Frontend UI (Professional & Tracing-Ready)**
- **Nhiệm vụ:** Build beautiful, professional UI với agent tracing visualization, confidence display, monetization signals.
- **Output:**
  - `web/index.html` (main page)
  - `web/styles.css` (professional styling, responsive)
  - `web/app.js` (fetch API, render UI, toggle tracing)
  - `web/components.js` (card component, trace viewer)
- **Timeline:** T+120 → T+210 phút.

### Member E — Trảo An Huy — **Feedback System & Monetization Layer**
- **Nhiệm vụ:** Build feedback collection, analytics, user rating pipeline, monetization hooks.
- **Output:**
  - `api/feedback_db.py` (feedback schema)
  - `web/feedback-widget.js` (post-suggestion feedback form)
  - `api/analytics.py` (aggregation: accuracy, NPS, trending)
  - `data/feedback.sqlite` (persistent feedback logs)
  - `scripts/generate_report.py` (weekly report)
  - `api/monetization.py` (partner integration hooks)
  - `README_FEEDBACK.md` (feedback workflow)
- **Timeline:** T+180 → T+240 phút.

## 2. Tính Độc Lập và Tương Tác

| Người | Trách nhiệm | Bảng CSDL (DB Tables) | API Routes | Module Frontend |
|---|---|---|---|---|
| A | Dataset & schema | restaurants, eta_logs | — | — |
| B | reAct agent | — | — | — |
| C | API server & routing | (đọc từ A) | /api/query, /api/feedback | — |
| D | UI rendering | — | (gọi API của C) | index.html, app.js |
| E | Feedback & analytics | feedback | /api/feedback, /api/analytics | feedback-widget.js |

**Chốt tương tác (Key separation):**
- A quản lý tầng dữ liệu (Data layer).
- B quản lý logic Agent.
- C quản lý API kết nối B với Frontend.
- D quản lý Giao diện hiển thị (UI).
- E quản lý luồng dữ liệu phản hồi/phân tích (Feedback & Analytics).

## 3. Definition of Done (DoD)

- **Member A:** `data/sample_data.sqlite` với ≥30 bản ghi hợp lệ; script import chạy không lỗi.
- **Member B:** Agent sinh ra `action_trace` với ≥2 bước mỗi truy vấn; 5 tool hoạt động tốt; system prompt dẫn dắt reasoning chuẩn.
- **Member C:** API `/api/query` trả về gợi ý + action_trace; `/api/feedback` lưu DB; latency < 2s.
- **Member D:** UI responsive, render đầy đủ thông tin gợi ý và trace toggle; thiết kế chuyên nghiệp.
- **Member E:** Form feedback hiển thị sau gợi ý; script analytics chạy ra report; hook monetization được tài liệu hoá; bảo mật privacy.

## 4. Checklist Tích Hợp (Integration)

- [ ] Backend khởi động thành công: `python api/app.py`
- [ ] Frontend tải thành công: mở `web/index.html`
- [ ] Gửi truy vấn → Agent sinh ra trace hợp lệ
- [ ] UI hiển thị gợi ý + action_trace rõ ràng
- [ ] Gửi phản hồi (Feedback) → Lưu thành công vào DB
- [ ] Tất cả 5 thành phần hoạt động trơn tru với nhau
