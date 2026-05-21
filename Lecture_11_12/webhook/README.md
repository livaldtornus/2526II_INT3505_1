# Mẫu thiết kế Webhook & Event-driven

## Mô tả
Trong kiến trúc truyền thống, nếu hệ thống A muốn biết hệ thống B đã xử lý xong việc chưa, nó phải liên tục "hỏi" (Polling) ví dụ: cứ 5 giây gọi API `GET /status` một lần. Việc này cực kỳ tốn tài nguyên và không thời gian thực.

**Webhook (Event-driven)** giải quyết vấn đề này theo cơ chế "Đừng gọi tôi, tôi sẽ gọi bạn" (Hollywood Principle).
- Hệ thống B (Receiver) sẽ cung cấp một URL công khai.
- Hệ thống A (Publisher) khi làm xong việc, sẽ tự động bắn một request (Push) tới URL đó kèm theo dữ liệu sự kiện.

## Thành phần trong ví dụ này
1. `receiver.py`: Đóng vai trò là hệ thống thông báo của chúng ta. Chạy liên tục và đợi sự kiện.
2. `publisher.py`: Đóng vai trò là cổng thanh toán (như Momo, VNPay). Tự động bắn tín hiệu sang Receiver khi có giao dịch xảy ra.

## Chạy thử
**Bước 1: Mở Terminal 1 và bật Receiver**
```bash
python receiver.py
```
*Lúc này Receiver sẽ chạy ở cổng 5004 và im lặng chờ đợi.*

**Bước 2: Mở Terminal 2 và kích hoạt Publisher**
```bash
python publisher.py
```
*Bạn sẽ thấy Publisher bắn tín hiệu, và bên màn hình Terminal 1 (Receiver) ngay lập tức in ra các log xử lý gửi Email, gửi thông báo.*
