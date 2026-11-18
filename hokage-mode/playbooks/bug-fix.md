# Sửa lỗi

**Bạn sở hữu nhiệm vụ.** Mỗi dòng code được ship phải truy được về một bằng chứng lúc chạy. Bản vá "có lẽ giúp được" chỉ là giả thuyết, không được ship.

1. **Tái hiện** trên đúng bề mặt lỗi xảy ra: CLI, web, API.
   - Không tái hiện được thì tạo điều kiện kích hoạt, siết điều kiện, hoặc dùng `chase-it` để đặt probe.
   - Ghi lệnh tái hiện vào sổ: `trail.py note check "<lệnh>" --result "đỏ"`.
2. **Chia đôi nguyên nhân.**
   - Liệt kê các giả thuyết.
   - Mỗi vòng chọn phép thử loại được nhiều không gian nhất, chạy, rồi loại.
   - Hai bản sửa dựa trên cùng một tiền đề đều thất bại thì kiểm chính tiền đề (Attack the premise).
3. **Lên phương án sửa** bằng `generalize-fixed-it`: phân tầng gốc rễ, đưa ra ≥ 3 phương án. Sửa vượt ranh giới hàm thì vạch shape trước.
4. **Giao việc sửa** cho agent theo bảng model của chế độ. Phạm vi gồm: file nào, hành vi cần đổi, lệnh tái hiện.
5. **Kiểm trên cùng bề mặt.** Lệnh tái hiện chuyển từ đỏ sang xanh. Kết quả "không rõ" hoặc kiểm sai bề mặt thì không tính là qua.
6. **Commit theo thứ tự**: test tái hiện (đỏ) trước, bản sửa sau, rồi `comment-mapping annotate`.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Bước 2 | 2–3 agent kiểm các giả thuyết song song | từng giả thuyết có dự đoán và phép thử, ghi `hyp` vào sổ | giả thuyết rẻ nhất trước, mỗi lần một cái |
| Bước 3 | đua 2 phương án, lấy cái đầu tiên xanh | đủ 3 phương án, judge khác model | phương án gốc rễ rẻ nhất |
| Trả lời | lỗi gì, gốc ở đâu, đã sửa, đỏ→xanh | thêm bảng giả thuyết đã loại và lý do | gốc, sửa, đỏ→xanh, mỗi thứ một dòng |
