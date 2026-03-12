from flask import Flask, request, jsonify
import time

app = Flask(__name__)

balance = {"amount": 1000000}

processed = {}

@app.route("/payment", methods=["POST"])
def payment():
    idem_key = request.headers.get("Idempotency-Key")

    if not idem_key:
        return jsonify({"error": "Missing Idempotency-Key header"}), 400

    if idem_key in processed:
        cached = processed[idem_key]
        print(f"[DUPLICATE] key={idem_key} → trả kết quả cũ")
        return jsonify({**cached, "duplicate": True}), 200

    data = request.json
    amount = data.get("amount", 0)

    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    if balance["amount"] < amount:
        return jsonify({"error": "Insufficient balance"}), 422

    balance["amount"] -= amount

    result = {
        "status": "success",
        "amount": amount,
        "remaining_balance": balance["amount"],
        "processed_at": time.strftime("%H:%M:%S"),
        "idempotency_key": idem_key,
        "duplicate": False,
    }

    processed[idem_key] = result
    print(f"[NEW] key={idem_key} amount={amount} balance={balance['amount']}")

    return jsonify(result), 201


@app.route("/balance", methods=["GET"])
def get_balance():
    return jsonify({"balance": balance["amount"]}), 200


if __name__ == "__main__":
    print("Server running on http://localhost:6000")
    print(f"Initial balance: {balance['amount']}")
    app.run(port=6000, debug=True)
