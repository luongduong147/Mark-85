# Report template

Write in the user's language (Vietnamese example headings shown; translate if the user writes another language). Keep code, paths and commands untranslated. Delete sections that do not apply; keep the order. Target 3-6 pages; push raw evidence to the appendix.

```markdown
# Báo cáo quyết định refactor: <tên dự án / phạm vi>

Ngày: <YYYY-MM-DD> · Phạm vi: <repo / module / PR> · Độ tin cậy: <Cao | Trung bình | Thấp> (<lý do>)

## 1. Kết luận
**Quyết định:** <LEAVE | CONTAIN | REFACTOR-TARGETED | REFACTOR-PROGRAM | REWRITE | INSUFFICIENT-DATA>
(nếu mỗi khu vực một kết luận, dùng bảng: Khu vực | Quyết định | Lý do ngắn)

Ba lý do chính:
1. ...
2. ...
3. ...

Việc cần làm ngay: <1-3 dòng>
Điều kiện làm đổi quyết định: <các trigger>

## 2. Bối cảnh và giả định
- Mục tiêu / roadmap 3-6 tháng tới: <đã biết | giả định>
- Quy mô đội, tốc độ thay đổi: <số liệu | giả định>
- Phạm vi đã đọc và phần chỉ lấy mẫu: <...>

## 3. Bức tranh tổng thể
Kiến trúc trong 5-10 dòng (kèm sơ đồ nếu có ích). Số liệu chính từ hotspots.py: LOC theo ngôn ngữ, tỷ lệ test, top hotspot.

## 4. Lỗi và rủi ro cần xử lý riêng (không phải nợ kỹ thuật)
Bảng: ID | Mô tả | file:line | Mức độ | Cách khắc phục | Bằng chứng

## 5. Phát hiện về nợ kỹ thuật
Bảng: ID | Khu vực | Phát hiện | file:line | Mức độ | Lãi suất | Công sức | Bằng chứng (Verified/Inferred)
Sau bảng: 2-4 phát hiện quan trọng nhất, mỗi cái 3-5 dòng (vấn đề, vì sao tốn kém, hướng sửa).

## 6. "Trông tệ nhưng thực ra ổn"
Những thứ nhìn giống nợ nhưng nên giữ, kèm lý do (đã kiểm tra lịch sử/test).

## 7. Mô hình chi phí
Bảng cho từng khu vực: Lãi/tháng | Gốc (khoảng person-day) | Rủi ro khi sửa | Thời gian hoàn vốn | Giả định.
Phân tích độ nhạy: kết luận có đổi không nếu lãi suất giảm một nửa / tăng gấp đôi?

## 8. Các phương án
Với mỗi khu vực có nhiều lựa chọn: Giữ nguyên | Cô lập | Refactor từng phần | Refactor có hệ thống | Viết lại — ưu/nhược, chi phí, rủi ro, vì sao chọn/loại.
(Nếu cân nhắc REWRITE: chứng minh đủ 5 điều kiện ở decision-framework.md.)

## 9. Kế hoạch (chỉ khi quyết định là REFACTOR-*)
Các bước nhỏ, tự phát hành độc lập. Mỗi bước: mục tiêu, cách làm (strangler/branch by abstraction/...), test cần có trước, chỉ số thành công, cách rollback, ước lượng.

## 10. Việc nhanh (quick wins) và thói quen phòng ngừa
Các việc ≤ 2 ngày có lợi ngay; quy tắc/CI để nợ không tăng lại.

## 11. Điều chưa kiểm chứng
Những gì không đọc/không chạy được, dữ liệu cần thêm để nâng độ tin cậy.

## Phụ lục: Bằng chứng
Lệnh đã chạy và tóm tắt kết quả; bảng hotspot; danh sách file đã đọc.
```

## Finding entry format (for the key findings)
- **ID & title** (e.g. D-03 Agent loop mixes policy and execution)
- **Where**: `path/file.py:120-310`
- **Evidence**: what you observed/ran; Verified or Inferred
- **Why it costs**: tie to change frequency or incidents (e.g. "touched in 14 of the last 60 commits; each change edits 4 files")
- **Fix**: smallest change that removes most of the cost; effort S/M/L/XL with range
- **Risk of fixing**: tests present? critical path?

## Quality bar before delivering
- The verdict is on the first screen and every verdict has triggers.
- Every finding has a path and an evidence level; no claim of "slow", "complex", "duplicated" without a number or concrete example.
- Estimates are ranges with stated assumptions; sensitivity checked.
- Defects are separated from debt; "looks bad but fine" section is present.
- Nothing recommends a rewrite without the five conditions shown.
