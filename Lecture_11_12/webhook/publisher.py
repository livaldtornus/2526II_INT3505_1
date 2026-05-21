import requests
import time
import json

# URL của Webhook Receiver (Hệ thống thông báo của chúng ta)
WEBHOOK_URL = "http://localhost:5004/webhook/notifications"

def simulate_payment_system():
    """
    Hàm này giả lập một hệ thống thanh toán (như Stripe/Momo).
    Khi có sự kiện xảy ra, nó sẽ PUSH (đẩy) dữ liệu tới WEBHOOK_URL.
    """
    print("=== Hệ thống thanh toán đang xử lý... ===")
    
    # 1. Giả lập một giao dịch thành công
    time.sleep(2)
    success_event = {
        "event_id": "evt_001",
        "event_type": "payment_success",
        "data": {
            "order_id": "ORD-999",
            "amount": 1500000,
            "currency": "VND"
        }
    }
    print("[PUBLISHER] Bắn sự kiện: payment_success tới Webhook")
    try:
        response = requests.post(WEBHOOK_URL, json=success_event)
        print(f"[PUBLISHER] Receiver phản hồi: {response.status_code}\n")
    except Exception as e:
        print(f"[PUBLISHER] Lỗi khi bắn Webhook: {e}")

    # 2. Giả lập một giao dịch thất bại
    time.sleep(3)
    failed_event = {
        "event_id": "evt_002",
        "event_type": "payment_failed",
        "data": {
            "order_id": "ORD-777",
            "reason": "Insufficient funds"
        }
    }
    print("[PUBLISHER] Bắn sự kiện: payment_failed tới Webhook")
    try:
        response = requests.post(WEBHOOK_URL, json=failed_event)
        print(f"[PUBLISHER] Receiver phản hồi: {response.status_code}\n")
    except Exception as e:
        print(f"[PUBLISHER] Lỗi khi bắn Webhook: {e}")

if __name__ == "__main__":
    simulate_payment_system()
