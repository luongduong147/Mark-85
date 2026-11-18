---
name: shinobi-mode
description: "Chế độ nhẫn giả: xử lý nhiệm vụ trong thời gian thực ngắn nhất bằng chiến thuật subagent song song tối đa, không tiếc token; xong việc thì xóa sạch mọi dấu vết (file tạm, worktree, nhánh, tiến trình) trừ doc và sản phẩm. Dùng cho /shinobi-mode <nhiệm vụ>, hoặc 'làm nhanh nhất có thể', 'gấp', 'cần ngay'."
argument-hint: "<nhiệm vụ>"
disable-model-invocation: true
---

# Shinobi mode

Nhiệm vụ: **$ARGUMENTS** (nếu harness không thay biến này, vd dsh, lấy tham số từ phần user gõ kèm lệnh)

Trước tiên đọc **`../hokage-mode/SKILL.md`** (lõi: luật bất biến, router, điều phối) và cột **Shinobi** trong `../hokage-mode/references/dials.md`. File này chỉ ghi phần riêng của chế độ. Mọi đường dẫn `../…` tính từ thư mục của skill này, không phải thư mục làm việc: thay bằng đường dẫn tuyệt đối trước khi chạy lệnh.

**Thước đo duy nhất là thời gian từ lúc nhận nhiệm vụ tới lúc điều kiện xong được kiểm.** Token không phải ràng buộc. Chất lượng thì không được giảm: điều kiện xong vẫn phải VERIFIED.

## Chiến thuật tốc độ
1. **Khởi động trước.** Ngay trong lượt đầu, trước khi lập kế hoạch xong, chạy ngầm (`run_in_background`) những thứ chậm mà kiểu gì cũng cần: cài dependency, build, chạy test baseline, khởi động dev server. Lập kế hoạch trong lúc chúng chạy.
2. **Kế hoạch tối đa 5 dòng.** Chỉ gồm:
   - đường găng: chuỗi bước phụ thuộc nhau, quyết định thời gian tổng;
   - các nhánh chạy song song bên cạnh đường găng.
   Không viết spec, không chọn 3 hướng, không arena (trừ khi đua nhanh hơn ngồi nghĩ).
3. **Mọi lời gọi độc lập gửi trong một message**, cả tool lẫn Agent. Đọc 5 file thì gửi 5 lệnh Read cùng lúc. Không đọc tuần tự.
4. **Chia việc theo đường nối, không theo thói quen.**
   - Tách theo file, module, câu hỏi con, persona. Mỗi phần một agent, ghi thì mỗi con một worktree.
   - Khối lượng lớn đồng dạng thì dùng `/kage-bunshin` với N lớn và `haiku`.
5. **Đua khi chưa chắc.**
   - Có 2 cách đều hợp lý thì giao cả hai cho 2 agent cùng lúc.
   - Cách nào qua kiểm trước thì lấy. Hủy con kia bằng `TaskStop`, xóa worktree của nó.
   - Áp dụng cho cả việc tìm gốc lỗi: mỗi giả thuyết một agent.
6. **Không ngồi chờ.** Trong lúc agent chạy, tự làm phần việc trên đường găng hoặc chuẩn bị bước kiểm. Không poll.
7. **Kiểm sớm, kiểm hẹp, kiểm một lần.**
   - Viết lệnh kiểm điều kiện xong ngay từ đầu.
   - Chạy test hẹp trên vùng bị chạm trước, full suite chạy ngầm song song.
   - Không review panel. Dấu hiệu rủi ro rõ (auth, dữ liệu, migration) thì thêm đúng một verifier `sonnet`, chạy song song chứ không nối tiếp.
8. **Model theo tốc độ.**
   - `haiku` cho đọc rộng và việc cơ học.
   - `sonnet` cho code.
   - `opus` chỉ cho bước khó nhất trên đường găng, khi một lần làm đúng nhanh hơn ba lần thử.
9. **Không hỏi.** Chọn cách đảo ngược được, ghi lại lý do trong một dòng. Việc không đảo ngược được (deploy, force-push nhánh chung, xóa dữ liệu thật, gửi tin ra ngoài) vẫn phải dừng hỏi. Tốc độ không mua được ngoại lệ.
10. **Cắt đuôi.** Điều kiện xong vừa VERIFIED thì hủy ngay mọi agent còn chạy và mọi job ngầm không còn cần.

## Rút lui không dấu vết
Nhẫn giả xong việc thì không để lại gì, trừ tài liệu và chính sản phẩm.
1. Commit sản phẩm, nếu nhiệm vụ có yêu cầu commit. Còn thứ phải giữ thì truyền `--keep <glob>`.
2. `TaskStop` mọi agent còn sống. Mỗi bầy phân thân: `python3 ../kage-bunshin/scripts/kage.py down --run <id> --purge`.
3. `python3 ../hokage-mode/scripts/trail.py sweep`: đọc danh sách, rồi chạy lại với `--yes --purge`.
   - Bị dọn: file và thư mục mới không phải doc (build, cache, script tạm, ảnh chụp, log), worktree mới, nhánh mới, tiến trình mới đang nghe cổng.
   - Được giữ: `*.md`, `*.rst`, `docs/`, mọi thứ có từ trước nhiệm vụ.
   - Không bao giờ bị đụng: file đã track còn thay đổi chưa commit. Script chỉ cảnh báo.
4. Xóa file tạm ngoài repo mà chính nhiệm vụ đã tạo trong scratchpad hay `/tmp` (đường dẫn bạn tự biết vì bạn tạo ra chúng).
5. Kiểm lần cuối, rồi `trail.py end`:
   - `git status` chỉ khác lúc đầu ở phần sản phẩm;
   - `git worktree list` chỉ còn worktree chính;
   - không còn cổng nào do nhiệm vụ mở.

## Báo cáo (≤ 5 dòng)
1. Đã xong gì.
2. Kiểm bằng lệnh gì, kết quả ra sao.
3. Mất bao lâu, đã chạy song song bao nhiêu agent.
4. Đã dọn những gì.
5. Rủi ro còn lại (nếu có).
