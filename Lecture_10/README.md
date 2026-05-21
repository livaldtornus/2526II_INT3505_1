# Lecture 10: Service Operation - Security & Monitoring

Demo Flask API cho hai nhóm kiến thức chính:

- Observability: structured logs, audit logs, Prometheus metrics, trace/request id.
- Production security: security headers, WAF cơ bản, rate limiting, API key authorization, audit logs.

## Chạy API

```bash
cd Lecture_10
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

API chạy ở:

```text
http://127.0.0.1:5010
```

## Deploy Kubernetes local bằng Docker/kind

Chuẩn bị tool local, không cần sudo:

```bash
cd Lecture_10
./scripts/install-k8s-tools.sh
export PATH="$PWD/bin:$PATH"
```

Tạo Kubernetes cluster bằng Docker, build image API, load image vào cluster và apply manifest:

```bash
./scripts/bootstrap-kind.sh
```

Các URL sau khi deploy:

```text
API:        http://127.0.0.1:8080
Prometheus: http://127.0.0.1:19090
Grafana:    http://127.0.0.1:3000
```

Grafana login:

```text
username: admin
password: admin
```

Xóa cluster:

```bash
./scripts/delete-kind.sh
```

Các manifest chính:

| Nhóm | File |
| --- | --- |
| API Deployment/Service/Secret | `k8s/app/*.yaml` |
| Prometheus scrape pod metrics | `k8s/observability/10-prometheus-rbac.yaml`, `k8s/observability/11-prometheus.yaml` |
| Logging stdout sang Loki | `k8s/observability/20-loki.yaml`, `k8s/observability/21-promtail.yaml` |
| Tracing OTLP sang Tempo | `k8s/observability/30-tempo.yaml`, `k8s/observability/31-otel-collector.yaml` |
| Grafana datasources | `k8s/observability/40-grafana.yaml` |

Luồng observability trên Kubernetes:

```text
API stdout JSON logs -> Promtail -> Loki -> Grafana
API /metrics -> Prometheus -> Grafana
API OTLP traces -> OpenTelemetry Collector -> Tempo -> Grafana
```

## Điểm cần chỉ trong code khi demo

| Kiến thức | File | Vị trí demo |
| --- | --- | --- |
| Structured logging | `observability.py` | `JsonFormatter`, `app_logger`, `setup_observability()` |
| Metrics Prometheus | `observability.py`, `app.py`, `prometheus.yml` | `prometheus_client`, endpoint `/metrics`, Prometheus scrape config |
| Tracing/request id | `observability.py` | `get_trace_id()`, header `X-Request-Id` |
| Audit logs | `security.py` | hàm `audit()`, file `logs/audit.log` |
| WAF cơ bản | `security.py` | `SUSPICIOUS_PATTERNS`, `waf_and_rate_limit()` |
| Rate limiting | `security.py` | `FixedWindowRateLimiter`, giới hạn 8 request/phút/client |
| Security headers | `security.py` | `add_security_headers()` |
| API key authorization | `security.py`, `app.py` | `require_api_key()`, endpoint `POST /api/v1/orders` |
| Circuit breaker | `app.py` | `CircuitBreaker`, `call_inventory_service()` |

## Lệnh demo nhanh

Health check:

```bash
curl http://127.0.0.1:5010/health
```

Xem metrics theo format Prometheus:

```bash
curl http://127.0.0.1:5010/metrics
```

Chạy Prometheus bằng Docker để scrape API:

```bash
docker run --rm --name lecture-10-prometheus \
  --add-host=host.docker.internal:host-gateway \
  -p 9090:9090 \
  -v "$PWD/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus
```

Mở Prometheus UI:

```text
http://127.0.0.1:9090
```

Query demo trong Prometheus:

```promql
flask_http_requests_total
rate(flask_http_requests_total[1m])
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))
security_events_total
circuit_breaker_open
```

Query demo sau khi deploy Kubernetes:

```bash
curl http://127.0.0.1:8080/api/v1/products
curl -X POST http://127.0.0.1:8080/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: demo-service-key" \
  -d '{"product_id": 1, "quantity": 2}'
curl "http://127.0.0.1:8080/api/v1/products?q=%3Cscript%3Ealert(1)%3C/script%3E"
```

Prometheus queries:

```promql
flask_http_requests_total{app="lecture-10-api"}
rate(flask_http_requests_total{app="lecture-10-api"}[1m])
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket{app="lecture-10-api"}[5m]))
security_events_total{app="lecture-10-api"}
circuit_breaker_open{app="lecture-10-api"}
```

Grafana Loki query:

```logql
{app="lecture-10-api"}
```

Grafana Tempo:

```text
Explore -> Tempo -> Search -> Service Name: lecture-10-api
```

Gọi API có trace id:

```bash
curl -H "X-Request-Id: demo-trace-001" http://127.0.0.1:5010/api/v1/products
```

Tạo order thành công với API key service:

```bash
curl -X POST http://127.0.0.1:5010/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: demo-service-key" \
  -d '{"product_id": 1, "quantity": 2}'
```

Demo authorization fail:

```bash
curl -X POST http://127.0.0.1:5010/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

Demo WAF chặn payload nguy hiểm:

```bash
curl "http://127.0.0.1:5010/api/v1/products?q=%3Cscript%3Ealert(1)%3C/script%3E"
```

Demo rate limit, gọi quá 8 lần trong 1 phút:

```bash
for i in {1..10}; do curl -i http://127.0.0.1:5010/api/v1/products; done
```

Demo circuit breaker, ép inventory service fail 3 lần:

```bash
for i in {1..4}; do
  curl -X POST "http://127.0.0.1:5010/api/v1/orders?fail_inventory=true" \
    -H "Content-Type: application/json" \
    -H "X-Api-Key: demo-service-key" \
    -d '{"product_id": 1, "quantity": 1}'
done
```

Xem log:

```bash
tail -f logs/app.log
tail -f logs/audit.log
```

## Gợi ý chia commit

Commit 1:

```text
Add Lecture 10 observability demo
```

Nội dung: `app.py`, `observability.py`, endpoint `/metrics`, `/health`, request logs và trace id.

Commit 2:

```text
Add Lecture 10 production security controls
```

Nội dung: `security.py`, WAF cơ bản, rate limiting, security headers, API key authorization, audit logs, README demo.
