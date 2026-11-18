---
name: bruiser-mode
description: "Chế độ lì đòn: xử lý nhiệm vụ dài hơi không biết mệt (backlog dài, migration lớn, chạy qua đêm) với mục tiêu tiết kiệm token tối đa: đơn vị nhỏ, checkpoint mỗi bước để sống sót qua compact và phiên mới, model rẻ trước, đọc ít, log ra file, gặp vùng không tiến thêm thì đổi cách chứ không dừng. Dùng cho /bruiser-mode <nhiệm vụ>, hoặc 'chạy tới khi xong', 'tôi đi ngủ', 'làm hết backlog', 'tiết kiệm token'."
argument-hint: "<nhiệm vụ> [--done <điều kiện xong>]"
disable-model-invocation: true
---

# Bruiser mode

Nhiệm vụ: **$ARGUMENTS** (nếu harness không thay biến này, vd dsh, lấy tham số từ phần user gõ kèm lệnh)

Trước tiên đọc **`../hokage-mode/SKILL.md`** (lõi) và cột **Bruiser** trong `../hokage-mode/references/dials.md`. File này chỉ ghi phần riêng của chế độ. Mọi đường dẫn `../…` tính từ thư mục của skill này, không phải thư mục làm việc: thay bằng đường dẫn tuyệt đối trước khi chạy lệnh.

**Thước đo là kết quả trên mỗi token, và việc có về đích hay không.** Chậm cũng được, miễn không dừng giữa đường và không đốt token vào những thứ không đưa nhiệm vụ tới gần điều kiện xong.

## Khung bền
1. **Điều kiện xong là một lệnh.** Ghi vào sổ bằng `trail.py start --mode bruiser --done "<lệnh> → <kết quả mong đợi>"`. Chưa viết được lệnh đó thì việc đầu tiên là viết nó.
2. **Chia đơn vị nhỏ.** Mỗi đơn vị:
   - xong trong khoảng ≤ 15 lượt công cụ;
   - kết thúc bằng một lần kiểm rẻ;
   - được commit riêng.
   Ghi danh sách đơn vị vào sổ (`note plan`).
3. **Checkpoint sau mỗi đơn vị**: `trail.py note checkpoint "<xong đơn vị k/N; kế tiếp: …; bẫy: …>"`. Mọi thứ cần để làm tiếp phải nằm trong sổ, không chỉ trong đầu.
4. **Sau compact, phiên mới, hay "làm tiếp"**: chạy `trail.py resume` trước tiên. Không đọc lại code đã đọc, không chạy lại thứ đã VERIFIED.
5. **Chờ thứ chậm** (CI, job dài) thì dùng `/loop` hoặc `ScheduleWakeup` với nhịp hợp với tốc độ thay đổi của thứ đang chờ. Không poll dày, không ngồi chờ trong ngữ cảnh.

## Lì đòn
- **Vùng không tiến thêm không phải điểm dừng.** Ba lần thử không tiến thì đổi loại cách tiếp cận: đọc lại nguồn, đổi giả thuyết, chia đơn vị nhỏ hơn, hoặc build công cụ làm thay.
- **Không thử lại cùng một cách.** Mọi lần thất bại ghi vào sổ (`note hyp … --verdict refuted`). Đọc sổ trước khi thử cách mới.
- **Ba cách thất bại có cùng tiền đề** thì kiểm tiền đề đó.
- **Bị chặn** (cần người, cần quyền, cần quyết định sản phẩm) thì ghi `note blocked`, chuyển sang đơn vị khác. Không ngồi chờ.
- **Chỉ dừng khi** điều kiện xong đạt, gặp việc không đảo ngược được (vẫn dừng hỏi), hoặc ngõ cụt thật. Ngõ cụt thì báo đã thử những gì, vì sao loại. Không nới điều kiện xong để tuyên bố thắng.

## Tiết kiệm token
**Đọc ít**
- `grep -n` / `rg` trước khi mở file. Read có `offset`/`limit` quanh chỗ cần.
- Không bao giờ đọc lại file vừa sửa để "kiểm tra".

**Output gọn**
- Test chạy chế độ yên lặng và chỉ in lỗi (`-q`, `--tb=line`, `--reporter=dot`), rồi `| tail -30`.
- Build và log dài ghi ra file, chỉ đọc phần lỗi.
- Diff xem bằng `--stat` trước, mở chi tiết đúng file cần.

**Không lặp**
- Không chép lại kế hoạch, không tóm tắt lại thứ đã có trong sổ.
- Câu trả lời giữa chừng chỉ là một dòng tiến độ.

**Dùng đòn bẩy**
- 20 lần sửa giống nhau thì viết một script hay codemod chạy một lần.
- Kiểm hàng loạt thì viết một lệnh tổng hợp ra PASS/FAIL.

**Subagent**
- Chỉ dùng khi nó rẻ hơn tự đọc: đọc file lớn, tóm tắt log, quét nhiều file.
- `haiku`, brief yêu cầu trả về ≤ 20 dòng, chi tiết ghi ra file.
- Lên `sonnet` sau 2 lần `haiku` thất bại cùng việc. `opus` chỉ khi user cho phép.
- Không review panel, không arena, không bầy lớn (`kage-bunshin` tối đa 2–3 con).

**Song song**
- Tối đa 2, và chỉ khi một nhánh đang chờ IO.

## Dọn dẹp
`trail.py sweep --yes` cuối mỗi đợt lớn, và lần cuối khi xong. Sổ được giữ lại để làm hồ sơ.

## Báo cáo
- **Giữa chừng**: `[k/N] <đơn vị vừa xong> · kiểm: <kết quả> · tiếp: <đơn vị kế>`
- **Cuối**:
  - điều kiện xong và trạng thái cuối;
  - số đơn vị làm được, số đơn vị bị loại, số đơn vị `blocked` kèm lý do;
  - đường dẫn sổ;
  - việc nên làm tiếp nếu còn.
