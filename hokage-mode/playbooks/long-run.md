# Việc dài hơi / không có playbook khớp

**Bạn sở hữu điều kiện kết thúc.** Định nghĩa xong là gì, rồi chạy tới đó.

1. **Định khung.** Ghi vào sổ khi `start`:
   - điều kiện xong, ở dạng phép thử chạy ra đúng/sai;
   - phạm vi, gồm số đơn vị ước lượng;
   - các chướng ngại đã biết.
2. **Thiết kế quy trình.**
   - Chia thành đơn vị nhỏ, tự hạ cánh được.
   - Làm phần có ẩn số rủi ro nhất trước.
   - Dựng khung kiểm chứng trước khi làm việc, ghi baseline.
   - Ghi danh sách pha vào sổ: `trail.py note plan "<pha 1 → pha 2 → …>"`.
3. **Vòng lặp**, mỗi đơn vị là một thí nghiệm:
   - nêu giả thuyết;
   - làm thay đổi nhỏ nhất;
   - kiểm theo điều kiện xong;
   - có tiến thì commit, không tiến thì revert;
   - ghi `checkpoint`.
4. **Phát hiện giữa đường** mà phục vụ mục tiêu thì tự xử lý. Ngoài mục tiêu thì ghi lại làm việc tiếp theo.
5. **Chờ thứ gì lâu** (CI, job, deploy của người khác) thì dùng `/loop` hoặc `ScheduleWakeup` với nhịp hợp với tốc độ thay đổi của thứ đang chờ. Không poll dày.
6. **Gặp vùng không tiến thêm** thì đổi cách, không dừng. Ngõ cụt thật thì báo rõ đã thử những gì. Không nới điều kiện xong để tuyên bố thắng.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Đơn vị | chia rộng, chạy song song theo đợt | từng đợt, có verifier | tuần tự, checkpoint mỗi đơn vị |
