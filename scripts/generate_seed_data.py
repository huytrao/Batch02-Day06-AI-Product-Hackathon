"""
Seed data generator for Ocean Park 1 Eats prototype.
Creates sample_data.csv and sample_data.sqlite with 35+ restaurant records.
"""

import csv
import json
import os
import sqlite3
import random
import sys

DATADIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_PATH = os.path.join(DATADIR, "sample_data.csv")
DB_PATH = os.path.join(DATADIR, "sample_data.sqlite")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

random.seed(42)

RESTAURANTS = [
    {
        "id": 1,
        "name": "Phở Thìn",
        "vendor": "GrabFood",
        "cuisine": "Phở - Món Việt",
        "tags": "giaonhanh,nổi tiếng,sáng-sớm",
        "eta_history": [28, 32, 30, 35, 29, 31, 33],
        "open_time": "06:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://www.facebook.com/phothinocp1/",
            "https://grab.vn/food/vi/restaurant/pho-thin-ocp1/",
            "https://maps.google.com/?cid=phothinocp1"
        ],
        "base_eta": 30,
        "rating": 4.5,
        "review_count": 128
    },
    {
        "id": 2,
        "name": "Bún Chả Hương Liên",
        "vendor": "ShopeeFood",
        "cuisine": "Bún - Món Việt",
        "tags": "giaonhanh,best-seller",
        "eta_history": [35, 38, 33, 40, 36, 34, 37],
        "open_time": "07:00",
        "close_time": "21:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/bun-cha-huong-lien-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12345/"
        ],
        "base_eta": 35,
        "rating": 4.7,
        "review_count": 205
    },
    {
        "id": 3,
        "name": "Pizza Hut Ocean Park",
        "vendor": "GrabFood",
        "cuisine": "Pizza - Ý",
        "tags": "giaonhanh,giao-chậm,có-thể-order",
        "eta_history": [42, 48, 45, 50, 44, 46, 43, 55],
        "open_time": "09:00",
        "close_time": "22:30",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/pizza-hut-ocp1/",
            "https://www.pizzahut.vn/"
        ],
        "base_eta": 45,
        "rating": 4.2,
        "review_count": 89
    },
    {
        "id": 4,
        "name": "Cơm Gà Xối Mỡ",
        "vendor": "ShopeeFood",
        "cuisine": "Cơm - Gà",
        "tags": "giaonhanh,giá-rẻ,best-seller",
        "eta_history": [25, 22, 28, 26, 24, 27, 23],
        "open_time": "10:00",
        "close_time": "21:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/com-ga-xoi-mo-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12346/"
        ],
        "base_eta": 25,
        "rating": 4.6,
        "review_count": 167
    },
    {
        "id": 5,
        "name": "Bánh Mì Phố",
        "vendor": "GrabFood",
        "cuisine": "Bánh mì - Đồ ăn nhanh",
        "tags": "giaonhanh,sáng-sớm,giá-rẻ",
        "eta_history": [18, 20, 16, 22, 19, 17, 21],
        "open_time": "05:30",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/banh-mi-pho-ocp1/",
            "https://maps.google.com/?cid=banhmiphoocp1"
        ],
        "base_eta": 18,
        "rating": 4.4,
        "review_count": 73
    },
    {
        "id": 6,
        "name": "Lẩu Cua Đồng",
        "vendor": "ShopeeFood",
        "cuisine": "Lẩu - Món Việt",
        "tags": "giao-chậm,nhóm-đông",
        "eta_history": [45, 50, 48, 55, 52, 47, 51],
        "open_time": "10:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/lau-cua-dong-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12347/"
        ],
        "base_eta": 48,
        "rating": 4.3,
        "review_count": 94
    },
    {
        "id": 7,
        "name": "Gà Rán Jollibee",
        "vendor": "GrabFood",
        "cuisine": "Gà rán - Đồ ăn nhanh",
        "tags": "giaonhanh,best-seller,có-thể-order",
        "eta_history": [30, 28, 32, 35, 29, 31, 27],
        "open_time": "07:30",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/jollibee-ocp1/",
            "https://www.jollibee.com.vn/"
        ],
        "base_eta": 30,
        "rating": 4.5,
        "review_count": 312
    },
    {
        "id": 8,
        "name": "Bún Bò Huế",
        "vendor": "ShopeeFood",
        "cuisine": "Bún - Món Huế",
        "tags": "giaonhanh,giá-rẻ",
        "eta_history": [32, 35, 30, 38, 33, 36, 31],
        "open_time": "06:30",
        "close_time": "21:30",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/bun-bo-hue-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12348/"
        ],
        "base_eta": 33,
        "rating": 4.3,
        "review_count": 88
    },
    {
        "id": 9,
        "name": "Sushi Tokyo",
        "vendor": "GrabFood",
        "cuisine": "Sushi - Nhật",
        "tags": "giao-chậm,cao-cấp",
        "eta_history": [38, 42, 40, 45, 39, 41, 44],
        "open_time": "10:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/sushi-tokyo-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12349/"
        ],
        "base_eta": 40,
        "rating": 4.8,
        "review_count": 56
    },
    {
        "id": 10,
        "name": "Mì Cay Hàn Quốc",
        "vendor": "ShopeeFood",
        "cuisine": "Mì - Hàn Quốc",
        "tags": "giaonhanh,cao-cấp,có-thể-order",
        "eta_history": [27, 25, 30, 28, 26, 29, 32],
        "open_time": "09:00",
        "close_time": "22:30",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/mi-cay-han-quoc-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12350/"
        ],
        "base_eta": 28,
        "rating": 4.6,
        "review_count": 134
    },
    {
        "id": 11,
        "name": "Bánh Cuốn Nóng",
        "vendor": "GrabFood",
        "cuisine": "Bánh - Món Việt",
        "tags": "giaonhanh,sáng-sớm",
        "eta_history": [22, 20, 25, 23, 21, 24, 19],
        "open_time": "05:00",
        "close_time": "13:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/banh-cuon-nong-ocp1/",
            "https://maps.google.com/?cid=banhcuonnongocp1"
        ],
        "base_eta": 22,
        "rating": 4.4,
        "review_count": 65
    },
    {
        "id": 12,
        "name": "Phở Cuốn Hà Nội",
        "vendor": "ShopeeFood",
        "cuisine": "Phở cuốn - Món Việt",
        "tags": "giaonhanh,best-seller",
        "eta_history": [30, 33, 28, 35, 31, 29, 34],
        "open_time": "08:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/pho-cuon-ha-noi-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12351/"
        ],
        "base_eta": 31,
        "rating": 4.5,
        "review_count": 142
    },
    {
        "id": 13,
        "name": "Cơm Tấm Sài Gòn",
        "vendor": "GrabFood",
        "cuisine": "Cơm - Món Nam",
        "tags": "giaonhanh,giá-rẻ,best-seller",
        "eta_history": [26, 24, 29, 27, 25, 28, 30],
        "open_time": "07:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/com-tam-sai-gon-ocp1/",
            "https://maps.google.com/?cid=comtamsaigonocp1"
        ],
        "base_eta": 27,
        "rating": 4.6,
        "review_count": 188
    },
    {
        "id": 14,
        "name": "Mỳ Quảng Đà Nẵng",
        "vendor": "ShopeeFood",
        "cuisine": "Mỳ - Món Trung Bộ",
        "tags": "giaonhanh,có-thể-order",
        "eta_history": [34, 37, 32, 39, 35, 33, 36],
        "open_time": "06:30",
        "close_time": "21:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/my-quang-da-nang-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12352/"
        ],
        "base_eta": 35,
        "rating": 4.2,
        "review_count": 77
    },
    {
        "id": 15,
        "name": "Bò Né 3 Ngon",
        "vendor": "GrabFood",
        "cuisine": "Bò - Món Việt",
        "tags": "giaonhanh,cao-cấp",
        "eta_history": [29, 32, 27, 34, 30, 28, 33],
        "open_time": "06:30",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/bo-ne-3-ngon-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12353/"
        ],
        "base_eta": 30,
        "rating": 4.7,
        "review_count": 156
    },
    {
        "id": 16,
        "name": "Chè Thái Sương Sương",
        "vendor": "ShopeeFood",
        "cuisine": "Chè - Tráng miệng",
        "tags": "giaonhanh,giá-rẻ",
        "eta_history": [15, 18, 14, 20, 16, 17, 19],
        "open_time": "10:00",
        "close_time": "22:30",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/che-thai-suong-suong-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12354/"
        ],
        "base_eta": 16,
        "rating": 4.3,
        "review_count": 92
    },
    {
        "id": 17,
        "name": "KFC Ocean Park",
        "vendor": "GrabFood",
        "cuisine": "Gà rán - Đồ ăn nhanh",
        "tags": "giaonhanh,best-seller,có-thể-order",
        "eta_history": [35, 32, 38, 40, 33, 36, 34],
        "open_time": "07:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/kfc-ocp1/",
            "https://www.kfcvietnam.com.vn/"
        ],
        "base_eta": 35,
        "rating": 4.4,
        "review_count": 420
    },
    {
        "id": 18,
        "name": "Xôi Bà Thảo",
        "vendor": "ShopeeFood",
        "cuisine": "Xôi - Món Việt",
        "tags": "giaonhanh,sáng-sớm,giá-rẻ",
        "eta_history": [12, 15, 13, 18, 14, 11, 16],
        "open_time": "05:00",
        "close_time": "11:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/xoi-ba-thao-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12355/"
        ],
        "base_eta": 14,
        "rating": 4.8,
        "review_count": 201
    },
    {
        "id": 19,
        "name": "Lẩu Riêu Cua Đồng",
        "vendor": "GrabFood",
        "cuisine": "Lẩu - Món Việt",
        "tags": "giao-chậm,nhóm-đông,có-thể-order",
        "eta_history": [48, 52, 50, 55, 49, 53, 46],
        "open_time": "10:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/lau-rieu-cua-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12356/"
        ],
        "base_eta": 50,
        "rating": 4.4,
        "review_count": 103
    },
    {
        "id": 20,
        "name": "Trà Chanh 1989",
        "vendor": "ShopeeFood",
        "cuisine": "Đồ uống",
        "tags": "giaonhanh,giá-rẻ",
        "eta_history": [10, 12, 9, 14, 11, 13, 8],
        "open_time": "08:00",
        "close_time": "23:30",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/tra-chanh-1989-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12357/"
        ],
        "base_eta": 11,
        "rating": 4.1,
        "review_count": 67
    },
    {
        "id": 21,
        "name": "Mì Vằn Thắn",
        "vendor": "GrabFood",
        "cuisine": "Mì - Món Hoa",
        "tags": "giaonhanh,có-thể-order",
        "eta_history": [24, 27, 22, 29, 25, 23, 26],
        "open_time": "07:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/mi-van-than-ocp1/",
            "https://maps.google.com/?cid=mivanthanocp1"
        ],
        "base_eta": 25,
        "rating": 4.3,
        "review_count": 81
    },
    {
        "id": 22,
        "name": "Ốc Ngon Việt",
        "vendor": "ShopeeFood",
        "cuisine": "Ốc - Món Việt",
        "tags": "giao-chậm,nhóm-đông",
        "eta_history": [40, 44, 38, 47, 41, 42, 45],
        "open_time": "11:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/oc-ngon-viet-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12358/"
        ],
        "base_eta": 42,
        "rating": 4.2,
        "review_count": 59
    },
    {
        "id": 23,
        "name": "Bánh Xèo Cô Ba",
        "vendor": "GrabFood",
        "cuisine": "Bánh - Món Nam",
        "tags": "giaonhanh,best-seller",
        "eta_history": [28, 31, 26, 33, 29, 30, 27],
        "open_time": "09:00",
        "close_time": "21:30",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/banh-xeo-co-ba-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12359/"
        ],
        "base_eta": 29,
        "rating": 4.5,
        "review_count": 119
    },
    {
        "id": 24,
        "name": "Cháo Ếch Đồng",
        "vendor": "ShopeeFood",
        "cuisine": "Cháo - Món Việt",
        "tags": "giao-chậm,nhóm-đông",
        "eta_history": [36, 40, 34, 42, 37, 39, 35],
        "open_time": "08:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/chao-ech-dong-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12360/"
        ],
        "base_eta": 38,
        "rating": 4.1,
        "review_count": 46
    },
    {
        "id": 25,
        "name": "Bún Riêu Cua",
        "vendor": "GrabFood",
        "cuisine": "Bún - Món Việt",
        "tags": "giaonhanh,sáng-sớm",
        "eta_history": [22, 25, 20, 27, 23, 21, 24],
        "open_time": "06:00",
        "close_time": "14:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/bun-rieu-cua-ocp1/",
            "https://maps.google.com/?cid=bunrieucuaocp1"
        ],
        "base_eta": 23,
        "rating": 4.5,
        "review_count": 96
    },
    {
        "id": 26,
        "name": "Cơm Niêu Singapore",
        "vendor": "ShopeeFood",
        "cuisine": "Cơm - Món Á",
        "tags": "giao-chậm,cao-cấp",
        "eta_history": [38, 42, 36, 44, 40, 39, 41],
        "open_time": "10:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/com-nieu-singapore-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12361/"
        ],
        "base_eta": 40,
        "rating": 4.4,
        "review_count": 73
    },
    {
        "id": 27,
        "name": "Bánh Giò Bà Điệp",
        "vendor": "GrabFood",
        "cuisine": "Bánh - Món Việt",
        "tags": "giaonhanh,sáng-sớm,giá-rẻ",
        "eta_history": [15, 18, 13, 20, 16, 14, 17],
        "open_time": "05:30",
        "close_time": "12:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/banh-gio-ba-diep-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12362/"
        ],
        "base_eta": 16,
        "rating": 4.6,
        "review_count": 84
    },
    {
        "id": 28,
        "name": "Phá Lấu Cô Năm",
        "vendor": "ShopeeFood",
        "cuisine": "Phá lấu - Món Nam",
        "tags": "giao-chậm,có-thể-order",
        "eta_history": [33, 37, 30, 39, 34, 36, 32],
        "open_time": "09:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/pha-lau-co-nam-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12363/"
        ],
        "base_eta": 35,
        "rating": 4.3,
        "review_count": 63
    },
    {
        "id": 29,
        "name": "Bánh Tráng Trộn",
        "vendor": "GrabFood",
        "cuisine": "Bánh - Đồ ăn vặt",
        "tags": "giaonhanh,giá-rẻ",
        "eta_history": [14, 17, 12, 19, 15, 13, 16],
        "open_time": "09:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/banh-trang-tron-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12364/"
        ],
        "base_eta": 15,
        "rating": 4.0,
        "review_count": 44
    },
    {
        "id": 30,
        "name": "Hủ Tiếu Nam Vang",
        "vendor": "ShopeeFood",
        "cuisine": "Hủ tiếu - Món Nam",
        "tags": "giaonhanh,best-seller",
        "eta_history": [26, 29, 24, 31, 27, 25, 28],
        "open_time": "06:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/hu-tieu-nam-vang-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12365/"
        ],
        "base_eta": 27,
        "rating": 4.5,
        "review_count": 113
    },
    {
        "id": 31,
        "name": "Cơm Gà Hải Nam",
        "vendor": "GrabFood",
        "cuisine": "Cơm - Món Hoa",
        "tags": "giaonhanh,có-thể-order",
        "eta_history": [32, 35, 30, 37, 33, 31, 34],
        "open_time": "08:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/com-ga-hai-nam-ocp1/",
            "https://maps.google.com/?cid=comgahainamocp1"
        ],
        "base_eta": 33,
        "rating": 4.4,
        "review_count": 91
    },
    {
        "id": 32,
        "name": "Chả Cá Lã Vọng",
        "vendor": "ShopeeFood",
        "cuisine": "Cá - Món Việt",
        "tags": "giao-chậm,cao-cấp",
        "eta_history": [40, 44, 38, 46, 41, 43, 39],
        "open_time": "10:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/cha-ca-la-vong-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12366/"
        ],
        "base_eta": 42,
        "rating": 4.7,
        "review_count": 108
    },
    {
        "id": 33,
        "name": "Bánh Bao Bà Xứ",
        "vendor": "GrabFood",
        "cuisine": "Bánh - Món Hoa",
        "tags": "giaonhanh,sáng-sớm,giá-rẻ",
        "eta_history": [12, 15, 10, 17, 13, 11, 14],
        "open_time": "05:00",
        "close_time": "21:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/banh-bao-ba-xu-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12367/"
        ],
        "base_eta": 13,
        "rating": 4.5,
        "review_count": 72
    },
    {
        "id": 34,
        "name": "Mực Nướng Hong Kong",
        "vendor": "ShopeeFood",
        "cuisine": "Mực - Món Á",
        "tags": "giao-chậm,cao-cấp",
        "eta_history": [44, 48, 42, 50, 45, 47, 43],
        "open_time": "11:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/muc-nuong-hong-kong-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12368/"
        ],
        "base_eta": 45,
        "rating": 4.2,
        "review_count": 38
    },
    {
        "id": 35,
        "name": "Chân Gà Sả Tắc",
        "vendor": "GrabFood",
        "cuisine": "Đồ ăn vặt",
        "tags": "giaonhanh,giá-rẻ",
        "eta_history": [20, 23, 18, 25, 21, 19, 22],
        "open_time": "10:00",
        "close_time": "23:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/chan-ga-sa-tac-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12369/"
        ],
        "base_eta": 21,
        "rating": 4.1,
        "review_count": 55
    },
    {
        "id": 36,
        "name": "Ớt Hiểm BBQ",
        "vendor": "ShopeeFood",
        "cuisine": "BBQ - Món Việt",
        "tags": "giao-chậm,nhóm-đông,có-thể-order",
        "eta_history": [50, 55, 48, 58, 52, 53, 49],
        "open_time": "10:00",
        "close_time": "23:30",
        "evidence_links": [
            "https://shopeefood.vn/ha-noi/ot-hiem-bbq-ocp1",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12370/"
        ],
        "base_eta": 52,
        "rating": 4.3,
        "review_count": 87
    },
    {
        "id": 37,
        "name": "Bún Đậu Mắm Tôm",
        "vendor": "GrabFood",
        "cuisine": "Bún - Món Việt",
        "tags": "giaonhanh,best-seller,nhóm-đông",
        "eta_history": [24, 27, 22, 29, 25, 23, 26],
        "open_time": "08:00",
        "close_time": "22:00",
        "evidence_links": [
            "https://grab.vn/food/vi/restaurant/bun-dau-mam-tom-ocp1/",
            "https://www.facebook.com/groups/vinhomesocp1/permalink/12371/"
        ],
        "base_eta": 25,
        "rating": 4.6,
        "review_count": 145
    },
]


def generate_csv():
    """Write sample_data.csv with 37 restaurant records."""
    fieldnames = [
        "id", "name", "vendor", "cuisine", "tags",
        "eta_history", "open_time", "close_time",
        "evidence_links", "base_eta", "rating", "review_count"
    ]
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in RESTAURANTS:
            row = {
                "id": r["id"],
                "name": r["name"],
                "vendor": r["vendor"],
                "cuisine": r["cuisine"],
                "tags": r["tags"],
                "eta_history": json.dumps(r["eta_history"], ensure_ascii=False),
                "open_time": r["open_time"],
                "close_time": r["close_time"],
                "evidence_links": "|".join(r["evidence_links"]),
                "base_eta": r["base_eta"],
                "rating": r["rating"],
                "review_count": r["review_count"],
            }
            writer.writerow(row)
    print(f"✓ CSV written: {CSV_PATH} ({len(RESTAURANTS)} records)")


def build_sqlite():
    """Create SQLite DB with restaurants, eta_logs, feedback_submissions tables."""
    SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        vendor TEXT NOT NULL DEFAULT 'GrabFood',
        cuisine TEXT,
        tags TEXT,
        open_time TEXT,
        close_time TEXT,
        base_eta INTEGER DEFAULT 30,
        rating REAL DEFAULT 0.0,
        review_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS eta_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        eta INTEGER NOT NULL,
        recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
    );

    CREATE TABLE IF NOT EXISTS feedback_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_text TEXT,
        suggestion_id INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        feedback_text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS evidence_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER NOT NULL,
        url TEXT NOT NULL,
        label TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
    );
    """

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Remove old DB so we always start fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)

    # Insert restaurants
    for r in RESTAURANTS:
        conn.execute(
            """INSERT INTO restaurants (id, name, vendor, cuisine, tags, open_time, close_time, base_eta, rating, review_count)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (r["id"], r["name"], r["vendor"], r["cuisine"], r["tags"],
             r["open_time"], r["close_time"], r["base_eta"], r["rating"], r["review_count"])
        )

        # Insert eta_logs
        for eta_val in r["eta_history"]:
            conn.execute(
                "INSERT INTO eta_logs (restaurant_id, eta) VALUES (?, ?)",
                (r["id"], eta_val)
            )

        # Insert evidence_links
        for i, url in enumerate(r["evidence_links"]):
            conn.execute(
                "INSERT INTO evidence_links (restaurant_id, url, label) VALUES (?, ?, ?)",
                (r["id"], url, f"source_{i+1}")
            )

    conn.commit()
    conn.close()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
    eta_count = conn.execute("SELECT COUNT(*) FROM eta_logs").fetchone()[0]
    ev_count = conn.execute("SELECT COUNT(*) FROM evidence_links").fetchone()[0]
    conn.close()
    print(f"✓ SQLite DB: {DB_PATH}")
    print(f"  - {count} restaurants")
    print(f"  - {eta_count} eta_logs")
    print(f"  - {ev_count} evidence_links")


def main():
    generate_csv()
    build_sqlite()
    print("✓ Seed data generation complete!")


if __name__ == "__main__":
    main()
