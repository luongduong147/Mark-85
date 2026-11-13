# Replay eval: kiểm chứng skill có "giống tôi" không

Một skill sinh ra từ convention rất khó chấm bằng unit test. Thay vào đó, ta **phát lại một tình huống cũ** và so với cái user đã thực sự chấp nhận.

## Chọn tình huống
- Lấy từ transcript: tin nhắn mở đầu của user (đầu vào), các lần user sửa lưng (điểm đau), và trạng thái cuối user chấp nhận (đáp án).
- Ưu tiên tình huống có ≥2 lần sửa lưng, vì đó là nơi skill phải tạo khác biệt.
- Che dữ liệu nhạy cảm trước khi đưa vào prompt.

## Chạy
| Agent | Prompt |
|---|---|
| A (có skill) | Nội dung SKILL.md + "Làm theo skill trên." + tin nhắn mở đầu của user |
| B (baseline) | Chỉ tin nhắn mở đầu của user |

Cả hai chỉ chạy tới bước lập kế hoạch và bản nháp đầu ra, không thực thi hành động có tác dụng phụ (không ghi file thật, không gọi dịch vụ ngoài). Hai agent spawn song song trong một message.

## Judge (context sạch, mù nhãn: X/Y)
Đưa cho judge: đầu vào, các lần sửa lưng gốc (dạng "user đã phải nói: …"), trạng thái cuối được chấp nhận, và output X/Y. Chấm từng mục:
1. **Bước**: X/Y có đi đúng chuỗi bước user đã dẫn dắt không? (0–5)
2. **Tránh sửa lưng**: với mỗi lần user từng sửa lưng, X/Y có tự tránh được không? (đếm)
3. **Đầu ra**: định dạng và tiêu chí xong có khớp với thứ user chấp nhận không? (0–5)
4. **Thừa**: X/Y có làm thêm thứ user không muốn không? (liệt kê)

## Đọc kết quả
- A tránh được ≥ một nửa số lần sửa lưng và điểm Bước ≥4: đạt.
- A ≈ B: skill chỉ nói những điều model vốn đã làm. Cắt bớt và tập trung vào điểm đau.
- A làm thừa: có luật bị viết quá rộng. Thu hẹp lại.
