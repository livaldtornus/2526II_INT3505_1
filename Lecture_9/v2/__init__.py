from flask import Blueprint, request, jsonify
import uuid
import time

v2_api = Blueprint('v2_api', __name__)

@v2_api.route('/payments', methods=['POST'])
def process_payment():
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
            "api_version": "v2"
        }
    }
    
    return jsonify(response_data), 200
