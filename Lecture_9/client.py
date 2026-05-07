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

def test_idempotency_v2():
    print("=== Đang kiểm tra tính năng Idempotency (v2) ===")
    url = f"{BASE_URL}/api/v2/payments"
    id_key = "req_unique_123456"
    headers = {"Idempotency-Key": id_key}
    payload = {
        "amount": 500.00,
        "currency": "USD",
        "user_id": "usr_idempotent",
        "payment_method": "E_WALLET"
    }

    # Lần gọi thứ nhất
    print(f"Lần gọi 1 (Key: {id_key})...")
    resp1 = requests.post(url, json=payload, headers=headers)
    print(f"Status: {resp1.status_code}, Cache: {resp1.headers.get('X-Idempotency-Cache')}")
    print(f"Transaction ID: {resp1.json()['data']['transaction_id']}")

    # Lần gọi thứ hai (Trùng key)
    print(f"\nLần gọi 2 (Cùng Key: {id_key})...")
    resp2 = requests.post(url, json=payload, headers=headers)
    print(f"Status: {resp2.status_code}, Cache: {resp2.headers.get('X-Idempotency-Cache')}")
    print(f"Transaction ID: {resp2.json()['data']['transaction_id']} (Phải trùng khớp với lần 1)")

    if resp1.json()['data']['transaction_id'] == resp2.json()['data']['transaction_id']:
        print("\n=> THÀNH CÔNG: Idempotency hoạt động chính xác!")
    else:
        print("\n=> THẤT BẠI: Idempotency không hoạt động.")
    print("-" * 50)

if __name__ == "__main__":
    try:
        # Chờ một chút để đảm bảo server đã sẵn sàng nếu chạy đồng thời
        time.sleep(1)
        test_v1_api()
        test_v2_api()
        test_idempotency_v2()
    except requests.exceptions.ConnectionError:
        print("Không thể kết nối đến server. Hãy đảm bảo bạn đã chạy 'python server.py' trước.")

