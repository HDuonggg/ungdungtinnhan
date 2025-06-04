# Secure Messaging App

Ứng dụng chat bảo mật đơn giản sử dụng Flask, hỗ trợ nhiều phòng chat với giao diện đẹp, có chế độ sáng/tối và hiển thị người dùng online.

## Tính năng

- Tạo và tham gia phòng chat bằng mã phòng/cypher key.
- Gửi và nhận tin nhắn theo thời gian thực (tự động làm mới).
- Hiển thị danh sách người dùng đang online trong phòng.
- Giao diện đẹp, hỗ trợ chuyển đổi giữa chế độ sáng và tối.
- Thông báo khi người dùng vào/rời phòng.

## Cài đặt

1. **Yêu cầu:** Python 3.x, pip
2. **Cài đặt thư viện:**
   ```sh
   pip install flask
   ```
3. **Chạy ứng dụng:**
   ```sh
   python app.py
   ```
4. **Truy cập:** Mở trình duyệt và vào địa chỉ [http://localhost:5000](http://localhost:5000)

## Cấu trúc thư mục

```
app.py
app/
    templates/
        index.html
```

> **Lưu ý:** Ứng dụng sử dụng HTML được nhúng trực tiếp trong `app.py`. Bạn có thể thay đổi giao diện bằng cách chỉnh sửa biến `HTML` trong file này.

## Sử dụng

- Nhập tên và mã phòng để vào phòng chat.
- Gửi tin nhắn, xem ai đang online.
- Nhấn "Rời phòng" để thoát.
- Nhấn nút 🌙/☀️ để chuyển đổi giao diện sáng/tối.

## Bảo mật & Giới hạn

- Ứng dụng chỉ lưu trữ dữ liệu trên RAM, không có cơ sở dữ liệu.
- Không mã hóa nội dung tin nhắn.
- Không dùng cho mục đích sản xuất hoặc trao đổi thông tin nhạy cảm.

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Hãy tạo pull request hoặc issue nếu bạn muốn cải thiện ứng dụng.

---

**Tác giả:** [Dương Huy Hoàng - CNTT 17-07]  
**Giấy phép:** MIT
![image](https://github.com/user-attachments/assets/2fb070f7-1d19-4564-8951-1157954ae26e)

![image](https://github.com/user-attachments/assets/4e4d1b11-d4bd-4a8b-a755-49606ca3aeb9)
