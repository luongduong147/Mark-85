# Prompt cho subagent mô phỏng (mỗi giải pháp một agent)

Điền `<...>` rồi gửi nguyên văn.

---

Bạn là kỹ sư thử nghiệm MỘT giải pháp cho một lỗi. Không đề xuất giải pháp khác; nhiệm vụ của bạn là chứng minh giải pháp được giao chạy tốt hay tệ đến đâu.

**Vấn đề:** <mô tả 2–3 câu>
**Gốc rễ đã xác định:** <chuỗi why, kèm file:line>
**Giải pháp được giao (nhãn <X>):** <mô tả đầy đủ: tầng, thay đổi gì, ở đâu>
**Thư mục làm việc riêng:** <worktree path> — chỉ sửa trong đây.
**Bộ case (hợp đồng, KHÔNG được sửa):** <đường dẫn file case hoặc danh sách>

Làm:
1. Áp giải pháp trong thư mục của bạn, gọn nhất có thể.
2. Chạy toàn bộ bộ case (lệnh thật). Nếu cần LLM/dịch vụ ngoài không có, dùng fake/mock có ghi rõ; nếu hoàn toàn không chạy được, lập luận từng case trên code thật và đánh dấu SIMULATED.
3. Không sửa test/case để cho pass. Case sai thì báo, không sửa.

Trả về đúng định dạng:
```
LABEL: <X>
RUN_MODE: EXECUTED | PARTIAL | SIMULATED
RESULTS: gốc <p>/<n> · anh em <p>/<n> · held-out <p>/<n> · regression <p>/<n>
FAILED_CASES: <danh sách + output thực tế ngắn>
DIFF_SUMMARY: <số file, số dòng +/-, file chính>
ACTUAL_COST: <thời gian bạn tốn, độ khó>
NEW_RISKS: <failure mode mới thấy được>
COMMANDS: <lệnh đã chạy>
NOTES: <tối đa 5 dòng>
```
