#!/bin/bash

echo "=== Đang kiểm tra môi trường test ==="

# Kiểm tra xem server có đang chạy không (mặc định tại 8080)
if ! curl -s http://localhost:8080/v1/products > /dev/null; then
    echo "LỖI: Server chưa được khởi động tại http://localhost:8080/v1"
    echo "Vui lòng chạy server ở Lecture_7 trước khi thực hiện test."
    exit 1
fi

echo "=== Đang khởi chạy bộ test với Newman ==="

# Chạy newman thông qua npx để không cần cài đặt global
npx -y newman run product_api_tests.json \
    --reporters cli \
    --color on

echo ""
echo "=== Hoàn tất quá trình Test ==="
echo "Kiểm tra bảng tổng kết phía trên để xem kết quả Pass/Fail và Response Time."
