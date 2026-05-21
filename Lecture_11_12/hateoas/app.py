from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập database đơn hàng
orders = {
    "ORD123": {"id": "ORD123", "status": "PENDING", "amount": 100},
    "ORD124": {"id": "ORD124", "status": "PAID", "amount": 200},
    "ORD125": {"id": "ORD125", "status": "SHIPPED", "amount": 300}
}

def generate_links(order):
    """Hàm sinh ra các liên kết (HATEOAS) dựa trên State của Order"""
    order_id = order['id']
    status = order['status']
    base_url = "http://localhost:5003"
    
    links = [
        {"rel": "self", "href": f"{base_url}/orders/{order_id}", "method": "GET"}
    ]
    
    if status == "PENDING":
        links.append({"rel": "pay", "href": f"{base_url}/orders/{order_id}/pay", "method": "POST"})
        links.append({"rel": "cancel", "href": f"{base_url}/orders/{order_id}/cancel", "method": "POST"})
    elif status == "PAID":
        links.append({"rel": "ship", "href": f"{base_url}/orders/{order_id}/ship", "method": "POST"})
        links.append({"rel": "refund", "href": f"{base_url}/orders/{order_id}/refund", "method": "POST"})
        
    return links

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
        
    response = {
        "order": order,
        "_links": generate_links(order)  # Chèn links tương ứng với trạng thái
    }
    return jsonify(response)

@app.route('/orders/<order_id>/<action>', methods=['POST'])
def process_order_action(order_id, action):
    # API giả lập xử lý các action
    return jsonify({"message": f"Action '{action}' processed for order {order_id}"})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
