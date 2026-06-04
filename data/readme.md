# Ocean Park 1 Eats — Data Infrastructure Documentation

## Cấu trúc thư mục dữ liệu

```
data/
├── schema.sql          # Định nghĩa bảng cho toàn bộ hệ thống (restaurants, eta_logs, feedback_submissions)
├── sample_data.csv     # Tập dữ liệu thô gồm 35 nhà hàng với tag và lịch sử ETA
├── sample_data.sqlite  # Cơ sở dữ liệu SQLite chính (được tạo tự động bởi import script)
└── readme.md           # File này

scripts/
└── import_csv_to_sqlite.py   # Script import CSV → SQLite
```

## Các bảng trong Schema

### `restaurants`
| Cột | Kiểu | Mô tả |
|-----|------|--------|
| id | INTEGER PK | ID duy nhất của quán |
| name | TEXT | Tên quán ăn |
| vendor | TEXT | Nền tảng giao đồ ăn (GrabFood, ShopeeFood) |
| eta_history_json | TEXT | Mảng JSON lịch sử ETA (phút), ví dụ: `[30, 35, 32, 40, 28]` |
| cuisine | TEXT | Loại ẩm thực (Phở, Bún, Cơm, Ăn vặt...) |
| tags | TEXT | Nhãn phụ phân tách bằng dấu phẩy |
| evidence_links | TEXT | ≥2 link minh chứng phân tách bằng dấu phẩy (FB/Google Maps) |
| is_active | INTEGER | Trạng thái hoạt động (1: Mở cửa, 0: Đóng cửa) |

### `eta_logs`
Ghi log mỗi lần Agent gọi ETA estimate — phục vụ phân tích độ chính xác theo thời gian.

| Cột | Kiểu | Mô tả |
|-----|------|--------|
| id | INTEGER PK | ID tự tăng |
| restaurant_id | INTEGER FK | Liên kết tới restaurants.id |
| requested_at | TIMESTAMP | Thời điểm gọi |
| predicted_eta | INTEGER | ETA dự đoán (phút) |
| confidence_score | REAL | Độ tin cậy 0.0–1.0 |

### `feedback_submissions`
Thu thập phản hồi người dùng sau mỗi gợi ý — phục vụ Member E (Feedback System).

| Cột | Kiểu | Mô tả |
|-----|------|--------|
| id | INTEGER PK | ID tự tăng |
| query | TEXT | Câu hỏi gốc của người dùng |
| suggestion_id | INTEGER FK | Liên kết tới restaurants.id |
| user_rating | INTEGER | Đánh giá 1–5 sao |
| feedback_text | TEXT | Bình luận tự do (tùy chọn) |
| created_at | TIMESTAMP | Thời điểm gửi phản hồi |

## Định dạng dữ liệu quan trọng

### `eta_history_json`
Lưu dạng JSON Array chứa chuỗi số nguyên (đơn vị: phút).

```json
[30, 35, 32, 40, 28]
```

**Hướng dẫn cho Member B (Agent):** Parse trường này bằng `json.loads()` rồi tính:
- `predicted_eta = mean(eta_history)` làm giá trị dự đoán
- `confidence = 1 - (std / mean)` để đo độ ổn định của ETA

### `evidence_links`
Danh sách link phân tách bằng dấu phẩy (`,`), mỗi record có **≥2 links** dẫn đến:
- Bài viết Facebook Group cư dân Ocean Park 1
- Google Maps listing của quán

```
https://facebook.com/groups/op1/posts/101,https://g.co/maps/phothinop
```

**Hướng dẫn cho Member B:** Split bằng `evidence_links.split(',')` để lấy danh sách link.

## Lệnh thực thi

### Tạo SQLite từ CSV (chạy từ thư mục gốc dự án)

```bash
python scripts/import_csv_to_sqlite.py
```

### Kiểm tra nhanh sau import

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/sample_data.sqlite'); print(conn.execute('SELECT COUNT(*) FROM restaurants').fetchone())"
```

### Query mẫu

```sql
-- Top 5 quán giao nhanh nhất (dựa trên lịch sử ETA trung bình)
SELECT id, name, vendor, eta_history_json
FROM restaurants
WHERE is_active = 1
LIMIT 5;

-- Đếm tổng số quán
SELECT COUNT(*) FROM restaurants;

-- Lọc theo vendor
SELECT name, cuisine FROM restaurants WHERE vendor = 'GrabFood';
```

## Acceptance Criteria (Member A — DoD)

- [x] `data/sample_data.csv` có đúng 35 records
- [x] Mỗi record có `eta_history_json` là mảng JSON hợp lệ (≥5 điểm dữ liệu)
- [x] Mỗi record có `evidence_links` với **≥2 links** (FB + Google Maps)
- [x] `data/schema.sql` định nghĩa đủ 3 bảng: `restaurants`, `eta_logs`, `feedback_submissions`
- [x] Script `scripts/import_csv_to_sqlite.py` chạy không lỗi
- [x] `SELECT COUNT(*) FROM restaurants` trả về ≥ 30
