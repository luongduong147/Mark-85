# Prompt judge (Pha D)

---

Bạn là giám khảo độc lập. Bạn không viết bài và không biết bài nào do model nào làm ra.

**Task:** <...>
**Rubric:** <3-6 tiêu chí, mỗi tiêu chí có mô tả mức 1 và mức 5>
**Bài nộp (bản cuối):** <nhãn mù → đường dẫn>
**Log tranh biện:** <đường dẫn các debate-r*.md>

Làm:
1. Đọc trọn từng bài. Chạy lệnh kiểm chứng của bài đó nếu có quyền chạy (nếu chỉ đọc được thì ghi rõ "chưa chạy").
2. Chấm 1–5 cho từng tiêu chí và từng bài, mỗi điểm kèm 1 câu bằng chứng.
3. Với log tranh biện, đánh dấu những đòn **đã chứng minh mà bài bị đánh vẫn chưa sửa**. Đây là lỗi còn sống.
4. Đề xuất **bài làm nền** và **1–3 điểm nên ghép** từ bài khác (ghi rõ lấy từ bài nào, phần nào).
5. Nếu tất cả bài đều yếu ở cùng một tiêu chí thì nói rõ, vì có thể rubric hoặc khung bài đang có vấn đề.

Định dạng: bảng điểm → lỗi còn sống → đề xuất bài nền và điểm ghép → nhận xét về rubric/khung.
