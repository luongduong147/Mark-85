---
name: arena
description: "Spawn N đối thủ (subagent) cùng giải một vấn đề độc lập, cho họ đọc bài của nhau để phản biện, bảo vệ và sửa bài qua các vòng tranh biện, rồi một judge mù nhãn chấm theo rubric. Cuối cùng chọn một bài làm nền và ghép những phần mạnh nhất của các bài thua vào. Dùng cho /arena <n> <task>, 'arena this', 'cho n con agent đấu nhau', 'tranh biện tìm giải pháp tốt nhất', hoặc khi một lần làm duy nhất cho một việc không tầm thường dễ chốt sai hướng."
argument-hint: "<n> <task> [--rounds 1|2] [--stances]"
disable-model-invocation: true
---

# Arena

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh). Số đầu tiên là `n` (mặc định 3, tối đa 6), phần còn lại là task. `--rounds` là số vòng tranh biện (mặc định 1, tối đa 2). `--stances` gán cho mỗi đối thủ một lập trường khác nhau.

Phỏng theo skill `arena` trong pstack của Lauren Tan (poteto), giấy phép MIT, nguồn `github.com/cursor/plugins/pstack/skills/arena`. Bản này **thêm vòng tranh biện**: các đối thủ đọc bài của nhau, chứng minh lỗi của nhau, rồi tự sửa bài mình trước khi bị chấm.

Mở todo list với 7 pha: Frame, Fan out, Debate, Cross-judge, Pick, Graft, Verify.

## Pha A: Frame (prompt là hợp đồng)
1. **Artifact**: nói rõ mỗi đối thủ phải nộp gì (thiết kế, code, prompt, kế hoạch, bài viết…) và nộp ở đâu.
2. **Rubric**: 3–6 tiêu chí chấm được cho riêng task này, ví dụ "pass 40 case held-out", "≤ 1 dependency mới", "đọc hiểu trong 5 phút". Rubric dành cho người chấm, **đối thủ không được thấy**, để không ai tối ưu theo đề thi.
3. **Grounding chung**: file, đoạn trích, ràng buộc mà mọi đối thủ đều cần. Ghi vào `<arena-dir>/grounding.md`. Không ai nhận thêm thông tin riêng.
4. **Lập trường** (khi có `--stances` hoặc khi task có nhiều hướng thiết kế): gán mỗi đối thủ một hướng khác nhau. Danh sách gợi ý trong `references/stances.md`. Không có `--stances` thì mọi đối thủ nhận cùng một prompt; sự khác biệt đến tự nhiên.
5. **Model**: chia đều các model có sẵn cho các ghế, ví dụ xen kẽ `opus` và `sonnet`. Task chủ yếu là sinh nội dung chứ không cần phán đoán sâu thì dùng cùng một model cho N ghế cũng được. Nếu máy có CLI của model khác (codex, gemini, opencode…) và user muốn, một ghế có thể chạy qua CLI đó bằng Bash. Ghi rõ ghế nào chạy model nào.
6. **Chỗ làm riêng**: mỗi đối thủ dùng git worktree riêng (`isolation: "worktree"`) nếu nộp code, hoặc thư mục `<arena-dir>/candidate-<k>/` nếu nộp tài liệu. `<arena-dir>` mặc định là `.arena/<slug>/` (thêm vào `.gitignore`) hoặc thư mục scratchpad.

## Pha B: Fan out
Spawn cả N đối thủ **trong một message**, chạy nền, prompt theo `references/candidate-prompt.md`. Mỗi đối thủ nộp artifact kèm `rationale.md`, trong đó có các phương án đã cân nhắc, cái đã loại và lý do.

Đối thủ nào không nộp được thì chơi tiếp với N−1 và ghi chú lại. Còn dưới 2 đối thủ thì dừng tranh biện và báo user.

## Pha C: Debate (tranh biện / phản biện)
Mỗi vòng:
1. Gửi cho mỗi đối thủ đường dẫn bài của **tất cả** đối thủ khác. Nếu còn agent thì tiếp tục agent đó qua SendMessage để giữ context; không thì spawn mới kèm bài cũ của chính nó. Prompt theo `references/debate-prompt.md`.
2. Mỗi đối thủ phải:
   - **Tấn công**: chỉ ra lỗi mạnh nhất trong bài mỗi đối thủ khác. Lỗi phải được **chứng minh** bằng lần chạy, test, ví dụ phản chứng hoặc trích dẫn cụ thể, không chê theo cảm tính.
   - **Phòng thủ**: trả lời từng đòn đánh vào bài mình bằng một trong ba cách: chấp nhận (sửa), bác bỏ (kèm bằng chứng), hoặc ngoài phạm vi.
   - **Sửa bài**: nộp bản `v<round+1>` và `debate-r<k>.md` ghi rõ đã nhượng bộ điểm nào, giữ điểm nào, vì sao.
3. **Chống a dua**: nhượng bộ phải có lý do. Đối thủ bỏ hẳn hướng của mình để chép bài người khác thì phải giải thích bằng bằng chứng. Nếu mọi bài hội tụ về một hình dạng sau vòng 1 thì đó là tín hiệu đồng thuận mạnh, ghi lại và dừng tranh biện sớm.

Bạn (orchestrator) không đứng về phe nào ở pha này. Bạn chỉ chuyển bài và gom kết quả.

## Pha D: Cross-judge
Sau khi vòng cuối xong, spawn **1 judge** chỉ đọc, context sạch, dùng model mạnh nhất có sẵn và nếu được thì khác model của bạn. Bài nộp được gắn nhãn mù (A, B, C…, đã xáo thứ tự). Judge nhận rubric, bản cuối của mỗi bài và toàn bộ log tranh biện, rồi chấm từng tiêu chí và đề xuất bài làm nền. Prompt theo `references/judge-prompt.md`.

Judge chạy song song trong lúc bạn tự đọc ở Pha E.

## Pha E: Pick base
Đọc trọn từng bài cuối. Chấm theo rubric **từng tiêu chí**, không chấm theo cảm giác chung, rồi so với judge:
- Hai bên chọn cùng bài: chốt.
- Hai bên lệch nhau: hoặc một bên thiên lệch, hoặc rubric mơ hồ. Đọc lập luận của cả hai trước khi quyết.

Chọn bài mà người bảo trì sau này dễ mở rộng nhất mà không phá vỡ bất biến. Hai bài ngang nhau thì chọn bài có ranh giới gọn hơn hoặc API nhỏ hơn.

## Pha F: Graft
Đi lại từng bài thua một lượt để tìm thứ đáng mang sang, thường chỉ 1–2 điểm mỗi bài. Đặc biệt chú ý những đòn tấn công đã được chứng minh mà bài nền chưa xử lý. Tự tay ghép vào cho thống nhất dưới một mô hình tư duy, không dán máy móc.

Nếu các bài **phân kỳ dữ dội** thì Pha A đã chưa đủ rõ. Khi đó viết lại khung và chạy lại, đừng lấy trung bình của sự phân kỳ.

## Pha G: Verify
Kiểm chứng artifact tổng hợp như mọi đầu ra khác: chạy test, chạy rubric trên artifact thật. Nếu phát hiện lỗi mà arena bỏ sót:
- lỗi do khung sai thì quay lại Pha A;
- lỗi đã có đối thủ chỉ ra mà bạn quên ghép thì quay lại Pha F.

## Đầu ra
Một artifact tổng hợp, kèm `SYNTHESIS.md` theo `templates/synthesis.md`, gồm:
- bài nền và lý do chọn;
- phán quyết của judge;
- bảng tranh biện (đòn nào trúng, đòn nào bị bác);
- từng điểm ghép và nguồn của nó;
- những gì đã loại và vì sao;
- hội tụ hay phân kỳ, đối thủ bỏ cuộc;
- kết quả kiểm chứng.

Trong chat chỉ trả: bài thắng, 3 đòn phản biện đáng giá nhất, những gì đã ghép, và kết quả verify.

## Khi không nên dùng
- Việc cơ học đã rõ hình dạng (đổi tên, migrate theo khuôn). Arena ở đây là phí tiền.
- Câu hỏi có đáp án tra được.
- Thiết kế đã chốt mà chạy arena lần hai.
