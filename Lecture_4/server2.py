import os
from flask import Flask, send_file, redirect
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = "/docs"
API_URL = "/openapi.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Book Management API"}
)

app.register_blueprint(swaggerui_blueprint)


@app.route("/")
def index():
    return redirect("/docs")


@app.route("/openapi.yaml")
def serve_yaml():
    return send_file("books_api.yaml", mimetype="text/yaml")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
