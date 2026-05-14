# Lecture 10: Service Operation - Security & Monitoring

Demo Flask API cho hai nhóm kiến thức chính:

- Observability: structured logs, audit logs, Prometheus metrics, trace/request id.
- Production security: security headers, WAF cơ bản, rate limiting, API key authorization, audit logs.

## Chạy API

```bash
cd Lecture_10
python app.py
```

API chạy ở:

```text
http://127.0.0.1:5010
```

## Điểm cần chỉ trong code khi demo

| Kiến thức | File | Vị trí demo |
| --- | --- | --- |
| Structured logging | `observability.py` | `JsonFormatter`, `app_logger`, `setup_observability()` |
| Metrics Prometheus | `observability.py`, `app.py` | `MetricsStore.render_prometheus()`, endpoint `/metrics` |
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
