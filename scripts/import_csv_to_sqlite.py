# scripts/import_csv_to_sqlite.py
import os
import csv
import sqlite3
import json
import sys

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def init_and_import_db():
    csv_path = 'data/sample_data.csv'
    sql_schema_path = 'data/schema.sql'
    db_path = 'data/sample_data.sqlite'

    # Đảm bảo thư mục dữ liệu tồn tại
    os.makedirs('data', exist_ok=True)

    print("=== Khởi tạo Data Infrastructure cho Ocean Park 1 Eats ===")
    
    # 1. Kết nối DB và chạy Schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    print("[OK] Đã cấu hình Schema thành công.")

    # 2. Đọc và Import CSV
    if not os.path.exists(csv_path):
        print(f"[Error] Không tìm thấy file dữ liệu nguồn tại {csv_path}")
        return

    # Xóa dữ liệu cũ trong bảng restaurants để tránh trùng lặp khi re-run
    cursor.execute("DELETE FROM restaurants")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            # Kiểm tra tính hợp lệ của JSON của mảng eta_history
            try:
                eta_data = json.loads(row['eta_history_json'])
                eta_json_str = json.dumps(eta_data)
            except json.JSONDecodeError:
                # Fallback nếu dữ liệu lỗi
                eta_json_str = json.dumps([30, 40])

            cursor.execute("""
                INSERT INTO restaurants (id, name, vendor, eta_history_json, cuisine, tags, evidence_links, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(row['id']),
                row['name'],
                row['vendor'],
                eta_json_str,
                row['cuisine'],
                row['tags'],
                row['evidence_links'],
                int(row['is_active'])
            ))
            count += 1
            
    conn.commit()
    print(f"[OK] Đã import thành công {count} bản ghi vào bảng 'restaurants'.")

    # 3. Chạy test query kiểm tra tiêu chuẩn nghiệm thu (Acceptance Criteria)
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    total_rows = cursor.fetchone()[0]
    print(f"[Kiểm tra] Tổng số hàng hiện tại trong DB: {total_rows}")
    
    if total_rows >= 30:
        print("[Đạt] Đã vượt mức nghiệm thu tối thiểu (>= 30 quán ăn).")
    else:
        print("[Cảnh báo] Số lượng hàng chưa đạt yêu cầu nghiệm thu.")
        
    conn.close()

if __name__ == '__main__':
    init_and_import_db()