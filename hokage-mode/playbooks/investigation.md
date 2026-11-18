# Điều tra (chỉ đọc)

**Bạn sở hữu câu trả lời.** Không sửa code. Kết quả là lời giải thích có dẫn chứng, hoặc một khuyến nghị.

1. Lần theo phần code liên quan.
   - Câu hỏi rộng thì chia vùng cho các agent `Explore`/`haiku` đọc song song, mỗi con trả về `file:line` cùng một câu kết luận.
   - Câu hỏi "vì sao code lại thế này" thì xem `git log -L` / `git blame` của đoạn đó.
2. Viết câu trả lời theo các phần:
   - Tổng quan
   - Khái niệm chính
   - Cách chạy
   - Ở đâu (`file:line`)
   - Bẫy
   Câu hỏi là một lựa chọn thì trả lời bằng khuyến nghị kèm bảng đánh đổi.
3. Tiền đề của câu hỏi sai thì nói thẳng.
4. Hóa ra cần sửa code thì dừng ở đây và định tuyến lại sang `bug-fix` hoặc `feature`.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Đọc | bung nhiều agent một lượt | 2–3 agent, tự mở lại các `file:line` then chốt | tự grep, đọc theo đoạn |
| Trả lời | 5 dòng + `file:line` | đủ các phần, nhãn VERIFIED/INFERRED | các phần, mỗi phần ≤ 3 dòng |
