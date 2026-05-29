from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from functools import wraps
from uuid import uuid4

from flask import Flask, jsonify, request


app = Flask(__name__)


PLANS = {
    "free": {
        "name": "Free",
        "monthly_fee_usd": 0,
        "included_calls": 1000,
        "price_per_1000_extra_calls_usd": 0,
        "rate_limit_per_minute": 10,
        "support": "community",
        "best_for": "Sinh vien va developer dang thu nghiem sandbox",
    },
    "pro": {
        "name": "Pro",
        "monthly_fee_usd": 29,
        "included_calls": 50000,
        "price_per_1000_extra_calls_usd": 0.8,
        "rate_limit_per_minute": 100,
        "support": "email",
        "best_for": "Startup tich hop vao san pham that",
    },
    "enterprise": {
        "name": "Enterprise",
        "monthly_fee_usd": "custom",
        "included_calls": "custom",
        "price_per_1000_extra_calls_usd": "custom",
        "rate_limit_per_minute": 1000,
        "support": "SLA + dedicated channel",
        "best_for": "Doi tac co call volume lon va can SLA",
    },
}


BUSINESS_MODEL_CANVAS = {
    "api_name": "Campus Deals API",
    "value_propositions": [
        "Cung cap danh sach uu dai gan truong theo vi tri, danh muc va ngan sach.",
        "Giam thoi gian tich hop cho app sinh vien bang docs, sandbox va API key tu dong.",
        "Tra ve du lieu on dinh kem analytics de doi tac theo doi hieu qua tich hop.",
    ],
    "customer_segments": [
        "Ung dung sinh vien",
        "Nha phat trien chatbot noi bo truong",
        "Doi tac thuong mai muon tiep can cong dong sinh vien",
    ],
    "channels": [
        "Developer portal",
        "Tai lieu API va sample client",
        "Workshop hackathon va sandbox public",
    ],
    "customer_relationships": [
        "Self-service onboarding",
        "Email support cho goi Pro",
        "SLA rieng cho Enterprise",
    ],
    "revenue_streams": [
        "Freemium cho developer moi",
        "Pay-per-call khi vuot quota",
        "Enterprise contract cho doi tac can du lieu rieng",
    ],
    "key_resources": [
        "Deal database",
        "API gateway, API keys va quota",
        "Analytics dashboard",
    ],
    "key_activities": [
        "Cap nhat du lieu uu dai",
        "Duy tri docs va sandbox",
        "Theo doi KPI: developer signup, call volume, error rate",
    ],
    "key_partners": [
        "Quan ca phe, nha sach, phong gym gan truong",
        "Cau lac bo sinh vien",
        "Bo phan IT cua truong",
    ],
    "cost_structure": [
        "Hosting va monitoring",
        "Cham soc doi tac cung cap deal",
        "Ho tro developer va van hanh portal",
    ],
}


DEALS = [
    {
        "id": "deal_001",
        "title": "Giam 20% ca phe sang",
        "merchant": "Campus Coffee",
        "category": "food",
        "distance_meters": 250,
        "student_price_vnd": 32000,
    },
    {
        "id": "deal_002",
        "title": "Combo sach lap trinh",
        "merchant": "Tech Bookstore",
        "category": "books",
        "distance_meters": 900,
        "student_price_vnd": 180000,
    },
    {
        "id": "deal_003",
        "title": "Ve tap gym 7 ngay",
        "merchant": "FitHub",
        "category": "fitness",
        "distance_meters": 1200,
        "student_price_vnd": 99000,
    },
]


developers = {}
usage_windows = defaultdict(deque)
analytics = {
    "total_calls": 0,
    "total_errors": 0,
    "by_endpoint": defaultdict(lambda: {"calls": 0, "errors": 0}),
    "by_api_key": defaultdict(lambda: {"calls": 0, "errors": 0}),
}


def now_iso():
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def public_developer(developer):
    data = dict(developer)
    data["api_key"] = developer["api_key"][:12] + "..."
    return data


def track_api_call(response):
    if not request.path.startswith("/api/"):
        return response

    endpoint = request.url_rule.rule if request.url_rule else request.path
    api_key = request.headers.get("X-API-Key", "anonymous")
    is_error = response.status_code >= 400

    analytics["total_calls"] += 1
    analytics["by_endpoint"][endpoint]["calls"] += 1
    analytics["by_api_key"][api_key]["calls"] += 1

    if is_error:
        analytics["total_errors"] += 1
        analytics["by_endpoint"][endpoint]["errors"] += 1
        analytics["by_api_key"][api_key]["errors"] += 1

    response.headers["X-API-Product"] = "Campus Deals API"
    return response


app.after_request(track_api_call)


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        developer = developers.get(api_key)
        if not developer:
            return jsonify({
                "error": "invalid_api_key",
                "message": "Dang ky tai /api/developers/register de nhan API key demo.",
            }), 401

        plan = PLANS[developer["plan"]]
        window = usage_windows[api_key]
        cutoff = datetime.now(UTC) - timedelta(minutes=1)
        while window and window[0] < cutoff:
            window.popleft()

        if len(window) >= plan["rate_limit_per_minute"]:
            return jsonify({
                "error": "rate_limit_exceeded",
                "message": "Ban da vuot quota theo phut cua goi hien tai.",
                "plan": developer["plan"],
                "rate_limit_per_minute": plan["rate_limit_per_minute"],
                "upgrade_url": "/api/plans",
            }), 429

        window.append(datetime.now(UTC))
        return func(developer, *args, **kwargs)

    return wrapper


def filter_deals(category=None, max_distance=None):
    results = list(DEALS)
    if category:
        results = [deal for deal in results if deal["category"] == category]
    if max_distance is not None:
        results = [deal for deal in results if deal["distance_meters"] <= max_distance]
    return results


@app.route("/")
def developer_portal():
    return """
    <!doctype html>
    <html lang="vi">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Campus Deals API Developer Portal</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; color: #17202a; background: #f6f8fa; }
            header { background: #0f766e; color: white; padding: 32px 40px; }
            main { max-width: 1040px; margin: 0 auto; padding: 28px 20px 48px; }
            section { background: white; border: 1px solid #d8dee4; border-radius: 8px; padding: 20px; margin-bottom: 18px; }
            h1, h2 { margin-top: 0; }
            code, pre { background: #eef2f7; border-radius: 6px; }
            code { padding: 2px 6px; }
            pre { padding: 14px; overflow-x: auto; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
            .metric { border-left: 4px solid #0f766e; padding-left: 12px; }
            a { color: #0f766e; font-weight: bold; }
        </style>
    </head>
    <body>
        <header>
            <h1>Campus Deals API</h1>
            <p>Developer portal demo: docs, sandbox, pricing va analytics cho mot API product.</p>
        </header>
        <main>
            <section>
                <h2>Quick Start</h2>
                <pre>curl -X POST http://localhost:5000/api/developers/register \\
  -H "Content-Type: application/json" \\
  -d '{"name":"Demo Team","email":"team@example.com","plan":"free"}'</pre>
                <p>Sau khi co API key, goi <code>/api/v1/deals</code> voi header <code>X-API-Key</code>.</p>
            </section>
            <section class="grid">
                <div class="metric"><h2>Docs</h2><p><a href="/api/docs">/api/docs</a></p></div>
                <div class="metric"><h2>Sandbox</h2><p><a href="/api/sandbox/deals">/api/sandbox/deals</a></p></div>
                <div class="metric"><h2>Pricing</h2><p><a href="/api/plans">/api/plans</a></p></div>
                <div class="metric"><h2>KPIs</h2><p><a href="/api/analytics">/api/analytics</a></p></div>
            </section>
            <section>
                <h2>Launch Strategy</h2>
                <p>Ra mat bang sandbox public, docs co sample request, free tier de tang developer signup,
                sau do theo doi call volume va error rate de cai thien developer experience.</p>
            </section>
        </main>
    </body>
    </html>
    """


@app.route("/api/docs")
def docs():
    return jsonify({
        "api": "Campus Deals API",
        "version": "v1",
        "base_url": "http://localhost:5000",
        "authentication": "Header X-API-Key for production endpoints",
        "developer_experience": {
            "portal": "/",
            "sandbox": "/api/sandbox/deals",
            "sample_client": "python client.py",
        },
        "endpoints": [
            {
                "method": "POST",
                "path": "/api/developers/register",
                "description": "Dang ky developer va nhan API key demo.",
            },
            {
                "method": "GET",
                "path": "/api/v1/deals?category=food&max_distance=1000",
                "description": "Lay deals that, yeu cau X-API-Key.",
            },
            {
                "method": "GET",
                "path": "/api/sandbox/deals",
                "description": "Sandbox khong can API key, du lieu demo on dinh.",
            },
            {
                "method": "GET",
                "path": "/api/analytics",
                "description": "KPI san pham API: developer signup, call volume, error rate.",
            },
        ],
    })


@app.route("/api/developers/register", methods=["POST"])
def register_developer():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    email = payload.get("email")
    plan = payload.get("plan", "free")

    if not name or not email:
        return jsonify({"error": "validation_error", "message": "name va email la bat buoc."}), 400
    if plan not in PLANS:
        return jsonify({"error": "invalid_plan", "available_plans": list(PLANS)}), 400

    api_key = "ck_" + uuid4().hex
    developer = {
        "id": "dev_" + uuid4().hex[:8],
        "name": name,
        "email": email,
        "plan": plan,
        "api_key": api_key,
        "created_at": now_iso(),
    }
    developers[api_key] = developer

    return jsonify({
        "message": "Developer registered",
        "developer": developer,
        "next_steps": [
            "Doc docs tai /api/docs",
            "Thu sandbox tai /api/sandbox/deals",
            "Goi production endpoint /api/v1/deals voi header X-API-Key",
        ],
    }), 201


@app.route("/api/plans")
def plans():
    return jsonify({
        "monetization_model": "freemium + pay-per-call + enterprise contract",
        "plans": PLANS,
    })


@app.route("/api/business-model-canvas")
def business_model_canvas():
    return jsonify(BUSINESS_MODEL_CANVAS)


@app.route("/api/sandbox/deals")
def sandbox_deals():
    return jsonify({
        "mode": "sandbox",
        "data": DEALS[:2],
        "note": "Sandbox khong can API key va dung du lieu demo co dinh.",
    })


@app.route("/api/v1/deals")
@require_api_key
def list_deals(developer):
    category = request.args.get("category")
    max_distance = request.args.get("max_distance", type=int)
    data = filter_deals(category=category, max_distance=max_distance)
    return jsonify({
        "data": data,
        "meta": {
            "count": len(data),
            "developer": public_developer(developer),
            "filters": {
                "category": category,
                "max_distance": max_distance,
            },
        },
    })


@app.route("/api/analytics")
def api_analytics():
    total_calls = analytics["total_calls"]
    total_errors = analytics["total_errors"]
    error_rate = round(total_errors / total_calls, 4) if total_calls else 0

    return jsonify({
        "kpis": {
            "developers_registered": len(developers),
            "call_volume": total_calls,
            "error_rate": error_rate,
        },
        "by_endpoint": analytics["by_endpoint"],
        "developers": [public_developer(developer) for developer in developers.values()],
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "not_found",
        "message": "Endpoint khong ton tai. Xem /api/docs de biet cac endpoint hop le.",
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
