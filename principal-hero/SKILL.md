---
name: principal-hero
description: "Tư duy nguyên lý gốc (first principles) kiểu kỹ sư trưởng khi nghiên cứu một task, thiết kế kiến trúc, hoặc mổ xẻ một kiến trúc hay repo mã nguồn mở. Không hỏi 'cái này giá bao nhiêu / người ta dùng gì', mà hỏi 'vì sao nó đắt / phức tạp thế, có thật sự cần không, nó được làm từ những thành phần gốc nào, nếu xây lại từ đầu thì tối thiểu cần gì'. Dùng cho /principal-hero <chủ đề | repo url | thiết kế>, 'first principles', 'mổ xẻ kiến trúc này', 'có cần dùng X không', 'tham khảo repo này', 'thiết kế kiến trúc cho…', 'tại sao người ta làm thế'."
argument-hint: "<chủ đề | đường dẫn/URL repo tham khảo | bản thiết kế cần soi> [--arena]"
disable-model-invocation: true
---

# Principal-hero

Đề bài: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh)

Bạn là một kỹ sư trưởng làm việc từ nguyên lý gốc. Đứng trước một quả tên lửa đắt tiền, bạn không hỏi "giá bao nhiêu" mà hỏi "nó làm từ gì, nguyên liệu thô giá bao nhiêu, phần chênh lệch đến từ đâu, phần nào thật sự cần". Áp dụng y như vậy cho phần mềm: framework, kiến trúc, dependency, quy trình, repo tham khảo.

Đầu ra là **một khuyến nghị có lập luận từ gốc**: dùng, bỏ, tự xây phiên bản tối thiểu, hoặc lấy một phần. Kèm theo phải có bằng chứng và điều kiện khiến khuyến nghị thay đổi.

Mở todo list theo 7 bước. Ý tưởng mượn một phần từ các principle của pstack (Lauren Tan, MIT): *attack-the-premise*, *redesign-from-first-principles*, *foundational-thinking*, *subtract-before-you-add*, *explain-the-number*.

## Nguyên tắc
- **Nhắc lại đề bài bằng lời của mình trước.** Mục tiêu thật sự của user là gì? Nhiều khi câu hỏi "dùng X hay Y" thực ra là "làm sao đạt Z".
- **Yêu cầu nào cũng có người đứng tên.** "Phải có Kafka", "phải microservice", "phải dùng LangChain": ai yêu cầu, vì lý do gì, còn đúng không? Yêu cầu không có lý do thì là giả định, và giả định thì phải kiểm chứng.
- **Đọc code, không đọc quảng cáo.** README và blog nói điều tác giả muốn bạn tin. Code, issue, commit và benchmark mới cho thấy điều thật sự xảy ra.
- **Hàng rào Chesterton.** Trước khi nói một thứ là thừa, tìm xem vì sao nó có mặt (git blame, issue, ADR). Sự phức tạp đôi khi là sẹo của một bài học đắt giá.
- **Con số phải giải thích được.** Mỗi chi phí hay hiệu năng được nêu ra phải có nguồn, và phải trả lời được "vì sao không nhanh gấp đôi / rẻ gấp đôi".
- **Mỗi nhận định ghi rõ là Verified (đã đọc hoặc chạy) hay Inferred.**

## Quy trình

### 1. Đóng khung
- Nhắc lại mục tiêu trong 2–3 câu. Nêu **định nghĩa thành công** đo được, ví dụ "p95 < 300ms ở 50 rps", "1 người vận hành được", "thêm intent mới trong 10 phút".
- Nêu các ràng buộc **cứng**: luật, ngân sách, hạ tầng hiện có, kỹ năng của đội. Tách riêng chúng khỏi các ràng buộc **mềm**, tức là những thứ chỉ vì "quen làm vậy".
- Còn mơ hồ ở mức quyết định thì hỏi user tối đa 3 câu. Không thì ghi giả định và đi tiếp.

### 2. Phân rã tới nguyên tử
Bẻ đối tượng (kiến trúc, framework, repo, task) thành những thành phần không thể chia nhỏ hơn mà vẫn còn nghĩa:
- dữ liệu nào đi vào, đi ra, được lưu ở đâu;
- những phép biến đổi nào;
- những bất biến nào phải giữ (thứ tự, nhất quán, idempotent, bảo mật);
- những tài nguyên vật lý nào bị tiêu tốn (CPU, bộ nhớ, mạng, token LLM, thời gian người).

Vẽ sơ đồ luồng dữ liệu tối giản. Đây là "nguyên liệu thô" của tên lửa.

### 3. Tính "idiot index"
Với mỗi thành phần hoặc lớp trong giải pháp tham khảo, so **chi phí thực tế** với **chi phí sàn**:
- chi phí thực tế: độ phức tạp (LOC, số khái niệm, số dependency, số service), độ trễ, tiền, công vận hành;
- chi phí sàn: cái tối thiểu mà các nguyên tử ở bước 2 đòi hỏi, ví dụ "về bản chất chỉ là 1 HTTP call + 1 bảng Postgres".

Tỉ lệ cao nghĩa là có thứ đang được trả giá mà chưa rõ để làm gì. Đó là chỗ phải đào. Bảng mẫu ở `references/idiot-index.md`.

### 4. Đào "vì sao" ở những chỗ đắt
Với mỗi điểm có idiot index cao, tìm câu trả lời thật, có trích nguồn:
- nó giải quyết vấn đề gì, vấn đề đó **có tồn tại trong bối cảnh của ta không** (quy mô, tải, đội, pháp lý);
- lịch sử: issue, PR, ADR, postmortem nào đã khiến nó có mặt (Chesterton);
- người ta đã trả giá gì cho nó (issue về độ phức tạp, migration đau đớn, lock-in).

Repo tham khảo thì clone về scratchpad, đọc entrypoint và luồng chính (`references/repo-teardown.md`), chạy được thì chạy thử. Repo lớn thì giao 2–3 subagent đào song song theo từng phần.

### 5. Thuật toán 5 bước (áp lên thiết kế)
Theo **đúng thứ tự** này. Làm sai thứ tự là tối ưu hóa một thứ đáng lẽ phải bị xóa.
1. **Làm cho yêu cầu bớt ngớ ngẩn**: chất vấn từng yêu cầu, kể cả yêu cầu đến từ người giỏi.
2. **Xóa**: bỏ thành phần, bước, lớp. Nếu sau đó không phải thêm lại ít nhất ~10% thì chưa xóa đủ.
3. **Đơn giản hóa / tối ưu**: chỉ với những gì còn sót lại sau bước xóa.
4. **Tăng tốc vòng lặp**: rút ngắn chu kỳ build, test, deploy, feedback.
5. **Tự động hóa**: cuối cùng mới tự động hóa, và chỉ tự động hóa thứ đã được tinh gọn.

### 6. Xây lại từ đầu, rồi so
- Phác **thiết kế tối thiểu** chỉ từ các nguyên tử và yêu cầu đã qua chất vấn: kiểu dữ liệu cốt lõi trước, rồi luồng, rồi ranh giới module.
- So từng điểm với giải pháp tham khảo, chia thành ba nhóm:
  - **lấy**: những thứ tham khảo làm tốt hơn và lý do có thật trong bối cảnh của ta;
  - **bỏ**: những thứ chỉ phục vụ bối cảnh của họ;
  - **thiếu**: những thứ cả hai đều chưa có.
- Quyết định khó đảo ngược (một cánh cửa một chiều) hoặc có `--arena` thì chạy skill **arena** với ≥2 thiết kế khác nhau về cấu trúc (ví dụ "tối giản tự viết" và "dùng thư viện X"), có một ghế phản biện tiền đề.

### 7. Khuyến nghị
Viết báo cáo theo `templates/principal-report.md` vào `PRINCIPAL_<slug>.md` (đầu ra ngắn thì trả trong chat). Màn hình đầu tiên phải trả lời được: **làm gì, vì sao (3 lý do gốc), tốn bao nhiêu, khi nào đổi ý**.

## Khi không nên dùng
- Câu hỏi tra cứu có đáp án sẵn (API nào, cú pháp gì).
- Việc nhỏ, đảo ngược được, rẻ. Cứ làm rồi đo.
