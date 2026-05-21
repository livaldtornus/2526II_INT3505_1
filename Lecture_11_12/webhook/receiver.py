from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook/notifications', methods=['POST'])
def handle_webhook():
    """
    API này đóng vai trò là "Receiver" (Người nhận).
    Nó sẽ luôn mở và chờ hệ thống khác (Publisher) gọi đến (Push) khi có sự kiện xảy ra.
    """
    # 1. Xác thực Webhook (Trong thực tế cần kiểm tra chữ ký Signature/Secret Key)
    # 2. Nhận dữ liệu sự kiện
    event_data = request.json
    
    if not event_data:
        return jsonify({"error": "Invalid payload"}), 400
        
    event_type = event_data.get('event_type')
    
    # 3. Xử lý sự kiện (Event-driven)
    if event_type == "payment_success":
        order_id = event_data['data']['order_id']
        amount = event_data['data']['amount']
        logging.info(f"[WEBHOOK NHẬN] Thanh toán thành công cho đơn hàng {order_id}. Số tiền: {amount}. Tiến hành gửi Email cảm ơn khách hàng!")
        
    elif event_type == "payment_failed":
        order_id = event_data['data']['order_id']
        logging.warning(f"[WEBHOOK NHẬN] Thanh toán thất bại cho đơn hàng {order_id}. Gửi thông báo yêu cầu khách kiểm tra lại thẻ!")
        
    else:
        logging.info(f"[WEBHOOK NHẬN] Nhận được sự kiện không xác định: {event_type}")

    # Webhook Receiver luôn phải trả về 2xx nhanh nhất có thể để Publisher biết là đã nhận được
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    # Chạy receiver ở cổng 5004
    print("Webhook Receiver đang chạy tại cổng 5004 và chờ sự kiện...")
    app.run(port=5004, debug=True)
