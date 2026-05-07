from flask import Blueprint, request, jsonify, make_response
import uuid
import time

v2_api = Blueprint('v2_api', __name__)

# Giả lập bộ nhớ đệm để lưu trữ các yêu cầu đã xử lý
# Trong thực tế nên dùng Redis hoặc Database với TTL
idempotency_cache = {}

@v2_api.route('/payments', methods=['POST'])
def process_payment():
    # Kiểm tra Idempotency Key trong Header
    idempotency_key = request.headers.get('Idempotency-Key')
    
    if idempotency_key:
        # Nếu đã tồn tại key này trong cache, trả về kết quả cũ ngay lập tức
        if idempotency_key in idempotency_cache:
            response_data = idempotency_cache[idempotency_key]
            resp = make_response(jsonify(response_data), 200)
            resp.headers['X-Idempotency-Cache'] = 'HIT'
            return resp

    data = request.json
    
    # API v2 yêu cầu thêm trường payment_method và cấu trúc trả về chi tiết hơn
    amount = data.get('amount')
    currency = data.get('currency', 'USD')
    payment_method = data.get('payment_method')
    user_id = data.get('user_id')
    
    if not amount or not payment_method or not user_id:
        return jsonify({
            "error": "Validation Failed",
            "details": "Fields 'amount', 'payment_method', and 'user_id' are required in v2."
        }), 400
        
    # Giả lập xử lý tốn thời gian
    # time.sleep(1) 

    response_data = {
        "data": {
            "transaction_id": str(uuid.uuid4()),
            "status": "COMPLETED",
            "amount_processed": amount,
            "currency": currency,
            "payment_method": payment_method,
            "user_id": user_id,
            "timestamp": int(time.time())
        },
        "meta": {
            "api_version": "v2",
            "idempotency_key": idempotency_key
        }
    }
    
    # Lưu vào cache nếu có Idempotency-Key
    if idempotency_key:
        idempotency_cache[idempotency_key] = response_data

    resp = make_response(jsonify(response_data), 200)
    if idempotency_key:
        resp.headers['X-Idempotency-Cache'] = 'MISS'
    
    return resp

