import json
import logging
import time
import uuid
from collections import defaultdict
from pathlib import Path

from flask import g, request
from werkzeug.exceptions import HTTPException


LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        extra_fields = getattr(record, "extra_fields", None)
        if extra_fields:
            payload.update(extra_fields)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)


def build_logger(name, file_name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = JsonFormatter()

    file_handler = logging.FileHandler(LOG_DIR / file_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


app_logger = build_logger("lecture_10.app", "app.log")
audit_logger = build_logger("lecture_10.audit", "audit.log")


class MetricsStore:
    def __init__(self):
        self.http_requests = defaultdict(int)
        self.http_latency_total = defaultdict(float)
        self.security_events = defaultdict(int)
        self.circuit_breaker_state = 0

    def record_request(self, method, path, status_code, duration_seconds):
        labels = (method, path, str(status_code))
        self.http_requests[labels] += 1
        self.http_latency_total[labels] += duration_seconds

    def record_security_event(self, event_type):
        self.security_events[event_type] += 1

    def render_prometheus(self):
        lines = [
            "# HELP flask_http_requests_total Total HTTP requests.",
            "# TYPE flask_http_requests_total counter",
        ]

        for (method, path, status), value in sorted(self.http_requests.items()):
            lines.append(
                'flask_http_requests_total{method="%s",path="%s",status="%s"} %s'
                % (method, path, status, value)
            )

        lines.extend(
            [
                "# HELP flask_http_request_duration_seconds_total Total request duration.",
                "# TYPE flask_http_request_duration_seconds_total counter",
            ]
        )

        for (method, path, status), value in sorted(self.http_latency_total.items()):
            lines.append(
                'flask_http_request_duration_seconds_total{method="%s",path="%s",status="%s"} %.6f'
                % (method, path, status, value)
            )

        lines.extend(
            [
                "# HELP security_events_total Total blocked or audited security events.",
                "# TYPE security_events_total counter",
            ]
        )

        for event_type, value in sorted(self.security_events.items()):
            lines.append('security_events_total{type="%s"} %s' % (event_type, value))

        lines.extend(
            [
                "# HELP circuit_breaker_open Circuit breaker state, 1 is open and 0 is closed.",
                "# TYPE circuit_breaker_open gauge",
                "circuit_breaker_open %s" % self.circuit_breaker_state,
            ]
        )

        return "\n".join(lines) + "\n"


metrics = MetricsStore()


def get_trace_id():
    traceparent = request.headers.get("traceparent", "")
    parts = traceparent.split("-")
    if len(parts) >= 2 and len(parts[1]) == 32:
        return parts[1]
    return request.headers.get("X-Request-Id") or uuid.uuid4().hex


def setup_observability(app):
    @app.before_request
    def start_request_trace():
        g.started_at = time.perf_counter()
        g.trace_id = get_trace_id()

    @app.after_request
    def record_request_metrics(response):
        duration = time.perf_counter() - g.get("started_at", time.perf_counter())
        route = request.url_rule.rule if request.url_rule else request.path

        metrics.record_request(request.method, route, response.status_code, duration)
        response.headers["X-Request-Id"] = g.get("trace_id", "")

        app_logger.info(
            "request_completed",
            extra={
                "extra_fields": {
                    "trace_id": g.get("trace_id"),
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                    "remote_addr": request.remote_addr,
                    "user_agent": request.headers.get("User-Agent", ""),
                }
            },
        )

        return response

    @app.errorhandler(Exception)
    def log_unhandled_exception(error):
        if isinstance(error, HTTPException):
            return {"error": error.name, "message": error.description, "trace_id": g.get("trace_id")}, error.code

        app_logger.exception(
            "unhandled_exception",
            extra={
                "extra_fields": {
                    "trace_id": g.get("trace_id"),
                    "method": request.method,
                    "path": request.path,
                }
            },
        )
        return {"error": "Internal Server Error", "trace_id": g.get("trace_id")}, 500
