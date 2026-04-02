from flask import Flask
from flask_cors import CORS
from routes import api_bp
from utils import error_response

def create_app():
    # 1. Setup Flask App
    app = Flask(__name__)
    CORS(app)
    
    # 2. Register Blueprints (Separation of Concerns)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    
    # 3. Global Error Handlers (Mọi lỗi đều format chuẩn)
    @app.errorhandler(404)
    def not_found(e):
        return error_response(f"Not Found: {str(e.description)}", 404)

    @app.errorhandler(400)
    def bad_request(e):
        return error_response(f"Bad Request: {str(e.description)}", 400)

    @app.errorhandler(500)
    def server_error(e):
        return error_response(f"Internal Server Error: {str(e.description)}", 500)
        
    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 App is running with Refactored Clean Architecture!")
    app.run(debug=True, host="0.0.0.0", port=5001)
