"""
server.py — Swagger UI Server cho Book Management API
=====================================================
Yêu cầu:
    pip install flask pyyaml

Chạy:
    python server.py

Sau đó mở trình duyệt tại:
    http://localhost:8000/docs   ← Swagger UI
    http://localhost:8000/openapi.yaml ← Raw YAML spec
"""

import os
import socket
import yaml
from flask import Flask, jsonify, send_file, render_template_string

# ─── Cấu hình ────────────────────────────────────────────────────────────────
YAML_FILE = "books_api.yaml"   # Đặt cùng thư mục với server.py
HOST      = "0.0.0.0"
PORT      = 8000

app = Flask(__name__)

# ─── Helper ──────────────────────────────────────────────────────────────────

def get_local_ip() -> str:
    """Lấy địa chỉ IP nội bộ của máy để chia sẻ trong LAN."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ─── Swagger UI HTML template ─────────────────────────────────────────────────
SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>📚 Book Management API — Swagger UI</title>
  <link rel="stylesheet"
        href="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui.css" />
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #f7f9fc; font-family: sans-serif; }

    /* ── Top banner ── */
    #banner {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: #fff;
      padding: 18px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 12px rgba(0,0,0,.35);
    }
    #banner h1 { margin: 0; font-size: 1.25rem; letter-spacing: .5px; }
    #banner h1 span { color: #e94560; }
    #banner small { opacity: .7; display: block; margin-top: 2px; font-size: .78rem; }

    /* ── Share box ── */
    #share-box {
      background: rgba(255,255,255,.08);
      border: 1px solid rgba(255,255,255,.18);
      border-radius: 8px;
      padding: 10px 18px;
      text-align: right;
    }
    #share-box p { margin: 0 0 6px; font-size: .78rem; opacity: .75; }
    #share-box a {
      color: #4dd0e1;
      text-decoration: none;
      font-size: .88rem;
      font-weight: 600;
    }
    #share-box a:hover { text-decoration: underline; }

    /* ── Copy button ── */
    #copy-btn {
      margin-left: 10px;
      padding: 3px 10px;
      border: 1px solid #4dd0e1;
      border-radius: 4px;
      background: transparent;
      color: #4dd0e1;
      cursor: pointer;
      font-size: .78rem;
      transition: background .2s;
    }
    #copy-btn:hover { background: #4dd0e130; }

    /* ── Swagger wrapper ── */
    #swagger-ui { max-width: 1200px; margin: 0 auto; padding: 24px 16px 48px; }

    /* slight style tweaks for Swagger */
    .swagger-ui .topbar { display: none; }
    .swagger-ui .info .title { color: #1a1a2e; }
  </style>
</head>
<body>

<div id="banner">
  <div>
    <h1>📚 <span>Book</span> Management API</h1>
    <small>OpenAPI 3.0 · Swagger UI {{ swagger_version }}</small>
  </div>
  <div id="share-box">
    <p>🔗 Chia sẻ link trong LAN</p>
    <a id="lan-link" href="{{ lan_url }}" target="_blank">{{ lan_url }}</a>
    <button id="copy-btn" onclick="copyLink()">Copy</button>
  </div>
</div>

<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
<script src="https://unpkg.com/swagger-ui-dist@5.17.14/swagger-ui-standalone-preset.js"></script>
<script>
  window.onload = () => {
    SwaggerUIBundle({
      url: "/openapi.yaml",
      dom_id: "#swagger-ui",
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIStandalonePreset
      ],
      plugins: [SwaggerUIBundle.plugins.DownloadUrl],
      layout: "StandaloneLayout",
      deepLinking: true,
      displayRequestDuration: true,
      defaultModelsExpandDepth: 2,
      defaultModelExpandDepth: 2,
      docExpansion: "list",        // "list" | "full" | "none"
      filter: true,
      syntaxHighlight: { activate: true, theme: "monokai" },
      tryItOutEnabled: true,
    });
  };

  function copyLink() {
    const url = document.getElementById("lan-link").href;
    navigator.clipboard.writeText(url).then(() => {
      const btn = document.getElementById("copy-btn");
      btn.textContent = "✓ Copied!";
      setTimeout(() => btn.textContent = "Copy", 2000);
    });
  }
</script>
</body>
</html>
"""

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Redirect root → /docs"""
    from flask import redirect
    return redirect("/docs")


@app.route("/docs")
def swagger_ui():
    """Render trang Swagger UI."""
    local_ip = get_local_ip()
    lan_url   = f"http://{local_ip}:{PORT}/docs"
    return render_template_string(
        SWAGGER_UI_HTML,
        lan_url=lan_url,
        swagger_version="5.17",
    )


@app.route("/openapi.yaml")
def serve_yaml():
    """Trả về file OpenAPI YAML gốc."""
    yaml_path = os.path.join(os.path.dirname(__file__), YAML_FILE)
    if not os.path.exists(yaml_path):
        return jsonify({"error": f"Không tìm thấy file {YAML_FILE}"}), 404
    return send_file(yaml_path, mimetype="text/yaml")


@app.route("/openapi.json")
def serve_json():
    """Trả về spec dưới dạng JSON (tiện cho các tool khác)."""
    yaml_path = os.path.join(os.path.dirname(__file__), YAML_FILE)
    if not os.path.exists(yaml_path):
        return jsonify({"error": f"Không tìm thấy file {YAML_FILE}"}), 404
    with open(yaml_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    return jsonify(spec)


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "api": "Book Management API"})


# ─── Startup ──────────────────────────────────────────────────────────────────

def print_banner():
    local_ip = get_local_ip()
    print("\n" + "=" * 55)
    print("  📚  Book Management API — Swagger UI Server")
    print("=" * 55)
    print(f"  🏠  Local  :  http://localhost:{PORT}/docs")
    print(f"  🌐  LAN    :  http://{local_ip}:{PORT}/docs")
    print(f"  📄  YAML   :  http://localhost:{PORT}/openapi.yaml")
    print(f"  📦  JSON   :  http://localhost:{PORT}/openapi.json")
    print("=" * 55)
    print("  Nhấn Ctrl+C để dừng server.\n")


if __name__ == "__main__":
    # Kiểm tra file YAML tồn tại trước khi khởi động
    yaml_path = os.path.join(os.path.dirname(__file__), YAML_FILE)
    if not os.path.exists(yaml_path):
        print(f"[LỖI] Không tìm thấy '{YAML_FILE}'.")
        print(f"       Hãy đặt file YAML cùng thư mục với server.py.")
        exit(1)

    print_banner()
    app.run(host=HOST, port=PORT, debug=False)
