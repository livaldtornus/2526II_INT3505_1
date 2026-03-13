from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-123-with-more-bytes-for-sha256'

users = {
    "alice": "password123",
    "bob": "securepassword"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    if username in users and users[username] == password:
        # Create JWT token
        headers = {
            "typ": "JWT",
            "alg": "HS256"
        }
        payload = {
            'username': username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256', headers=headers)
        
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]

    try:
        # Decode token
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({
            "message": f"Hello, {decoded['username']}! Here is your protected data.",
            "data": "This is highly confidential."
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    print("JWT Server running on http://localhost:5005")
    app.run(port=5005, debug=True)
