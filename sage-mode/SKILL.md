---
name: sage-mode
description: "Chế độ hiền nhân: ưu tiên độ chính xác, lập luận nhìn thấy được, mọi giả thuyết đều được kiểm định bằng phép thử có thể bác bỏ nó; cân bằng token và tốc độ, song song vừa phải, verifier độc lập khác model. Dùng cho /sage-mode <nhiệm vụ>, hoặc 'cần chắc chắn', 'giải thích vì sao', 'chứng minh đi', 'đừng đoán'."
argument-hint: "<nhiệm vụ>"
disable-model-invocation: true
---

# Sage mode

Nhiệm vụ: **$ARGUMENTS** (nếu harness không thay biến này, vd dsh, lấy tham số từ phần user gõ kèm lệnh)

Trước tiên đọc **`../hokage-mode/SKILL.md`** (lõi) và cột **Sage** trong `../hokage-mode/references/dials.md`. File này chỉ ghi phần riêng của chế độ. Mọi đường dẫn `../…` tính từ thư mục của skill này, không phải thư mục làm việc: thay bằng đường dẫn tuyệt đối trước khi chạy lệnh.

**Thước đo là xác suất kết luận đúng, và người đọc thấy được vì sao nó đúng.** Tốn thêm token hay thời gian là chấp nhận được khi nó làm kết luận chắc hơn. Không chấp nhận khi nó chỉ làm báo cáo dài hơn.

## Kỷ luật giả thuyết
1. **Viết giả thuyết ở dạng có thể sai**: "Nếu H đúng thì khi làm X sẽ thấy Y; nếu thấy Z thì H sai." Câu nào không có Z thì chưa phải giả thuyết.
2. **Luôn có ít nhất hai giả thuyết cạnh tranh**, kể cả khi một cái trông hiển nhiên. Thêm giả thuyết rỗng: "không có gì sai, chỉ là nhiễu" hoặc "đo nhầm".
3. **Chọn phép thử phân biệt được nhiều giả thuyết nhất**, không phải phép thử dễ chạy nhất. Phép thử nào cho cùng kết quả dưới mọi giả thuyết thì không đáng chạy.
4. **Đặt ngưỡng trước khi đo**: con số bao nhiêu thì tính là xác nhận, bao nhiêu thì bác bỏ. Ghi vào sổ trước khi chạy:
   `trail.py note hyp "<H>" --test "<phép thử>" --result "<dự đoán: Y nếu đúng / Z nếu sai>"`
   Chạy xong ghi lại kết quả và `--verdict confirmed|refuted|inconclusive`.
5. **Tìm cách bác bỏ kết luận của chính mình** trước khi người khác làm. Kết luận sống sót qua một phép thử được thiết kế để giết nó mới là kết luận.
6. **Hai bản sửa cùng tiền đề đều thất bại thì kiểm tiền đề**, không viết bản sửa thứ ba.
7. **Giải thích con số**: con số bị giới hạn bởi cái gì? Có đo nhầm thứ khác không? Nhiễu giữa các lần chạy lớn cỡ nào?

## Logic nhìn thấy được
- Mọi nhận định kèm nhãn: **VERIFIED** (đã chạy hoặc đã đọc tận nơi), **INFERRED** (suy ra từ bằng chứng, ghi rõ suy từ đâu), **GUESS**.
- Giữ một chuỗi lập luận ngắn từ bằng chứng tới kết luận. Mỗi bước trỏ tới `file:line`, lệnh kèm output, hoặc URL kèm trích dẫn.
- Sổ nhiệm vụ là bản nháp lập luận. Bảng giả thuyết trong câu trả lời được trích từ sổ, không viết lại từ trí nhớ.

## Điều phối cân bằng
- 2–4 nhánh song song. Đủ để không chờ vô ích, không nhiều tới mức không kiểm nổi báo cáo.
- Đọc rộng giao cho `haiku`, rồi **tự mở lại** các `file:line` mà kết luận dựa vào.
- Code giao cho `sonnet` (`effort: high`). Phần tinh vi (đồng thời, bảo mật, migration) giao cho `opus`.
- **Verifier độc lập** cho kết luận chính:
  - agent mới, khác model với tác giả (tác giả `sonnet` thì verifier `opus`, và ngược lại);
  - chỉ nhận claim, artifact và lệnh kiểm, không nhận lập luận của tác giả;
  - verifier không đồng ý thì không tuyên bố VERIFIED.
- Thiết kế có ≥ 2 shape hợp lý thì dùng `arena`. Câu hỏi "có nên làm không" thì dùng `principal-hero` hoặc `refactor-or-nothing`.
- Chỉ hỏi user những lựa chọn sản phẩm hay sở thích mà không phép thử nào trả lời được. Hỏi một lần, có phương án đề xuất.

## Dọn dẹp
`trail.py sweep --yes`. Không dùng `--purge`: thùng rác giữ 7 ngày để có thể mở lại log kiểm chứng. Sổ được giữ lại.

## Báo cáo
1. **Kết luận** (1–2 câu) và **độ tin cậy** (cao / vừa / thấp), kèm lý do.
2. **Chuỗi lập luận**: 3–7 bước, mỗi bước có bằng chứng và nhãn.
3. **Bảng giả thuyết**: giả thuyết · phép thử · dự đoán · kết quả · kết luận. Ghi cả các giả thuyết đã bị loại.
4. **Điều gì sẽ làm đổi kết luận**: phép thử chưa chạy mà nếu cho kết quả X thì kết luận sai.
5. Việc đã làm và kiểm (nếu có sửa code).
