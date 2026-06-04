# Ocean Park 1 Eats — Data Infrastructure Documentation

## Cấu trúc thư mục dữ liệu
- `schema.sql`: File chứa định nghĩa bảng cho toàn bộ hệ thống.
- `sample_data.csv`: Tập dữ liệu thô gồm 35 nhà hàng tích hợp tag và lịch sử ETA.
- `sample_data.sqlite`: Cơ sở dữ liệu SQLite chính sau khi chạy script import.

## Định dạng Dữ liệu Quan trọng
1. **`eta_history_json`**: Được lưu dưới dạng text định dạng JSON Array chứa chuỗi số nguyên phút (ví dụ: `[30, 35, 32, 40, 28]`). Member B khi viết tool hãy parse trường này bằng `json.loads()` để lấy mảng và tính toán ETA kỳ vọng (Heuristic Mean/Median) cùng chỉ số Confidence.
2. **`evidence_links`**: Lưu danh sách link phân tách bằng dấu phẩy (`,`) dẫn trực tiếp đến bài viết Group cư dân FB hoặc Google Maps để tăng độ tin cậy của Agent (Tránh AI Hallucination).

## Lệnh thực thi nhanh
Để tạo mới hoặc re-import dữ liệu, di chuyển ra thư mục gốc dự án và chạy lệnh:
```bash
python scripts/import_csv_to_sqlite.py