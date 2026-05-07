from flask import Flask, jsonify
from v1 import v1_api
from v2 import v2_api

app = Flask(__name__)

# Đăng ký các phiên bản API dưới dạng Blueprint (URL Versioning)
app.register_blueprint(v1_api, url_prefix='/api/v1')
app.register_blueprint(v2_api, url_prefix='/api/v2')

@app.route('/')
def index():
    return jsonify({
        "message": "Payment API Server is running",
        "versions": {
            "v1": "/api/v1/payments (Deprecated)",
            "v2": "/api/v2/payments (Active)"
        }
    })

if __name__ == '__main__':
    # Chạy server ở cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
