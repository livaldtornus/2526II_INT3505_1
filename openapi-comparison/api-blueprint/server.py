"""
server.py — API Blueprint Doc Server
=====================================
Đọc file .apib và render thành trang HTML tài liệu API.

Thư viện dùng:
  - Flask        : web server
  - mistune      : render Markdown → HTML (apib là Markdown-based)

Cài đặt:
    pip install flask mistune

Chạy:
    python server.py

Mở trình duyệt:
    http://localhost:8001/docs
"""

import os
import re
import mistune
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
APIB_FILE = os.path.join(os.path.dirname(__file__), "library_api.apib")

# --- Dữ liệu giả lập ---
books = [
    {"id": 1, "title": "Nhà Giả Kim", "author": "Paulo Coelho", "genre": "fiction", "price": 85000, "available": True},
    {"id": 2, "title": "Đắc Nhân Tâm", "author": "Dale Carnegie", "genre": "non-fiction", "price": 95000, "available": True}
]

members = [
    {"id": 1, "name": "Nguyễn Văn A", "email": "nguyenvana@email.com", "joined_date": "2024-01-01"}
]

# ─── Parse .apib thành sections ─────────────────────────────────────────────

def parse_apib(filepath: str) -> dict:
    """Đọc file .apib và trích xuất metadata + nội dung."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    title = "Library Management API"
    host  = "http://localhost:8001"

    for line in lines[:10]:
        if line.startswith("# ") and not line.startswith("# Group"):
            title = line[2:].strip()
        if line.startswith("HOST:"):
            host = line.replace("HOST:", "").strip()

    # Tách thành các groups
    groups = []
    current_group = None
    current_endpoint = None
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("# Group "):
            if current_group:
                if current_endpoint:
                    current_group["endpoints"].append(current_endpoint)
                    current_endpoint = None
                groups.append(current_group)
            current_group = {"name": line[8:].strip(), "endpoints": []}
            current_endpoint = None

        elif line.startswith("## ") and current_group is not None:
            if current_endpoint:
                current_group["endpoints"].append(current_endpoint)
            name = line[3:].strip()
            current_endpoint = {"name": name, "actions": []}

        elif line.startswith("### ") and current_endpoint is not None:
            match = re.match(r"### (.+?) \[(GET|POST|PUT|DELETE|PATCH)\s*(.*?)\]", line)
            if match:
                action_name  = match.group(1).strip()
                method       = match.group(2).strip()
                path_override = match.group(3).strip()
                current_endpoint["actions"].append({
                    "name": action_name,
                    "method": method,
                    "path": path_override or "",
                })

        i += 1

    if current_group:
        if current_endpoint:
            current_group["endpoints"].append(current_endpoint)
        groups.append(current_group)

    # Convert toàn bộ nội dung sang HTML bằng mistune
    md = mistune.create_markdown(
        plugins=["table"],
    )
    html_body = md(content)

    return {"title": title, "host": host, "groups": groups, "html_body": html_body}


# ─── HTML Template ────────────────────────────────────────────────────────────

TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{{ data.title }} — API Blueprint</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; font-family: 'Segoe UI', sans-serif; background: #f0f4f8; color: #2d3748; }

    /* Banner */
    header {
      background: linear-gradient(135deg, #2b6cb0, #2c5282);
      color: #fff; padding: 20px 32px;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: 0 2px 10px rgba(0,0,0,.3);
    }
    header h1 { margin: 0; font-size: 1.3rem; }
    header h1 span { color: #90cdf4; }
    header .badge {
      background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.3);
      border-radius: 6px; padding: 6px 14px; font-size: .8rem; opacity: .9;
    }

    /* Layout */
    .container { max-width: 960px; margin: 0 auto; padding: 32px 16px; }

    /* Info box */
    .info-box {
      background: #fff; border-radius: 10px; padding: 20px 24px;
      margin-bottom: 28px; box-shadow: 0 1px 4px rgba(0,0,0,.08);
      display: flex; gap: 32px; align-items: center;
    }
    .info-box .label { font-size: .75rem; text-transform: uppercase; color: #718096; }
    .info-box .value { font-weight: 600; color: #2b6cb0; }

    /* Group card */
    .group { margin-bottom: 32px; }
    .group-title {
      font-size: 1rem; font-weight: 700; text-transform: uppercase;
      letter-spacing: 1px; color: #4a5568; margin-bottom: 12px;
      padding-left: 12px; border-left: 4px solid #3182ce;
    }
    .endpoint {
      background: #fff; border-radius: 10px;
      box-shadow: 0 1px 4px rgba(0,0,0,.08);
      margin-bottom: 12px; overflow: hidden;
    }
    .endpoint-header {
      padding: 14px 20px; font-weight: 600; font-size: .95rem;
      background: #ebf8ff; border-bottom: 1px solid #bee3f8;
      color: #2c5282;
    }
    .action {
      padding: 10px 20px; display: flex; align-items: center; gap: 14px;
      border-bottom: 1px solid #f7fafc; font-size: .9rem;
    }
    .action:last-child { border-bottom: none; }

    /* Method badges */
    .method {
      padding: 3px 10px; border-radius: 4px; font-size: .75rem;
      font-weight: 700; min-width: 60px; text-align: center; color: #fff;
    }
    .GET    { background: #38a169; }
    .POST   { background: #3182ce; }
    .PUT    { background: #dd6b20; }
    .DELETE { background: #e53e3e; }
    .PATCH  { background: #805ad5; }

    /* Full markdown section */
    .raw-docs {
      background: #fff; border-radius: 10px; padding: 28px 32px;
      box-shadow: 0 1px 4px rgba(0,0,0,.08); margin-top: 36px;
    }
    .raw-docs h1 { border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
    .raw-docs h2 { color: #2b6cb0; margin-top: 28px; }
    .raw-docs h3 { color: #2c5282; }
    .raw-docs code {
      background: #edf2f7; padding: 2px 6px; border-radius: 4px;
      font-family: 'Fira Code', monospace; font-size: .85em;
    }
    .raw-docs pre {
      background: #1a202c; color: #e2e8f0; padding: 16px 20px;
      border-radius: 8px; overflow-x: auto; font-size: .85rem;
      line-height: 1.6;
    }
    .raw-docs pre code { background: none; padding: 0; color: inherit; }
  </style>
</head>
<body>

<header>
  <div>
    <h1>📚 <span>{{ data.title }}</span></h1>
    <small style="opacity:.7">API Blueprint Format · Rendered by Flask</small>
  </div>
  <div class="badge">🌐 HOST: {{ data.host }}</div>
</header>

<div class="container">

  <!-- Info -->
  <div class="info-box">
    <div>
      <div class="label">Format</div>
      <div class="value">API Blueprint 1A</div>
    </div>
    <div>
      <div class="label">Base URL</div>
      <div class="value">{{ data.host }}</div>
    </div>
    <div>
      <div class="label">Endpoints</div>
      <div class="value">
        {% set count = namespace(n=0) %}
        {% for g in data.groups %}{% for e in g.endpoints %}{% for a in e.actions %}{% set count.n = count.n + 1 %}{% endfor %}{% endfor %}{% endfor %}
        {{ count.n }} actions
      </div>
    </div>
  </div>

  <!-- Endpoint Summary -->
  {% for group in data.groups %}
  <div class="group">
    <div class="group-title">{{ group.name }}</div>
    {% for endpoint in group.endpoints %}
    <div class="endpoint">
      <div class="endpoint-header">{{ endpoint.name }}</div>
      {% for action in endpoint.actions %}
      <div class="action">
        <span class="method {{ action.method }}">{{ action.method }}</span>
        <span>{{ action.name }}</span>
        {% if action.path %}<code style="margin-left:auto;color:#718096;font-size:.8rem">{{ action.path }}</code>{% endif %}
      </div>
      {% endfor %}
    </div>
    {% endfor %}
  </div>
  {% endfor %}

  <!-- Full rendered Markdown -->
  <div class="raw-docs">
    <h2 style="margin-top:0">📄 Full Documentation</h2>
    {{ data.html_body | safe }}
  </div>

</div>
</body>
</html>
"""

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    from flask import redirect
    return redirect("/docs")

@app.route("/docs")
def docs():
    data = parse_apib(APIB_FILE)
    return render_template_string(TEMPLATE, data=data)

@app.route("/raw")
def raw():
    """Trả về nội dung .apib gốc."""
    with open(APIB_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    from flask import Response
    return Response(content, mimetype="text/plain; charset=utf-8")

# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.route("/api/v1/books", methods=["GET"])
def list_books():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    search = request.args.get("search", "").lower()
    
    filtered = [b for b in books if search in b["title"].lower() or search in b["author"].lower()]
    start = (page - 1) * limit
    end = start + limit
    
    return jsonify({
        "total": len(filtered),
        "page": page,
        "limit": limit,
        "data": filtered[start:end]
    }), 200

@app.route("/api/v1/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book: return jsonify({"error": "NOT_FOUND", "message": "Không tìm thấy sách"}), 404
    return jsonify({"data": book}), 200

@app.route("/api/v1/books", methods=["POST"])
def create_book():
    data = request.json
    new_id = max([b["id"] for b in books] + [0]) + 1
    new_book = {**data, "id": new_id, "created_at": datetime.datetime.now().isoformat() + "Z"}
    books.append(new_book)
    return jsonify({"data": new_book}), 201

@app.route("/api/v1/members", methods=["GET"])
def list_members():
    return jsonify({"total": len(members), "data": members}), 200

@app.route("/api/v1/members", methods=["POST"])
def create_member():
    data = request.json
    new_id = max([m["id"] for m in members] + [0]) + 1
    new_member = {**data, "id": new_id, "joined_date": datetime.date.today().isoformat()}
    members.append(new_member)
    return jsonify({"data": new_member}), 201

# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    print(f"\n{'='*50}")
    print(f"  📚  API Blueprint Doc Server")
    print(f"  🌐  http://localhost:{port}/docs")
    print(f"  📄  http://localhost:{port}/raw  (file gốc .apib)")
    print(f"{'='*50}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
