---
name: generalize-fixed-it
description: "Sửa một lỗi/vấn đề theo hướng TỔNG QUÁT HÓA thay vì vá từng case: truy gốc rễ qua log và trace, phân loại tầng nguyên nhân (kiến trúc, code lặp, rule/keyword cứng trong LLM routing…), đề xuất nhiều giải pháp tổng quát, cho subagent mô phỏng từng giải pháp rồi gọi model tổng chấm điểm. Dùng khi gõ /generalize-fixed-it <problem>, hoặc nói 'sửa tận gốc', 'đừng vá case', 'fix tổng quát', 'lỗi này cứ lặp lại', 'generalize the fix'."
argument-hint: "<problem: mô tả lỗi / link log / file:line>"
disable-model-invocation: true
---

# Generalize-fixed-it

Vấn đề: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh)

Mục tiêu: sửa **lớp lỗi**, không phải **một lần lỗi**. Đầu ra là một bản sửa đã được mô phỏng, chấm điểm, và có bằng chứng rằng nó xử lý được cả những case anh em chưa từng thấy, chứ không chỉ case trước mắt.

Mở todo list với đúng 8 bước dưới đây trước khi làm.

## Nguyên tắc
- **Triệu chứng ≠ gốc rễ.** Triệu chứng là nơi trạng thái sai lộ ra; gốc rễ là chỗ ĐẦU TIÊN hệ thống quyết định sai. Hỏi "tại sao" đến khi câu trả lời là *một quyết định sai trong code/thiết kế*, không phải hệ quả của bước trước.
- **Bằng chứng trước, giả thuyết sau.** Đọc log/trace/state thật. Không đoán. Mỗi nhận định ghi rõ **Verified** (đã chạy/đã đọc) hay **Inferred**.
- **Guard chỉ là fix khi state đó hợp lệ.** Nếu state không được phép tồn tại, thêm `if`/retry/try-catch/clamp ở chỗ vỡ là che lỗi — phải tìm ai sinh ra state đó.
- **Hai fix cùng tiền đề đã fail → nghi tiền đề**, đừng viết fix thứ ba. Viết tiền đề ra một câu, kiểm chứng trực tiếp.
- **Case fix luôn là baseline**, không bị cấm — nhưng phải được so sánh công khai với các phương án tổng quát. Đôi khi case fix đúng là lựa chọn rẻ nhất; khi đó nói rõ vì sao.
- **Không over-engineer.** Tổng quát hóa vừa đủ để bao lớp lỗi đã chứng minh tồn tại, không phải mọi lớp lỗi tưởng tượng.

## Quy trình

### 1. Tái hiện & gom bằng chứng
- Tái hiện lỗi (lệnh, input, request). Không tái hiện được → ghi rõ và hạ độ tin cậy.
- Gom: log, stack trace, trace id, input/output thật, `git log -L`/`git blame` chỗ nghi vấn, các fix trước đó cho cùng triệu chứng (`git log --grep`).
- **Chưa có gì để quan sát** (lỗi lúc có lúc không, không log) → chạy skill **chase-it** trước để đặt probe, rồi quay lại.

### 2. Truy gốc rễ
- Chuỗi "5 why" từ triệu chứng ngược về quyết định sai. Ghi lại từng bước kèm `file:line`.
- Kiểm tra: state gây lỗi có hợp lệ không? Lỗi có chỉ xuất hiện sau restart (nghi state lưu trữ: cache, config, file lock)?
- Nếu đã có ≥2 fix thất bại: viết tiền đề chung của chúng, kiểm chứng tiền đề.

### 3. Quét pattern (cùng lỗi, chỗ khác)
Tìm MỌI nơi có cùng dạng lỗi: grep theo cấu trúc, tìm code copy-paste, tìm rule/keyword tương tự, các route/handler cùng khuôn. Ghi số lượng: "lỗi này có 1 instance" và "lỗi này có 7 instance" dẫn tới hai quyết định khác nhau.

### 4. Phân loại tầng nguyên nhân
Xếp gốc rễ vào một (hoặc vài) tầng trong `references/root-cause-levels.md`: L1 instance · L2 code lặp/drift · L3 rule/keyword cứng (LLM routing, regex, if-else theo từ khóa) · L4 thiếu abstraction/contract · L5 kiến trúc/ranh giới · L6 thiếu quan sát/quy trình. Đọc phần tương ứng để lấy gợi ý giải pháp.

### 5. Đề xuất ≥3 giải pháp
Luôn gồm: **(A) case fix** (baseline) + **≥2 giải pháp tổng quát ở tầng khác nhau**. Mỗi giải pháp ghi: tầng, ý tưởng, những case nó bao được, blast radius, chi phí (người-giờ dạng khoảng), có đảo ngược được không, rủi ro mới nó tạo ra.

### 6. Mô phỏng bằng subagent
1. Dựng **bộ case kiểm thử** trước (đây là hợp đồng, viết TRƯỚC khi ai code):
   - case gốc;
   - các instance anh em tìm được ở bước 3;
   - **case held-out** chưa ai thấy: biến thể, paraphrase (bắt buộc với L3/LLM routing — sinh ≥10 câu diễn đạt khác, có dấu/không dấu, viết tắt, lẫn tiếng Anh), biên, input xấu;
   - case **không được** đổi hành vi (regression guard).
2. Spawn mỗi giải pháp một subagent **trong cùng một message** (chạy song song), mỗi agent có chỗ làm riêng (git worktree / `isolation: "worktree"`). Prompt theo `references/simulator-prompt.md`. Agent áp giải pháp, chạy bộ case, trả về bảng pass/fail + diff + chi phí thực tế.
3. Agent không chạy được thật (thiếu môi trường, cần LLM thật) → mô phỏng bằng lập luận trên code thật, và đánh dấu **SIMULATED (không chạy)**.

### 7. Model tổng chấm điểm
Spawn **1 judge subagent** với model mạnh nhất có sẵn (mặc định `opus`), context sạch, chỉ đọc. Đưa: mô tả vấn đề, chuỗi gốc rễ, bộ case, kết quả từng subagent (theo nhãn A/B/C, không nói ai là case fix). Prompt theo `references/judge-prompt.md`. Judge chấm theo rubric và đề xuất 1 phương án + điều kiện. Bạn tự đọc kết quả song song; nếu bạn và judge bất đồng, đọc lại cả hai lập luận trước khi chốt.

### 8. Áp dụng & đóng vòng
- Giải pháp chạm L4/L5 (kiến trúc, contract công khai) hoặc khó đảo ngược → **hỏi user xác nhận** (AskUserQuestion) trước khi áp vào nhánh chính. L1–L3 có test đi kèm → áp luôn.
- Thêm **regression test** từ bộ case ở bước 6 (đặc biệt case held-out).
- Ghi comment theo skill **comment-mapping** (When–Why–How) ở chỗ sửa.
- Nếu phải đào sâu mới tìm ra nguyên nhân: đề xuất **một tín hiệu luôn bật, rẻ** (log/metric/assert) để lần sau nhìn là thấy.
- Viết báo cáo theo `templates/fix-report.md` vào `GENERALIZED_FIX_<slug>.md` (hoặc trả trong chat nếu ngắn).

## Đầu ra (trả lời cuối)
Gốc rễ trong 1–2 câu · tầng · phương án chọn và vì sao · bảng điểm judge · số case pass (gốc / anh em / held-out / regression) · việc còn mở.
