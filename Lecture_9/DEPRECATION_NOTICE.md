# Thông báo Ngừng hỗ trợ API Thanh toán v1 (Deprecation Notice)

**Ngày thông báo:** 2026-05-07  
**Phiên bản bị ảnh hưởng:** `/api/v1/*`  
**Ngày dự kiến gỡ bỏ hoàn toàn (EOL):** 2026-12-31

## 1. Lý do nâng cấp
Phiên bản v1 hiện tại không hỗ trợ đầy đủ các tính năng bảo mật mới và thiếu thông tin chi tiết về phương thức thanh toán, gây khó khăn cho việc đối soát dữ liệu. Phiên bản v2 được ra mắt để giải quyết các vấn đề này và tối ưu hóa hiệu năng xử lý.

## 2. Các thay đổi quan trọng (Breaking Changes)
| Tính năng | Phiên bản v1 | Phiên bản v2 (Mới) |
| :--- | :--- | :--- |
| **Endpoint** | `/api/v1/payments` | `/api/v2/payments` |
| **Bắt buộc** | `amount` | `amount`, `payment_method`, `user_id` |
| **Cấu trúc trả về** | Phẳng (Flat JSON) | Phân lớp (Data & Meta wrapping) |
| **Định dạng thời gian** | Không có | Epoch timestamp |

## 3. Hướng dẫn Migration cho Developers
Để chuyển đổi sang v2, các nhà phát triển cần thực hiện các bước sau:
1. Cập nhật URL endpoint từ `/v1/` sang `/v2/`.
2. Bổ sung trường `user_id` (ID của người dùng thực hiện thanh toán).
3. Bổ sung trường `payment_method` (Ví dụ: `CREDIT_CARD`, `E_WALLET`, `BANK_TRANSFER`).
4. Cập nhật logic xử lý kết quả trả về để đọc dữ liệu từ object `data`.

## 4. Kế hoạch hỗ trợ
- **Hiện tại - 31/10/2026:** Duy trì song song v1 và v2. Các phản hồi từ v1 sẽ có thêm Header `Warning` và `Deprecation`.
- **01/11/2026 - 30/12/2026:** Giai đoạn "Sunset". Tỉ lệ lỗi giả lập trên v1 sẽ tăng dần để nhắc nhở migrate.
- **31/12/2026:** Đóng hoàn toàn API v1.
