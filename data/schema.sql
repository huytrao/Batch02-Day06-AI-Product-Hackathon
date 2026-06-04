-- data/schema.sql

-- Bảng lưu trữ thông tin quán ăn và dữ liệu tích hợp
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    vendor TEXT NOT NULL,          -- GrabFood, ShopeeFood, Baemin, etc.
    eta_history_json TEXT NOT NULL, -- Mảng JSON chứa các mốc ETA lịch sử (ví dụ: [30, 35, 45, 40])
    cuisine TEXT NOT NULL,          -- Loại ẩm thực (Cơm, Bún, Phở, Ăn vặt...)
    tags TEXT,                     -- Các tag phụ (Giao nhanh, Đồ uống, Ăn chay...)
    evidence_links TEXT,           -- Danh sách link minh chứng nguồn (FB, Google Maps...)
    is_active INTEGER DEFAULT 1    -- Trạng thái hoạt động (1: Mở cửa, 0: Đóng cửa)
);

-- Bảng log lịch sử gọi ETA từ Agent phục vụ phân tích thời gian thực
CREATE TABLE IF NOT EXISTS eta_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_eta INTEGER,
    confidence_score REAL,
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
);

-- Bảng lưu trữ phản hồi từ người dùng (Hệ thống Feedback của Member E)
CREATE TABLE IF NOT EXISTS feedback_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    suggestion_id INTEGER,
    user_rating INTEGER CHECK(user_rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(suggestion_id) REFERENCES restaurants(id)
);