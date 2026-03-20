import os
import datetime
from flask import Flask, send_file, redirect, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# --- Dữ liệu giả lập ---
books = [
    {
        "id": 1,
        "title": "Nhà Giả Kim",
        "author": "Paulo Coelho",
        "genre": "fiction",
        "price": 85000,
        "published_year": 1988,
        "available": True,
        "created_at": "2024-01-15T08:30:00Z"
    },
    {
        "id": 2,
        "title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "genre": "non-fiction",
        "price": 95000,
        "published_year": 1936,
        "available": True,
        "created_at": "2024-01-16T10:00:00Z"
    }
]

# --- Documentation Routes ---
SWAGGER_URL = "/docs"
API_URL     = "/openapi.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "Book Management API"})
app.register_blueprint(swaggerui_blueprint)

@app.route("/")
def index():
    return redirect("/docs")

@app.route("/openapi.yaml")
def serve_yaml():
    return send_file("books_api.yaml", mimetype="text/yaml")

# --- API Endpoints (Cài đặt logic thực tế) ---

@app.route("/books", methods=["GET"])
def list_books():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    search = request.args.get("search", "").lower()
    
    # Filter đơn giản theo search
    filtered_books = [b for b in books if search in b["title"].lower() or search in b["author"].lower()]
    
    # Phân trang
    start = (page - 1) * limit
    end = start + limit
    data = filtered_books[start:end]
    
    return jsonify({
        "total": len(filtered_books),
        "page": page,
        "limit": limit,
        "data": data
    }), 200

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "NOT_FOUND", "message": "Không tìm thấy sách"}), 404
    return jsonify({"data": book}), 200

@app.route("/books", methods=["POST"])
def create_book():
    data = request.json
    new_id = max([b["id"] for b in books] + [0]) + 1
    new_book = {
        "id": new_id,
        "title": data.get("title"),
        "author": data.get("author"),
        "genre": data.get("genre"),
        "price": data.get("price"),
        "published_year": data.get("published_year"),
        "available": data.get("available", True),
        "created_at": datetime.datetime.now().isoformat() + "Z"
    }
    books.append(new_book)
    return jsonify({"data": new_book}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"API Server running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
