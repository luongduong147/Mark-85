# Router: nhiệm vụ → playbook → combo skill

Đọc nhiệm vụ, chọn **một** dòng phù hợp nhất. Nhiệm vụ có nhiều phần thì tách ra: mỗi phần một dòng, chạy theo thứ tự phụ thuộc. Không dòng nào khớp thì dùng `playbooks/long-run.md` ở pha Lập kế hoạch để tự thiết kế playbook.

## Bảng định tuyến
| Tín hiệu trong nhiệm vụ | Playbook | Combo skill (theo thứ tự) |
|---|---|---|
| "tại sao", "cái này chạy thế nào", "ở đâu", không cần sửa | `investigation` | Explore/haiku đọc rộng → `principal-hero` nếu là câu hỏi thiết kế → `show-me-the-simply-dump` nếu user cần bản dễ hiểu |
| lỗi tái hiện được | `bug-fix` | `generalize-fixed-it` (tìm gốc, ≥ 3 phương án) → `comment-mapping annotate` |
| lỗi lúc có lúc không, không có log | `bug-fix` (bước 1 thay bằng săn) | `chase-it` → `generalize-fixed-it` → `comment-mapping annotate` |
| tính năng mới | `feature` | `principal-hero` (shape) → `factory` nếu muốn dây chuyền đầy đủ, không thì tự giao việc → `anti-slop` → `dont-ship-shit` (tự review trước khi mở PR) |
| thiết kế có nhiều cách hợp lý, còn tranh cãi | `feature` bước 2 | `arena <n>` để các phương án đấu với nhau |
| dọn code, đổi cấu trúc, giữ nguyên hành vi | `refactor` | `refactor-or-nothing` (có nên làm không) → `anti-slop --fix` → `comment-mapping annotate` |
| chậm, tốn tài nguyên, cần một con số tốt hơn | `perf` | `chase-it` để đặt đo → `generalize-fixed-it` |
| khối lượng lớn chia được: search hàng loạt, quét toàn repo, giả lập nhiều user, tìm asset, gọi nhiều dịch vụ, pentest có phạm vi | `research-sweep` | `kage-bunshin` → tổng hợp → skill phù hợp với phát hiện |
| UI, landing page, dashboard, slide, 3D, "trông xấu" | `design` | `the-art-of-vision` → `anti-slop --only fe` |
| PR/MR cần đánh giá, "có nên merge không" | `review-merge` | `dont-ship-shit` → `anti-slop` trên diff → `security-review` nếu chạm auth/dữ liệu |
| backlog dài, migration lớn, "chạy tới khi xong" | `long-run` | tùy từng đơn vị, mỗi đơn vị lại đi qua router |
| mất ngữ cảnh, phiên mới, "làm tiếp" | `pause-resume` (phần Tiếp tục) | `trail.py resume` → playbook cũ |
| user bảo dừng, hết giờ, sắp compact | `pause-resume` (phần Dừng) | `trail.py note checkpoint` |
| "đóng gói cách tôi làm thành skill" | `feature` (bản rút gọn) | `clone-me` |
| xong nhiệm vụ | `cleanup` | `trail.py sweep` + `kage.py down` |

Skill có sẵn của Claude Code cũng nằm trong kho: `code-review`, `simplify`, `security-review`, `dataviz`, `loop`, `schedule`. Dùng khi chúng khớp hơn skill của Mark85.

## Chế độ đổi combo thế nào
| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| `generalize-fixed-it` | bỏ vòng chấm điểm; cho 2–3 phương án chạy đua, lấy cái đầu tiên qua kiểm | đầy đủ: ≥ 3 phương án, judge model khác | 1 phương án gốc rễ rẻ nhất trước, phương án khác chỉ khi nó thất bại |
| `arena` | chỉ khi đua nhanh hơn ngồi suy nghĩ | dùng khi thiết kế còn tranh cãi | tránh (tốn N lần token) |
| `the-art-of-vision` | `--skip-directions`, đánh bóng 1 vòng | đủ 3 hướng, đánh bóng tới khi sạch | 1 hướng, đánh bóng 2 vòng |
| `kage-bunshin` | N lớn, haiku, chạy ngay | N vừa, kiểm mẫu báo cáo | N nhỏ (2–3), báo cáo ≤ 20 dòng mỗi con |
| `dont-ship-shit` | `--quick` | đầy đủ | đầy đủ, nhưng chạy test hẹp trước |
| `anti-slop` | chỉ MUST KILL | toàn bộ | chỉ trên diff |
| `comment-mapping` | bỏ qua, trừ khi repo có rule | annotate | annotate gộp cuối đợt |
