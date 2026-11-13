# Tầng nguyên nhân & hướng tổng quát hóa

Mỗi tầng: dấu hiệu nhận biết → hướng giải pháp tổng quát → bẫy cần tránh.

## L1 — Instance bug
- **Dấu hiệu:** lỗi đơn lẻ, quét pattern không thấy chỗ nào khác giống.
- **Hướng:** case fix là đúng. Thêm test. Dừng ở đây — đừng tổng quát hóa thứ chỉ có 1 instance.
- **Bẫy:** dựng framework cho một lỗi.

## L2 — Code lặp / drift
- **Dấu hiệu:** cùng logic ở ≥2 chỗ và các bản đã lệch nhau (một chỗ được sửa, chỗ kia không); fix trước chỉ sửa 1 bản.
- **Hướng:** gom về một nguồn sự thật (hàm/module/bảng cấu hình chung), các caller gọi vào; xóa bản cũ (migrate caller rồi xóa API cũ).
- **Bẫy:** gộp hai thứ "trông giống nhau" nhưng khác nghiệp vụ → abstraction sai. Kiểm tra: chúng có thay đổi CÙNG LÝ DO không?

## L3 — Rule / keyword cứng (đặc biệt LLM routing)
- **Dấu hiệu:** if-else / regex / danh sách keyword quyết định intent/route; mỗi lỗi mới = thêm 1 keyword; câu không dấu, viết tắt, lẫn Anh–Việt, paraphrase làm route sai; prompt router liệt kê ví dụ thay cho định nghĩa.
- **Hướng (chọn theo chi phí tăng dần):**
  1. Chuẩn hóa input trước khi match (bỏ dấu, lowercase, alias/synonym map) — rẻ, bao được nhiều.
  2. Thay keyword bằng **định nghĩa intent + mô tả ranh giới** trong prompt router; few-shot gồm cả ví dụ **phản** (case dễ nhầm).
  3. **Semantic routing**: embedding + ngưỡng, mỗi route có tập câu mẫu; ngoài ngưỡng → fallback LLM classifier.
  4. **Hybrid có cấu trúc**: rule chỉ cho tín hiệu chắc chắn (lệnh, ID, slash command), còn lại để model; output router là JSON có `confidence`, dưới ngưỡng thì hỏi lại hoặc route mặc định an toàn.
  5. Vòng phản hồi: log mọi quyết định route + confidence để có bộ dữ liệu đánh giá.
- **Kiểm chứng bắt buộc:** bộ held-out paraphrase ≥10 câu/intent bị lỗi, đo accuracy trước/sau, và kiểm tra các intent khác KHÔNG tụt.
- **Bẫy:** thêm keyword thứ N+1 (đây chính là case fix); dùng LLM cho thứ rule xử lý chắc chắn được (tốn tiền + latency).

## L4 — Thiếu abstraction / contract
- **Dấu hiệu:** caller phải "biết" chi tiết nội bộ để dùng đúng; lỗi do caller quên một bước (quên validate, quên đóng resource, quên escape); kiểu dữ liệu cho phép state vô nghĩa.
- **Hướng:** làm state sai **không biểu diễn được** (type/enum/schema), đẩy bước bắt buộc vào trong API (constructor validate, context manager, builder), parse ở biên một lần rồi dùng dữ liệu đã parse.
- **Bẫy:** thêm validator rải rác ở mọi caller.

## L5 — Kiến trúc / ranh giới
- **Dấu hiệu:** sửa một chỗ lan ra nhiều module; hai thành phần cùng ghi một state; thứ tự khởi tạo/race; một module làm quá nhiều việc.
- **Hướng:** tách quyền sở hữu state (một writer), đưa side-effect ra biên, đổi luồng đồng bộ ↔ bất đồng bộ, hàng đợi/idempotency key.
- **Bẫy:** rewrite cả hệ thống. Luôn có phương án tăng dần + điểm rollback. Cần user xác nhận.

## L6 — Thiếu quan sát / quy trình
- **Dấu hiệu:** lỗi tìm ra muộn vì không có log/metric; cùng loại lỗi lọt qua review nhiều lần.
- **Hướng:** log có cấu trúc + correlation id ở biên, assert/invariant check, lint rule/CI gate, test contract. Biến bài học thành **cơ chế** (rule, script, hook) chứ không phải lời nhắc.
- **Bẫy:** log mọi thứ (nhiễu, lộ dữ liệu nhạy cảm).

## Chấm "độ tổng quát" của một giải pháp
| Tiêu chí | Câu hỏi |
|---|---|
| Coverage | Bao được bao nhiêu % case anh em + held-out? |
| Locality | Thay đổi gói gọn ở bao nhiêu file/module? |
| Cost | Người-giờ (khoảng thấp–cao), chi phí runtime (latency, token) |
| Reversibility | Rollback bằng 1 revert được không? |
| New risk | Tạo ra failure mode mới nào? |
| Simplicity | Code/khái niệm sau sửa ít hơn hay nhiều hơn trước? |
