---
name: comment-mapping
description: "Comment có cấu trúc theo When–Why–How (ngày phát hiện, ngày sửa, tại sao sửa, ảnh hưởng tới đâu, sửa thế nào), mỗi block có ID và trỏ ngược về spec / plan / task trong checklist. Dùng khi dựng repo hoặc pattern mới (/comment-mapping init), sau mỗi lần sửa lỗi hoặc thêm module (annotate), khi hỏi 'tìm đoạn code xử lý việc này' (find), hoặc 'module này đã phát triển qua những phiên bản nào' (history / map). Kích hoạt cả khi CLAUDE.md có rule Comment mapping."
argument-hint: "[init | annotate <path> | find \"<việc cần tìm>\" | history <module|path> | map | lint]"
---

# Comment-mapping

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh) (không có → `annotate` cho thay đổi vừa làm trong phiên).

Comment ở đây là **bản đồ truy vết**: mỗi block trả lời *khi nào* (phát hiện / sửa / tạo), *tại sao* (lỗi gì, ảnh hưởng tới đâu), *thế nào* (cơ chế sửa) và *thuộc yêu cầu nào* (spec / plan / task). Người đọc sau, hoặc agent sau, đứng tại một hàm là biết nó từ đâu ra và đã đổi ra sao.

- Định dạng chuẩn: `references/comment-format.md`. **Đọc trước khi viết block đầu tiên.**
- Công cụ: `scripts/cmap.py` (chỉ đọc, thư viện chuẩn). Đường dẫn script tính từ thư mục skill này.

## Các chế độ

### `init`: dựng playbook cho repo (chạy một lần khi dựng repo / dựng pattern)
1. Tìm tài liệu nguồn: spec, plan, checklist (`docs/`, `*.md` ở gốc, `factory/jobs/*/spec.md`…). Không có → hỏi user đường dẫn, hoặc ghi `none`.
2. Xác định các module và tiền tố ID (theo thư mục cấp 1–2 hoặc theo boundary trong kiến trúc).
3. Tạo `docs/CMAP.md` theo `references/playbook-template.md`.
4. Thêm **một mục rule** vào `CLAUDE.md` (hoặc `AGENTS.md` nếu repo dùng file đó; có cả hai thì thêm vào cả hai). Nội dung có sẵn trong playbook-template. Không lặp lại nếu đã có.
5. Tùy chọn (hỏi user): đặt block `NEW` cho từng module chính hiện có, làm mốc ban đầu (`When: created=<ngày commit đầu tiên của file>`, lấy bằng `git log --diff-filter=A --format=%ad --date=short -- <file> | tail -1`).

### `annotate [path]`: viết hoặc cập nhật block (mặc định)
1. Xác định thay đổi: `git diff` (cả staged), hoặc đoạn vừa sửa trong phiên, hoặc `path` được chỉ định.
2. Chọn STATUS: file hay hàm mới là `NEW`; sửa lỗi là `FIX`; đổi hành vi theo yêu cầu là `CHANGE`; không đổi hành vi là `REFACTOR`; ngừng dùng là `DEPRECATED`.
3. Lấy ID: `python scripts/cmap.py next-id <root> <module>`.
4. Điền Ref: tìm mục spec, bước plan, task trong checklist liên quan (grep theo từ khóa của thay đổi). Không chắc thì ghi `Ref: none (chưa có spec)` và báo user. Không bịa số mục.
5. Điền When:
   - Ngày phát hiện lấy từ hội thoại, issue hoặc log. Không biết thì để là ngày hôm nay và ghi chú `found≈`.
   - Ngày sửa là hôm nay.
6. Đặt block **ngay trên** đơn vị code. Đã có block thì thêm block mới lên trên, không sửa lịch sử cũ. Quá 3 block thì chuyển các block cũ vào Archive trong `docs/CMAP.md`.
7. Nếu checklist có task tương ứng, đánh dấu task đó kèm ID CMAP.
8. Chạy `python scripts/cmap.py lint <root>`.

### `find "<việc cần tìm>"`: tìm đoạn code xử lý việc này
1. `python scripts/cmap.py find <root> <từ khóa…>` để tìm trong CMAP block trước, vì đây là chỗ có nghĩa nghiệp vụ.
2. Không có kết quả hoặc kết quả yếu:
   - Tìm trong code bằng grep theo từ khóa, tên hàm, route, string trong UI hoặc log.
   - Đọc spec để biết thuật ngữ, rồi grep theo thuật ngữ đó.
   - Repo lớn thì giao cho một subagent Explore.
3. Trả về danh sách `file:line` xếp theo độ chắc chắn. Mỗi kết quả kèm 1 dòng mô tả "đoạn này làm gì" và ID CMAP nếu có. Code đúng là chỗ xử lý mà chưa có block thì đề xuất `annotate`.

### `history <module|path>`: module đã phát triển qua những phiên bản nào
1. `python scripts/cmap.py history <root> <module|path>` cho ra timeline CMAP và git log.
2. Ghép hai nguồn thành **process map** có các mốc:
   - ngày, ID, STATUS, tóm tắt Why/How;
   - commit liên quan;
   - task/spec liên quan.
3. Chỉ ra các giai đoạn, ví dụ "v1 dùng keyword, v2 chuyển semantic routing, v3 hybrid". Chỉ ra cả khoảng trống: có commit lớn mà không có CMAP thì ghi là "chưa được ghi lại".
4. Mặc định trả kết quả trong chat. User muốn lưu thì ghi vào `docs/cmap/<module>-history.md`.

### `map`: chỉ mục toàn repo
Chạy `scan --json` để tổng hợp `docs/CMAP_INDEX.md`, gồm:
- bảng theo module (ID, STATUS, tiêu đề, file:line, ngày);
- spec/plan/task nào chưa có code trỏ tới;
- block nào có Ref gãy.

### `lint`
Chạy `python scripts/cmap.py lint <root>`, sửa các block thiếu field hoặc Ref gãy (có hỏi user khi phải đoán).

## Quy tắc
- Viết theo ngôn ngữ của repo/user (mặc định tiếng Việt). ID, đường dẫn, tên hàm giữ nguyên.
- How mô tả **cơ chế**, không chép diff. Why phải có bằng chứng (log, số case lỗi, issue).
- Không viết CMAP cho các thay đổi lặt vặt như đổi tên, format, typo.
- Không đưa secret hay dữ liệu khách hàng vào comment.
- Gọi từ skill khác (generalize-fixed-it, chase-it, AI-Factory builder) thì dùng chế độ `annotate`.
