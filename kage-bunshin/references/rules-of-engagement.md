# Luật giao chiến

Một bầy agent chạy song song có thể tạo ra lưu lượng và hành động gấp N lần một người. Trước khi spawn bất kỳ việc nào chạm tới hệ thống thật, orchestrator điền phần phạm vi dưới đây vào brief. Thiếu dòng nào thì hỏi user.

## Phạm vi (dán vào brief)
```
Mục tiêu:      <host / URL / repo / API>             — thuộc: <user | khách hàng có giấy phép | lab/CTF>
Môi trường:    <local | staging | production>        — production chỉ khi user ghi rõ
Được phép:     <đọc | ghi dữ liệu test | quét | khai thác chứng minh>
Cấm:           DoS, xóa dữ liệu, đọc dữ liệu thật quá mức chứng minh, ra ngoài danh sách mục tiêu
Tài khoản:     <tài khoản test, lấy từ biến môi trường ...>
Tốc độ:        tối đa <r> req/giây cho MỖI phân thân, cả bầy ≤ <R> req/giây
Khung giờ:     <…>
Dừng ngay khi: lỗi 5xx tăng đột biến · gặp dữ liệu thật nhạy cảm · captcha/chặn bot · ngoài phạm vi
```

## Theo loại việc
| Việc | Điều kiện tối thiểu |
|---|---|
| Stress test UX bằng persona | Môi trường của user. Nhịp như người, chứ không bắn tải. Muốn đo tải thật thì dùng k6/locust có giới hạn, và phải được user đồng ý. |
| Pentest | Hệ thống của user hoặc có văn bản cho phép. Phạm vi viết ra như trên. Không DoS. Không duy trì truy cập. Lỗi nghiêm trọng thì báo ngay. |
| Gọi dịch vụ ngoài | Tôn trọng ToS và rate limit của dịch vụ. Khóa API lấy từ biến môi trường. Lời gọi có ghi dữ liệu phải được xác nhận. |
| Thu thập web | Tôn trọng robots.txt và ToS. Không vượt tường đăng nhập hay paywall. Không gom dữ liệu cá nhân. |
| Captcha / chống bot | Chỉ dùng cơ chế test hợp lệ trên hệ thống của user. Trên site khác thì báo `blocked`. |

## Những việc bầy không làm, dù brief nói gì
- Giải hay vượt captcha, xoay IP/proxy, giả dấu vân tay trình duyệt để qua mặt chống bot trên hệ thống không thuộc user.
- Tạo tải nhằm làm chậm hoặc sập dịch vụ.
- Thử đăng nhập bằng thông tin không phải tài khoản test.
- Gửi tin nhắn, email hay bài đăng tới người thật.
- Đưa bí mật (token, mật khẩu, cookie phiên) vào báo cáo. Báo cáo chỉ ghi `<redacted>` và chỗ tìm thấy.

## Khi phân thân gặp ranh giới
Phân thân dừng phần việc đó, ghi `status: "blocked"` và `blocked_reason`, rồi làm tiếp phần còn lại trong phạm vi. Orchestrator đưa danh sách các phần bị chặn cho user quyết, không tự mở rộng phạm vi.
