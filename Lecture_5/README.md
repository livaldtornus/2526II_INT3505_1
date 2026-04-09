# Pagination Performance Test (1M Records)

Môi trường kiểm thử hiệu năng giữa **Offset-based Pagination** và **Cursor-based Pagination** trên cơ sở dữ liệu SQLite với quy mô 1,000,000 bản ghi.

### 📋 Hướng dẫn thực thi

Chạy script benchmark để khởi tạo dữ liệu và đo thời gian thực thi:
```bash
python3 benchmark_pagination.py
```

### 🔍 Các chỉ số kiểm thử
- **Offset Query**: `SELECT * FROM records LIMIT 10 OFFSET 900000`
- **Cursor Query**: `SELECT * FROM records WHERE id > 900000 LIMIT 10`

### 🔧 Công cụ hỗ trợ
- Cơ sở dữ liệu mặc định: `benchmark_1m.db` (được tạo tự động khi chạy script).
- Truy vấn thủ công thông qua SQLite CLI:
  ```bash
  sqlite3 benchmark_1m.db "SELECT * FROM records LIMIT 10 OFFSET 900000;"
  ```

---
*Lưu ý: Thời gian thực thi có thể thay đổi tùy thuộc vào cấu hình phần cứng của hệ thống.*
