# Kế Hoạch Code — Hoàn Thành Prototype (Hackathon)

Mục tiêu: Phân công cụ thể các nhiệm vụ code để trong thời gian hackathon hoàn thành prototype web UI + backend (SQLite + API) và demo 3 phút.

Timeline ngắn (tính từ bắt đầu hackathon)
- T0: bắt đầu
- T+90 phút: dataset & evidence CSV hoàn thành
- T+150 phút: backend API cơ bản hoàn thành
- T+180 phút: frontend kết nối API và hiển thị
- T+210 phút: tích hợp, chạy 5 test case
- T+240 phút: hoàn thiện, rehearsal, nộp

Phân công nhiệm vụ code (chi tiết)

- Member A — Lê Hữu Đạt (Dataset Owner)
  - Nhiệm vụ: Tạo `02-group-spec/sample_data.csv` (schema: id, name, vendor, eta_history(json), tags, evidence_links) và script `scripts/import_sqlite.py` để load CSV vào `data/sample_data.sqlite`.
  - Deliverables: `02-group-spec/sample_data.csv`, `data/sample_data.sqlite`, `scripts/import_sqlite.py`.

- Member D — Nguyễn Đức Mạnh (Backend Owner)
  - Nhiệm vụ: Tạo REST API đơn giản trong `api/` (Flask or FastAPI). Endpoint chính: `GET /suggestions?location=...&limit=2` trả JSON: [{id,name,predicted_eta,confidence,reasons,source_links}].
  - Tối ưu: implement heuristic ranking using `eta_history` and recent reports.
  - Deliverables: `api/app.py`, `requirements.txt` (minimal), `api/README.md` với cách chạy.

- Member E — Trảo An Huy (Frontend Owner)
  - Nhiệm vụ: Xây `web/` static frontend (HTML/CSS/vanilla JS) gọi `/suggestions` và hiển thị: tên, predicted ETA, confidence badge, và links to sources; thêm button để mở deep-link tới app (simulated).
  - Deliverables: `web/index.html`, `web/styles.css`, `web/app.js`.

- Member C — Công Thái (Spec + UI Coordinator)
  - Nhiệm vụ: Định nghĩa payload API, mock requests/responses, thiết kế wireframe nhanh (PNG hoặc ASCII), viết `02-group-spec/build_slice.md` phần API contract và UI props.
  - Deliverables: updated `02-group-spec/build_slice.md`, `02-group-spec/ui_wireframe.png` (hoặc `.md`).

- Member B — Nguyễn Đông Anh (Evidence → Data)
  - Nhiệm vụ: Chuẩn hóa `02-group-spec/evidence_pack.md` thành CSV rows (`scripts/evidence_to_csv.py`) và gắn `evidence_links` vào `sample_data.csv`.
  - Deliverables: `scripts/evidence_to_csv.py`, updated `02-group-spec/sample_data.csv`.

Integration & QA
- Integration (Member D + E): nối frontend ↔ backend, ensure CORS and endpoints match.
- QA (all): chạy 5 test cases (happy, low-confidence, failure, correction, boundary) — lưu logs trong `02-group-spec/test_results.md`.

Repo & Run
- Member E (Repo Owner) sets up root `README.md` with quick start, and run scripts:

  - Python (backend):

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r api/requirements.txt
    python api/app.py
    ```

  - Static frontend: open `web/index.html` in browser or serve with `npx http-server web`.

Checklist (code-focused)
- [ ] `02-group-spec/sample_data.csv` ready and imported to SQLite
- [ ] `api/` serving `/suggestions` with heuristic ranking
- [ ] `web/` displays suggestions with ETA/confidence and sources
- [ ] 5 test cases executed and results documented
- [ ] `README.md` with run instructions

Quick notes
- Keep assumptions documented in each deliverable (data is simulated, ETA heuristic simple).  
- If time is tight: prioritize backend endpoint + single-page frontend that shows 2 suggestions from fake DB.

Ai muốn tôi tạo cấu trúc file starter cho một trong các phần trên (backend, frontend, scripts) thì nói phần nào, tôi sẽ khởi tạo ngay.
# Kế Hoạch Phân Việc (Code) — Hoàn thành Prototype Web UI

Mục tiêu: Phân công rõ ràng các nhiệm vụ code để hoàn thành prototype (SQLite + API + Web UI) và chuẩn bị demo 3 phút.

Tổng quan các nhiệm vụ chính (8 nhiệm vụ)

1) Prepare fake dataset & import — Member A (Lê Hữu Đạt)
   - Tạo `02-group-spec/sample_data.csv` gồm các cột: id, name, vendor, eta_sample_min, eta_sample_max, cuisine, tags, evidence_links
   - Viết script `scripts/import_csv_to_sqlite.py` để tạo `data/sample_data.sqlite` và import.
   - Deliverable: CSV mẫu + SQLite import script + `data/sample_data.sqlite`.

2) Implement backend API — Member D (Nguyễn Đức Mạnh)
   - Tạo API server (Python + Flask hoặc Node + Express) dưới thư mục `api/`.
   - Endpoint tối thiểu: `GET /suggestions?location=...&limit=2` trả JSON: [{id,name,pred_eta,confidence,rationale,sources}]
   - Đọc dữ liệu từ `data/sample_data.sqlite` và áp heuristic ranking (ETA trung bình, recent reports).
   - Deliverable: `api/app.py` (hoặc `index.js`) + `requirements.txt`/`package.json` + run script.

3) Build web frontend UI — Member E (Trảo An Huy)
   - Thư mục `web/` chứa `index.html`, `styles.css`, `app.js`.
   - Giao diện: input location, nút "Giao nhanh", hiển thị 2 gợi ý với ETA, confidence, nguồn (link), nút mở menu/redirect.
   - Kết nối AJAX tới `GET /suggestions` và xử lý lỗi / low-confidence badge.
   - Deliverable: `web/` folder sẵn demo chạy local.

4) Define UI/UX & endpoints — Member C (Công Thái)
   - Hoàn thiện payload request/response, xác định các trạng thái UI (happy, low-confidence, failure, correction).
   - Cập nhật `02-group-spec/build_slice.md` và thêm wireframe hoặc mô tả UI chi tiết.
   - Deliverable: API contract + UI states + updated `build_slice.md`.

5) Evidence ingestion script — Member B (Nguyễn Đông Anh)
   - Viết `scripts/evidence_to_csv.py` để chuyển `02-group-spec/evidence_pack.md` thành các hàng CSV (evidence_links, snippets).
   - Gắn evidence vào `sample_data.csv` field `evidence_links` (json list hoặc pipe-separated).
   - Deliverable: script + sample enriched CSV.

6) Integration & QA tests — Member D + E
   - Viết 5 test cases (happy, low-confidence, failure, correction, edge-case) và checklist.
   - Test end-to-end: từ `web/` → `api/` → `data/sample_data.sqlite`.
   - Deliverable: `tests/test_cases.md`, test logs, bug fixes.

7) Repo setup & run scripts — Member E
   - Thêm `README.md` (chạy local), `run_backend.sh` / `run_backend.ps1`, `run_frontend.sh` / `run_frontend.ps1`.
   - Tạo `requirements.txt` hoặc `package.json` cho dependencies.
   - Deliverable: Scripts + README hướng dẫn chạy nhanh.

8) Finalize & Demo rehearsal — All
   - Hợp nhất mọi file vào `02-group-spec/`, chạy rehearsal, chuẩn bị 3 phút demo script.
   - Deliverable: Final artifact folder và `02-group-spec/demo_script.txt`.

Tiêu chí hoàn thành (Definition of Done)
- API trả kết quả sample trong <2s với dataset mẫu
- Web UI hiển thị 2 gợi ý, ETA, confidence, và links nguồn
- Có 5 test case end-to-end passing (manual ok)
- README rõ ràng để bất kỳ thành viên nào cũng chạy demo local

Ghi chú & ưu tiên ngay bây giờ
- Ưu tiên số 1: Member A tạo `sample_data.csv` và script import — backend cần file này nhanh.
- Ưu tiên số 2: Member D code API stub dùng in-memory data nếu SQLite chưa sẵn.
- Nếu muốn, tôi có thể tạo ngay skeleton cho `scripts/import_csv_to_sqlite.py`, `api/app.py`, và `web/index.html`.

***
File này lưu ở root repo để cả team mở nhanh: `chiaviec_code.md`.
