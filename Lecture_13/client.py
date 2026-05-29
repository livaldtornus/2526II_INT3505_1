import json
import time

import requests


BASE_URL = "http://localhost:5000"


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def get(path, api_key=None, params=None):
    headers = {"X-API-Key": api_key} if api_key else {}
    response = requests.get(f"{BASE_URL}{path}", headers=headers, params=params, timeout=5)
    print(f"GET {path} -> {response.status_code}")
    print_json(response.json())
    return response


def post(path, payload):
    response = requests.post(f"{BASE_URL}{path}", json=payload, timeout=5)
    print(f"POST {path} -> {response.status_code}")
    print_json(response.json())
    return response


def register_developer():
    print_section("1. Developer signup: dang ky va nhan API key")
    response = post("/api/developers/register", {
        "name": "Lecture 13 Demo Team",
        "email": "demo-team@example.com",
        "plan": "free",
    })
    response.raise_for_status()
    api_key = response.json()["developer"]["api_key"]
    print(f"\nAPI key dung cho cac request tiep theo: {api_key}")
    return api_key


def view_developer_experience():
    print_section("2. Developer experience: docs, sandbox va pricing")
    get("/api/docs")
    get("/api/sandbox/deals")
    get("/api/plans")


def view_business_model_canvas():
    print_section("3. Business Model Canvas cho API")
    get("/api/business-model-canvas")


def call_production_api(api_key):
    print_section("4. Production API: goi endpoint co API key va query params")
    get("/api/v1/deals", api_key=api_key, params={
        "category": "food",
        "max_distance": 1000,
    })


def simulate_errors_and_kpis(api_key):
    print_section("5. Analytics: tao call volume va error rate")
    print("Goi sai API key de tao 401 error:")
    get("/api/v1/deals", api_key="ck_invalid_key")

    print("\nGoi hop le them 3 lan de tang call volume:")
    for index in range(3):
        print(f"\nLan {index + 1}:")
        get("/api/v1/deals", api_key=api_key)

    print("\nDoc KPI analytics:")
    get("/api/analytics")


def main():
    try:
        time.sleep(0.5)
        api_key = register_developer()
        view_developer_experience()
        view_business_model_canvas()
        call_production_api(api_key)
        simulate_errors_and_kpis(api_key)
    except requests.exceptions.ConnectionError:
        print("Khong the ket noi server. Hay chay: python server.py")
    except requests.exceptions.Timeout:
        print("Request timeout. Kiem tra server Flask co dang chay khong.")


if __name__ == "__main__":
    main()
