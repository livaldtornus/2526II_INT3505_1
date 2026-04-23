# Buổi 8: API Testing và Quality Assurance

Dự án này chứa bộ test tự động cho Product Management API đã phát triển ở Buổi 7.

## Công cụ sử dụng
- **Postman**: Dùng để thiết kế và tổ chức các test cases.
- **Newman**: Command-line runner cho Postman Collections, dùng để chạy test tự động.

## Cấu trúc thư mục
- `product_api_tests.json`: Postman Collection chứa 6 test cases bao quát toàn bộ quy trình CRUD.
- `run_tests.sh`: Script tự động cài đặt công cụ và chạy test.

## Các Test Case bao gồm:
1. **List Products (Initial)**: Kiểm tra danh sách ban đầu (phải trả về 200 OK và là một array).
2. **Create Product**: Tạo mới sản phẩm, kiểm tra status 201 và lưu ID vào biến môi trường.
3. **Get Product by ID**: Truy vấn sản phẩm vừa tạo bằng ID, kiểm tra tính đúng đắn của dữ liệu.
4. **Update Product**: Cập nhật giá và tên sản phẩm, kiểm tra thay đổi.
5. **Delete Product**: Xóa sản phẩm, kiểm tra status 204.
6. **Verify Product Deleted**: Thử truy vấn lại sản phẩm đã xóa, phải trả về 404 Not Found.

## Cách chạy Test

### Cách 1: Sử dụng script tự động
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Cách 2: Chạy thủ công bằng npx (không cần cài đặt global)
```bash
# Đảm bảo server ở Buổi 7 đang chạy trước khi thực hiện
npx newman run product_api_tests.json
```

## Đo lường Hiệu năng
Khi chạy bằng Newman, bạn sẽ nhận được bảng tổng kết ở cuối terminal bao gồm:
- **Response Time**: Thời gian phản hồi trung bình (Average), tối thiểu (Min), và tối đa (Max).
- **Failure Rate**: Số lượng test cases bị fail (nếu có).
