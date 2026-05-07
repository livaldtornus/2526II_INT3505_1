from flask import Blueprint, request, jsonify, make_response
import uuid

v1_api = Blueprint('v1_api', __name__)

@v1_api.route('/payments', methods=['POST'])
def process_payment():
    data = request.json
    
    # Giả lập logic xử lý thanh toán
    amount = data.get('amount')
    currency = data.get('currency', 'USD')
    
    if not amount:
        return jsonify({"error": "Missing amount"}), 400
        
    response_data = {
        "status": "success",
        "message": f"Successfully processed payment of {amount} {currency}",
        "transaction_id": str(uuid.uuid4())
    }
    
    # Tạo response object
    response = make_response(jsonify(response_data), 200)
    
    # Thêm Header Deprecation và Warning
    response.headers['Deprecation'] = 'true'
    response.headers['Warning'] = '299 - "This API version is deprecated and will be removed on 2026-12-31. Please migrate to /api/v2/payments"'
    
    return response
