---
name: chase-it
description: "Đuổi theo một lỗi hay hiện tượng lặp đi lặp lại mà chưa có gì quan sát được (lúc có lúc không, không log, không trace): lập giả thuyết, đặt probe/log có đánh dấu vào đúng chỗ, quản lý sổ probe, thu và đọc log, thu hẹp dần như chia đôi, rồi gỡ probe tạm hoặc nâng probe tốt thành log/metric lâu dài. Dùng cho /chase-it <hiện tượng>, 'đuổi theo lỗi này', 'lỗi lúc có lúc không', 'không biết sao nó bị', 'đặt log theo dõi', 'flaky', 'thỉnh thoảng lại bị'."
argument-hint: "<hiện tượng> | status [id] | close <id>"
---

# Chase-it

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh)
- `<hiện tượng>`: mở cuộc truy đuổi mới.
- `status [id]`: xem các probe đang chạy, log đã gom và giả thuyết còn sống.
- `close <id>`: gỡ probe, nâng cấp những probe đáng giữ, viết kết luận.

Mục tiêu: biến một lỗi **không nhìn thấy** thành lỗi **nhìn thấy được và có bằng chứng**, rồi bàn giao cho bước sửa (skill **generalize-fixed-it**). Skill này không sửa lỗi; nó làm cho lỗi hiện hình.

## Khái niệm
- **Chase id**: `<slug>-<YYYYMMDD>`, ví dụ `ws-drop-20261113`.
- **Probe**: một dòng log hoặc đoạn đo tạm thời. Mỗi dòng code của probe mang marker `CHASE:<id>` trong comment (cùng dòng, hoặc bọc bằng cặp `CHASE:<id>:begin` / `CHASE:<id>:end`). Marker này giúp script tìm và gỡ chính xác.
- **Sổ truy đuổi**: `.chase/<id>/` (thêm `.chase/` vào `.gitignore`), gồm:
  - `ledger.md`: hiện tượng, giả thuyết, danh sách probe, nhật ký các phát hiện. Khung ở `references/ledger-template.md`.
  - `logs/`: log đã gom hoặc trích ra.

## Quy trình

### 1. Định danh con ma
Ghi vào ledger:
- triệu chứng chính xác (thông báo lỗi, output sai);
- tần suất (mấy lần/ngày, % request);
- lần gần nhất xảy ra;
- điều kiện đi kèm đã biết (giờ, tải, user, môi trường, sau deploy hay restart);
- những gì **đã** loại trừ.

Thiếu thông tin thì hỏi user tối đa 3 câu. Sau đó tạo chase id và thư mục sổ.

### 2. Vẽ đường đi nghi vấn
Lần theo luồng từ đầu vào đến chỗ triệu chứng lộ ra: entrypoint → các biên (I/O, mạng, queue, LLM call, DB, cache, thread hoặc async) → chỗ lỗi hiện ra. Ghi các `file:line` then chốt.

Liệt kê **≥3 giả thuyết cạnh tranh**. Với mỗi giả thuyết, viết rõ: *"nếu đúng thì log tại X sẽ cho thấy Y"*. Giả thuyết nào không chỉ ra được quan sát phân biệt nó với các giả thuyết khác thì chưa dùng được.

Đọc `references/probe-patterns.md` để chọn kiểu probe phù hợp với loại lỗi (race, timeout, rò bộ nhớ, state lưu trữ, LLM không ổn định…).

### 3. Đặt probe (ít mà trúng)
- Đặt tại **biên** và **điểm rẽ nhánh** phân biệt được các giả thuyết, không rải khắp nơi. Lần đầu chỉ đặt ≤ 8 probe.
- Mỗi dòng log là một bản ghi có cấu trúc, một dòng duy nhất, có tiền tố cố định để grep được:
  `CHASE[<id>] p=<probe#> ts=<iso> cid=<correlation id> <key>=<value> …`
  Correlation id lấy từ request, job hoặc session id sẵn có. Nếu chưa có thì tạo một id và truyền theo luồng.
- Ghi **state**, không ghi cảm xúc: giá trị, độ dài, thời gian thực thi, nhánh nào được chọn, số lần retry, kích thước queue.
- **Không log** secret, token, mật khẩu hay nội dung người dùng. Cần thì hash hoặc chỉ ghi độ dài.
- Probe chạy trong vòng lặp nóng thì phải lấy mẫu (sample) hoặc giới hạn tần suất.
- Có thể bật/tắt qua biến môi trường `CHASE_<ID>=1` nếu code chạy ở môi trường dùng chung.
- Đăng ký từng probe vào ledger: số thứ tự, `file:line`, giả thuyết mà nó kiểm, ngày đặt.
- Kiểm tra bằng `python scripts/chase_probes.py list <root> <id>`. Số probe trong code phải khớp với ledger.

### 4. Thu log & theo dõi
- Tái hiện được thì chạy kịch bản tái hiện và lặp N lần (lỗi flaky thì lặp nhiều lần).
- Lỗi xảy ra ngẫu nhiên trong môi trường thật thì theo dõi file log bằng `tail -F` / `grep --line-buffered "CHASE\[<id>\]"` qua tool Monitor, kèm điều kiện dừng khi bắt được triệu chứng. Có thể dùng `/loop` để kiểm tra định kỳ. **Không** ngồi poll liên tục.
- Trích các dòng liên quan vào `.chase/<id>/logs/`, nhóm theo correlation id: `python scripts/chase_probes.py grep <logfile> <id> --by-cid`.

### 5. Đọc & thu hẹp
- So các luồng **lỗi** với các luồng **bình thường** trong cùng khoảng thời gian. Khác biệt đầu tiên giữa hai nhóm là manh mối.
- Gạch bỏ những giả thuyết bị log phủ định, ghi lại trong ledger kèm dòng log làm bằng chứng.
- Còn nhiều giả thuyết thì **di chuyển probe**: gỡ probe vô ích, đặt probe mới ở giữa đoạn nghi vấn, cứ thế chia đôi dần. Mỗi lần đổi probe đều ghi vào ledger.
- Lặp lại bước 3–5 cho tới khi chỉ ra được *quyết định sai đầu tiên* kèm bằng chứng log.

### 6. Đóng (`close <id>`)
1. **Phân loại probe**:
   - **gỡ**: probe tạm;
   - **nâng cấp**: tín hiệu rẻ, luôn bật, giúp lần sau nhìn là thấy. Chuyển thành log chính thức hoặc metric theo convention của repo và bỏ marker `CHASE`.
2. Gỡ probe tạm: chạy `python scripts/chase_probes.py remove <root> <id> --dry-run`, xem diff, rồi chạy lại không có `--dry-run`. Sau đó `list` lại phải ra 0.
3. Chạy test hoặc build để chắc chắn việc gỡ probe không làm hỏng gì.
4. Viết kết luận vào ledger:
   - gốc rễ (hoặc giả thuyết mạnh nhất còn lại kèm độ tin cậy);
   - bằng chứng;
   - probe đã nâng cấp;
   - đề xuất sửa.
5. Nếu đã tìm ra gốc rễ, đề nghị chạy `/generalize-fixed-it` và đưa đường dẫn ledger làm đầu vào.

## Đầu ra mỗi lượt
1–3 dòng ngắn: chase id · số probe đang đặt · giả thuyết còn sống · việc kế tiếp, ví dụ "đang chờ log từ 20 lần chạy".
