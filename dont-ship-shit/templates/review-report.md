# Dont-ship-shit — <id>: <tiêu đề PR/MR>

**Phán quyết: <MERGE | MERGE + NITS | CHANGES REQUIRED | BLOCK>.** <một câu lý do>

- Nền tảng: <github | gitlab | git> · Đích: `<base>` · Head: `<sha ngắn>` · Merge-base: `<sha ngắn>`
- Test: <đã chạy `<lệnh>` ở head (+ base cho test đỏ) | chưa chạy, lý do>
- PR này <một câu: thay đổi hành vi gì>

## 5 tiêu chí

| # | Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Double work | PASS / WARN / FAIL | `file:line` ↔ `file:line` (exact/shape, của ai) |
| 2 | Regression | PASS / WARN / FAIL / chưa chạy | test đỏ mới, test bị skip/xóa |
| 3 | Test hành vi | PASS / WARN / FAIL | test nào qua/trượt phép thử nào |
| 4 | Tổng quát | PASS / WARN / FAIL | tầng gốc L?, bản sửa đánh ở đâu |
| 5 | Map tính năng | PASS / WARN / FAIL | <tính năng> (nguồn: CMAP / issue / nhánh / suy luận) |

## Phải làm trước khi merge
1. <việc> — `file:line` — <vì sao>

## Spec test hành vi còn thiếu
```
Hành vi: …
Given …
When …
Then …
Phá thử: …
Vị trí: …
```

## Nợ cũ (không tính vào phán quyết)
- <test đỏ ở cả base lẫn head, cảnh báo có sẵn…>

## Doc cho PR (<150 chữ)
<PR làm gì, vì sao, ảnh hưởng tới đâu, kiểm tra thế nào.>

<sub>Verified = đã chạy hoặc đã đọc tận nơi · Inferred = suy luận. Tạo bởi /dont-ship-shit.</sub>
