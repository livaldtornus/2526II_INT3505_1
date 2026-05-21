# API Design Patterns & Architecture Choices

Tài liệu này tổng hợp các mẫu thiết kế API phổ biến và cách lựa chọn kiến trúc phù hợp.

## 1. Kiến trúc API: Khi nào dùng REST, gRPC, GraphQL?

| Tiêu chí | REST | GraphQL | gRPC |
| :--- | :--- | :--- | :--- |
| **Bản chất** | Dựa trên Resource (Tài nguyên) | Dựa trên Query (Truy vấn) | Dựa trên RPC (Gọi hàm từ xa) |
| **Giao thức** | HTTP/1.1 (phổ biến) | HTTP/1.1 hoặc HTTP/2 | HTTP/2 (Bắt buộc) |
| **Định dạng dữ liệu** | JSON, XML, HTML | JSON | Protocol Buffers (Binary) |
| **Ưu điểm** | Dễ hiểu, chuẩn hóa, dễ cache | Lấy đúng dữ liệu cần, tránh Over/Under-fetching | Cực kỳ nhanh, type-safe, streaming 2 chiều |
| **Khi nào nên dùng?** | API công cộng (Public API), các ứng dụng CRUD tiêu chuẩn, tích hợp hệ thống ngoài. | Các ứng dụng Frontend (React, Mobile) phức tạp cần lấy dữ liệu từ nhiều nguồn khác nhau. | Giao tiếp giữa các Microservices nội bộ (Backend-to-Backend), hệ thống yêu cầu hiệu năng cao. |

## 2. Các API Design Patterns (Mẫu thiết kế API)

### 2.1. CRUD (Create, Read, Update, Delete)
- **Mô tả**: Mẫu thiết kế cơ bản nhất, ánh xạ trực tiếp các thao tác HTTP (POST, GET, PUT/PATCH, DELETE) vào các thao tác database.
- **Khi nào dùng**: Quản lý tài nguyên đơn giản (ví dụ: Quản lý người dùng, bài viết, sản phẩm).

### 2.2. Query Pattern (Truy vấn nâng cao)
- **Mô tả**: Cho phép client tìm kiếm, lọc (filter), sắp xếp (sort), và phân trang (paginate) dữ liệu thông qua query parameters.
- **Khi nào dùng**: Khi có danh sách dữ liệu lớn, cần cung cấp công cụ linh hoạt cho người dùng tìm kiếm.

### 2.3. HATEOAS (Hypermedia As The Engine Of Application State)
- **Mô tả**: API trả về không chỉ dữ liệu mà còn các "links" (liên kết) chỉ báo các hành động tiếp theo có thể thực hiện.
- **Khi nào dùng**: Hệ thống có luồng trạng thái phức tạp (State machine), muốn client tự động thích ứng với thay đổi API mà không cần hard-code URL.

### 2.4. Webhook / Event-driven Pattern
- **Mô tả**: Thay vì client liên tục "hỏi" (polling) server xem có dữ liệu mới không, server sẽ chủ động "gọi" (push) một HTTP POST đến client khi có sự kiện xảy ra.
- **Khi nào dùng**: Các tác vụ bất đồng bộ tốn thời gian (thanh toán xong, render video xong), tích hợp với hệ thống bên thứ ba (Stripe, GitHub, Slack).

---

*Các ví dụ code cụ thể được cung cấp trong các thư mục tương ứng.*
