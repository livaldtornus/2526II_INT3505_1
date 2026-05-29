# Buoi 13: API as a Product

Demo nay minh hoa cach xem API nhu mot san pham:

- Developer portal: `GET /`
- Docs: `GET /api/docs`
- Sandbox: `GET /api/sandbox/deals`
- Developer signup va API key: `POST /api/developers/register`
- Monetization plans: `GET /api/plans`
- Business Model Canvas: `GET /api/business-model-canvas`
- KPI analytics: `GET /api/analytics`
- Production API co auth va quota: `GET /api/v1/deals`

## Chay demo

Terminal 1:

```bash
pip install -r requirements.txt
python server.py
```

Terminal 2:

```bash
python client.py
```

Mo developer portal tai:

```text
http://localhost:5000
```

## Noi dung can quan sat

- Developer experience: portal, docs, sandbox va sample client.
- Monetization: freemium, pay-per-call khi vuot quota, enterprise contract.
- KPI: so developer dang ky, call volume, error rate.
- Product operations: API key, quota theo plan, endpoint analytics.
