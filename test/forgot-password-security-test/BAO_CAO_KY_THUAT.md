# BÁO CÁO KỸ THUẬT: ĐÁNH GIÁ CHỨC NĂNG QUÊN MẬT KHẨU

## 1. THÔNG TIN CHUNG
- **Hệ thống thử nghiệm:** VinFast Auto Shop
- **Endpoint:** `POST /on/demandware.store/Sites-app_vinfast_vn-Site/vi_VN/Login-Auth0ForgotPassword`
- **Phương thức gửi:** `application/x-www-form-urlencoded`
- **Tổng số mẫu kiểm thử:** 11 yêu cầu (1 tài khoản tồn tại + 10 tài khoản ngẫu nhiên)

---

## 2. KẾT QUẢ GHI NHẬN TỪ THỰC TẾ

### 2.1. Phản hồi theo trạng thái tài khoản
Máy chủ phản hồi khác biệt rõ ràng giữa hai nhóm tài khoản:

1. **Tài khoản đã tồn tại trong hệ thống:**
   - Trả về mã trạng thái: `200 OK`
   - Dữ liệu phản hồi:
     ```json
     {
       "action": "Login-Auth0ForgotPassword",
       "success": true
     }
     ```

2. **Tài khoản không tồn tại trong hệ thống:**
   - Trả về mã trạng thái: `200 OK`
   - Dữ liệu phản hồi:
     ```json
     {
       "action": "Login-Auth0ForgotPassword",
       "success": false,
       "message": "Email chưa đăng ký tài khoản"
     }
     ```

### 2.2. Kiểm soát tần suất gửi yêu cầu
- Toàn bộ 11/11 yêu cầu gửi liên tiếp (khoảng cách 1.5 giây) đều được máy chủ phản hồi với mã `200 OK`.
- Chưa ghi nhận cơ chế giới hạn số lần gửi yêu cầu trong khoảng thời gian ngắn trên endpoint này.

### 2.3. Kiểm tra tính hợp lệ của CAPTCHA
- Khi gửi yêu cầu với tham số `grecaptcha_token` để trống, máy chủ vẫn tiếp nhận và xử lý thay vì yêu cầu bắt buộc phải có token hợp lệ.

---

## 3. CÁC ĐỀ XUẤT CẢI THIỆN CHO ĐỘI NGŨ PHÁT TRIỂN

### 1. Đồng nhất thông điệp phản hồi (Generic Response)
- Trả về cùng một cấu trúc thông báo cho mọi trường hợp (dù tài khoản có tồn tại hay không):
  ```json
  {
    "action": "Login-Auth0ForgotPassword",
    "success": true,
    "message": "Nếu địa chỉ email tồn tại trong hệ thống, hướng dẫn đặt lại mật khẩu sẽ được gửi đến hộp thư của bạn."
  }
  ```
- **Mục đích:** Bảo vệ quyền riêng tư của người dùng, tránh để lộ danh sách tài khoản đã đăng ký.

### 2. Áp dụng giới hạn tần suất gửi yêu cầu (Rate Limiting)
- Thiết lập giới hạn tối đa số lần gửi yêu cầu khôi phục mật khẩu theo từng địa chỉ IP và theo từng tài khoản email đích (ví dụ: tối đa 3-5 lần trong vòng 15 phút).
- **Mục đích:** Giảm tải cho máy chủ gửi thư và tránh gửi thư dồn dập vào hộp thư người dùng.

### 3. Xác thực bắt buộc CAPTCHA ở phía máy chủ
- Kích hoạt kiểm tra tính hợp lệ của token reCAPTCHA từ phía máy chủ trước khi xử lý logic gửi email đặt lại mật khẩu.
- **Mục đích:** Đảm bảo các yêu cầu được thực hiện từ giao diện người dùng thực tế.

### 4. Đánh dấu hết hạn Token sau khi sử dụng (Single-Use Token)
- Vô hiệu hóa token của phiên biểu mẫu ngay sau khi yêu cầu được xử lý xong, yêu cầu người dùng tải lại biểu mẫu để nhận token mới nếu muốn gửi yêu cầu tiếp theo.
