import requests
import time

BASE_URL = "http://localhost:5000"

def test_v1_api():
    print("=== Đang gọi API v1 (Deprecated) ===")
    url = f"{BASE_URL}/api/v1/payments"
    payload = {
        "amount": 100.50,
        "currency": "USD"
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
    
    # Kiểm tra header thông báo deprecation
    if 'Deprecation' in response.headers:
        print(f"\n[CẢNH BÁO TỪ SERVER] {response.headers.get('Warning')}")
        
    print("-" * 50)

def test_v2_api():
    print("=== Đang gọi API v2 (Mới nhất) ===")
    url = f"{BASE_URL}/api/v2/payments"
    
    # Cấu trúc payload v2 yêu cầu thêm user_id và payment_method
    payload = {
        "amount": 250.00,
        "currency": "USD",
        "user_id": "usr_987654321",
        "payment_method": "CREDIT_CARD"
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
    print("-" * 50)

if __name__ == "__main__":
    try:
        # Chờ một chút để đảm bảo server đã sẵn sàng nếu chạy đồng thời
        time.sleep(1)
        test_v1_api()
        test_v2_api()
    except requests.exceptions.ConnectionError:
        print("Không thể kết nối đến server. Hãy đảm bảo bạn đã chạy 'python server.py' trước.")
