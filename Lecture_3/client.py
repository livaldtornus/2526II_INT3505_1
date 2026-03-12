import requests, json, uuid, time

BASE = "http://localhost:6000"

def show(label, r):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"  Status : {r.status_code}")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

def get_balance():
    r = requests.get(f"{BASE}/balance")
    print(f"\n  >>> Balance hiện tại: {r.json()['balance']:,}")

def pay(label, idem_key, amount):
    r = requests.post(
        f"{BASE}/payment",
        json={"amount": amount},
        headers={"Idempotency-Key": idem_key},
    )
    show(label, r)
    return r


if __name__ == "__main__":
    get_balance()

    print("\n" + "━"*50)
    print("  DEMO 1: Thanh toán bình thường")
    print("━"*50)
    key1 = str(uuid.uuid4())
    pay("POST /payment (lần 1)", key1, 100000)
    get_balance()

    print("\n" + "━"*50)
    print("  DEMO 2: Gửi lại ĐÚNG key cũ (giả lập double-click / retry)")
    print("  → Server nhận ra duplicate, KHÔNG trừ tiền lần 2")
    print("━"*50)
    pay("POST /payment (lần 2, same key)", key1, 100000)
    get_balance()

    print("\n" + "━"*50)
    print("  DEMO 3: Gửi lại lần 3 cùng key → vẫn không trừ")
    print("━"*50)
    pay("POST /payment (lần 3, same key)", key1, 100000)
    get_balance()

    print("\n" + "━"*50)
    print("  DEMO 4: Thanh toán MỚI với key mới → trừ tiền bình thường")
    print("━"*50)
    key2 = str(uuid.uuid4())
    pay("POST /payment (key mới)", key2, 200000)
    get_balance()

    print("\n" + "━"*50)
    print("  DEMO 5: Không có Idempotency-Key → 400")
    print("━"*50)
    r = requests.post(f"{BASE}/payment", json={"amount": 50000})
    show("POST /payment (no key)", r)

    print("\n" + "━"*50)
    print("  DEMO 6: Số dư không đủ → 422")
    print("━"*50)
    key3 = str(uuid.uuid4())
    pay("POST /payment (quá số dư)", key3, 9999999)
    get_balance()
