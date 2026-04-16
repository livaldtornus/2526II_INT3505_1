# Product Management API

Hệ thống quản lý thông tin sản phẩm dựa trên chuẩn OpenAPI.

## Đặc điểm nổi bật
- **Framework**: Python Flask (kết hợp thư viện Connexion)
- **Chuẩn hóa**: Định nghĩa API bằng OpenAPI Spec 3.0
- **Persistence**: Sử dụng MongoDB (thông qua `pymongo`) để lưu trữ dữ liệu bền vững.

## Cấu trúc dự án
- `openapi.yaml`: Đặc tả chi tiết các endpoint và schema của hệ thống.
- `server/`: Mã nguồn triển khai backend.
  - `openapi_server/controllers/`: Xử lý logic nghiệp vụ cho từng endpoint.
  - `openapi_server/database.py`: Lớp trừu tượng quản lý việc truy xuất dữ liệu.
  - `openapi_server/models/`: Định nghĩa các cấu trúc dữ liệu theo spec.

## Cài đặt và Chạy thử

1. **Chuẩn bị môi trường**:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

2. **Khởi động dịch vụ**:
   ```bash
   python3 -m openapi_server
   ```
   Dịch vụ sẽ lắng nghe tại cổng `8080`.
   Tài liệu API (Swagger UI) có sẵn tại: `http://localhost:8080/v1/ui`.

## Kiểm tra các Endpoint

### Tạo sản phẩm mới
```bash
curl -X POST "http://localhost:8080/v1/products" \
     -H "Content-Type: application/json" \
     -d '{"name": "iPhone 15 Pro", "price": 999, "description": "Latest model", "quantity": 100}'
```

### Danh sách sản phẩm
```bash
curl -X GET "http://localhost:8080/v1/products"
```

### Cập nhật thông tin
```bash
curl -X PUT "http://localhost:8080/v1/products/{id}" \
     -H "Content-Type: application/json" \
     -d '{"name": "iPhone 15 Pro Max", "price": 1199}'
```

### Xóa sản phẩm
```bash
curl -X DELETE "http://localhost:8080/v1/products/{id}"
```

## Cấu hình Database
Dịch vụ sử dụng các biến môi trường sau để cấu hình kết nối MongoDB (mặc định sẽ kết nối tới localhost):
- `MONGO_URI`: URI kết nối MongoDB (Mặc định: `mongodb://localhost:27017/`)
- `DB_NAME`: Tên database (Mặc định: `product_db`)

Bạn có thể thay đổi bằng cách export biến môi trường trước khi chạy server:
```bash
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
python3 -m openapi_server
```
