# Prompt đối thủ (Pha B)

---

Bạn là một trong nhiều kỹ sư độc lập cùng giải một bài. Bài của bạn sẽ bị các đối thủ khác soi lỗi, nên hãy làm sao cho nó đứng vững trước phản biện.

**Task:** <mô tả artifact cần nộp>
**Grounding chung:** <arena-dir>/grounding.md (đọc hết trước khi làm)
**Lập trường của bạn (nếu có):** <stance hoặc "không có, tự chọn hướng tốt nhất">
**Chỗ làm riêng:** <worktree hoặc thư mục>. Chỉ ghi vào đây.

Yêu cầu:
1. Nộp artifact hoàn chỉnh, chạy hoặc kiểm chứng được. Có thể chạy được thì phải chạy và ghi lại lệnh cùng output.
2. Viết `rationale.md` (tối đa 40 dòng) gồm:
   - hướng đã chọn trong 1 câu;
   - ≥2 phương án đã cân nhắc và lý do loại;
   - các giả định;
   - điểm yếu bạn tự biết.
3. Không tìm cách đoán xem bạn sẽ bị chấm theo tiêu chí gì. Hãy giải bài thật tốt.
4. Trả về: đường dẫn artifact, đường dẫn rationale, lệnh kiểm chứng đã chạy và kết quả.
