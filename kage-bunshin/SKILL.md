---
name: kage-bunshin
description: "Ảnh phân thân: tách một việc lớn thành N phần và giao cho N subagent model nhẹ (mặc định haiku) chạy song song, mỗi phân thân một git worktree riêng, rồi gom báo cáo, gộp trùng và dọn sạch worktree, nhánh, tiến trình. Orchestrator (model lớn) chỉ chia việc, viết brief, kiểm chứng và tổng hợp. Hợp với việc bầy đàn: thu thập thông tin, web search số lượng lớn, rà soát toàn codebase, stress test như người dùng thật bằng Playwright/Chrome DevTools, tìm asset theo mô tả, gọi hàng loạt dịch vụ ngoài, pentest trong phạm vi được phép. Dùng cho /kage-bunshin <việc> [--n N], hoặc 'chạy song song', 'spawn nhiều agent', 'chia cho nhiều con', 'bầy agent', 'swarm', 'fan out', 'quét toàn bộ', 'search hàng loạt', 'giả lập nhiều user'."
argument-hint: "<việc> [--n <số phân thân>] [--model haiku|sonnet] [--headless] [--keep]"
---

# Kage-bunshin — ảnh phân thân

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này, vd dsh, lấy tham số từ phần user gõ kèm lệnh)
- `<việc>`: mô tả việc cần làm song song.
- `--n N`: số phân thân. Mặc định tự chọn theo cách chia việc (bước 2), tối đa 8 nếu user không nói khác.
- `--model`: model của phân thân, mặc định `haiku`. Phần nào cần suy luận nặng thì giao riêng phần đó cho `sonnet`, không nâng cả bầy.
- `--headless`: chạy bằng `scripts/kage.py run` (gọi `claude -p` trong từng worktree) thay cho công cụ Agent. Dùng trong dsh, CI, hoặc khi harness không có subagent.
- `--keep`: giữ worktree sau khi xong để user tự xem. Mặc định là dọn sạch.

Vai trò: **orchestrator** (model lớn, chính là bạn) chia việc, viết brief, kiểm chứng và tổng hợp. **Phân thân** (model nhẹ) làm phần việc tay chân của mình rồi báo cáo đúng khuôn. Phân thân không thấy cuộc trò chuyện này. Thứ duy nhất chúng biết là brief bạn viết.

## Khi nào dùng, khi nào không
Dùng khi việc **chia được thành các phần độc lập** và tổng khối lượng lớn: 40 truy vấn search, 300 file cần quét, 20 kịch bản người dùng, 15 API cần thử.

Không dùng khi:
- việc là một chuỗi phụ thuộc (bước sau cần kết quả bước trước);
- tự làm chỉ mất vài lệnh;
- các phần phải sửa cùng một file (sẽ xung đột khi gom).

Spawn tốn token. N phân thân là N lần đọc lại ngữ cảnh. Chọn N nhỏ nhất mà vẫn xong việc trong một lượt.

## Quy trình

### 1. Xác định việc và phạm vi
Viết ra một dòng: mục tiêu, đầu ra cuối cùng mà user nhận, và tiêu chí xong.

Việc chạm tới hệ thống thật (stress test, pentest, gọi dịch vụ ngoài, tự động hóa trình duyệt) phải qua **`references/rules-of-engagement.md`** trước khi spawn:
- mục tiêu thuộc user hoặc user có giấy phép;
- giới hạn tốc độ;
- không đụng production nếu chưa được nói rõ.

Thiếu phạm vi thì hỏi user **một** câu, không đoán.

### 2. Chia việc
Chọn trục chia theo `references/patterns.md`. Quy tắc chung:
- **Không chồng lấn.** Mỗi phần có ranh giới rõ: danh sách file, danh sách truy vấn, persona, endpoint.
- **Cân tải.** Code thì dùng `python3 <skill>/scripts/kage.py shard --n N [paths]`: script chia theo số dòng và giữ các file cùng thư mục chung một phần.
- **Cùng một khuôn báo cáo** cho mọi phân thân, để gom được bằng máy.
- Nhiều phần đều nhau thì dùng **bầy đồng dạng** (cùng brief, khác dữ liệu). Phần khác loại thì dùng **giao việc riêng** (brief riêng, có thể khác model).

### 3. Viết brief
Mỗi phân thân nhận một brief theo `templates/clone-brief.md`, gồm:
- mục tiêu;
- phần việc của riêng nó;
- thư mục làm việc;
- công cụ được dùng và bị cấm;
- điều kiện dừng;
- khuôn báo cáo (khối ```json ở cuối).

Model nhẹ làm đúng thứ được viết ra và đoán sai thứ bị bỏ ngỏ, nên brief phải cụ thể. Đừng gửi "tìm bug". Hãy gửi "đọc 14 file sau, tìm lỗi thuộc 4 loại sau, mỗi lỗi ghi file:line và một câu tái hiện".

### 4. Spawn
**Cách A: công cụ Agent (Claude Code).** Gọi tất cả trong **một** message để chúng chạy đồng thời. Mỗi lời gọi gồm:
- `model: "haiku"` (hoặc model của phần đó);
- `isolation: "worktree"` (mỗi con một worktree riêng);
- `description` có số thứ tự, vd `"bunshin 03: quét src/api"`;
- `prompt` là brief.

Không spawn thêm đợt hai khi đợt một chưa về. Chờ thông báo. Đừng đoán kết quả.

**Cách B: headless (`--headless`, dsh, CI).**
```bash
K=<skill>/scripts/kage.py
python3 $K up --n 5 --run audit          # 5 worktree ở ~/.cache/kage/<repo>/audit/clone-NN, nhánh kage/audit/NN
# viết tasks.jsonl: mỗi dòng {"prompt": "<brief>", "model"?: "haiku", "tools"?: "Read,Grep,...", "timeout"?: 900}
python3 $K run --run audit --tasks tasks.jsonl --model haiku
python3 $K status --run audit
```
Mỗi phân thân được cấp các biến môi trường sau, nhờ vậy các con chạy trình duyệt hay dev server không giẫm lên nhau:

| Biến | Nghĩa |
|---|---|
| `KAGE_CLONE` | số thứ tự của phân thân |
| `KAGE_PORT` | cổng riêng, để chạy dev server |
| `KAGE_PROFILE` | thư mục hồ sơ trình duyệt riêng, dùng cho `launch_persistent_context` hoặc `--user-data-dir` |
| `KAGE_OUT` | file báo cáo |

Khi không ở trong repo git, `up` tạo thư mục thường thay cho worktree.

### 5. Gom và kiểm chứng
- Cách B: `python3 $K collect --run <id>`. Lệnh này đọc khối JSON cuối của mỗi báo cáo, gộp các phát hiện trùng `key`, rồi ghi `summary.json` và in bảng trạng thái.
- Cách A: tự gom theo cùng logic từ các báo cáo trả về.

Báo cáo của model nhẹ là **lời khai, chưa phải bằng chứng**:
- **Kiểm lại tận nơi** mọi phát hiện có mức nghiêm trọng cao, cùng một mẫu ngẫu nhiên các phát hiện khác: mở file:line, chạy lại lệnh tái hiện, mở URL nguồn.
- Phát hiện chưa kiểm thì ghi `Inferred`.
- Phân thân có trạng thái `blocked`, `partial` hoặc `no-json` thì đọc log của nó. Chỉ giao lại phần thiếu, và chỉ một lần.

Phân thân có commit (việc sửa code): xem diff từng nhánh, `cherry-pick` phần dùng được vào nhánh của user **sau khi user đồng ý**. Không tự merge.

### 6. Báo cáo cho user
Theo `templates/swarm-report.md`:
- kết quả tổng hợp;
- bảng các phân thân (trạng thái, số phát hiện, thời gian);
- phát hiện đã kiểm chứng, xếp theo mức độ;
- phần chưa xong;
- chi phí ước lượng (số phân thân × model).

### 7. Dọn sạch (bắt buộc, kể cả khi hỏng giữa chừng)
```bash
python3 $K down --run <id>          # giết tiến trình còn sống, cất thay đổi chưa gom thành patch, gỡ worktree + nhánh, prune
python3 $K gc                       # rà worktree/nhánh kage/* mồ côi của các lần chạy trước; thêm --yes để dọn
```
- Với cách A: worktree không có thay đổi tự biến mất khi agent xong. Worktree có thay đổi thì gom xong mới gỡ, bằng `git worktree remove --force <path>` rồi `git branch -D <nhánh>`. Chỉ gỡ các đường dẫn mà kết quả agent trả về, không gỡ worktree của phiên khác.
- Tiến trình nền do phân thân mở (dev server, trình duyệt) phải tắt hết. Kiểm bằng `ps` theo cổng `KAGE_PORT` hoặc theo `KAGE_PROFILE`.
- Kiểm cuối:
  - `git worktree list` chỉ còn worktree chính;
  - `git branch --list 'kage/*'` trống;
  - `git status` của repo chính không đổi so với lúc bắt đầu.
- `--keep` thì bỏ qua bước này nhưng in ra lệnh `down` để user tự chạy sau.

`down` không xóa báo cáo. Báo cáo và các patch đã cất nằm ở `~/.cache/kage/<repo>/<run>/` cho tới khi chạy `down --purge`.

## Luật của bầy
- **Một phân thân, một worktree, một phần việc.** Không con nào ghi ra ngoài thư mục của mình, trừ file báo cáo.
- **Không bí mật trong brief.** Brief không chứa token hay mật khẩu. Phân thân cần quyền gì thì đọc từ biến môi trường hoặc file cấu hình sẵn có của user.
- **Không đẩy đi đâu.** Phân thân không push, không mở PR, không đăng bài, không gửi email. Mọi hành động ra ngoài đều qua orchestrator và được user xác nhận.
- **Có điểm dừng.** Mỗi brief có giới hạn thời gian và số bước. Bị chặn thì báo `blocked` kèm lý do, không xoay xở bằng cách lách.
- **Captcha và chống bot là tín hiệu dừng**, không phải chướng ngại để vượt. Trên hệ thống của user, dùng khóa test hoặc cờ tắt captcha ở môi trường staging. Trên site của người khác, gặp captcha thì báo `blocked` (chi tiết ở `rules-of-engagement.md`).
- **Orchestrator chịu trách nhiệm cuối.** Phân thân sai thì bạn sai, nếu bạn chuyển nguyên báo cáo của nó tới user mà không kiểm.

## Tài liệu
| File | Nội dung |
|---|---|
| `references/patterns.md` | Công thức cho từng loại việc bầy đàn: trục chia, N gợi ý, công cụ, khuôn phát hiện |
| `references/rules-of-engagement.md` | Phạm vi, giấy phép, giới hạn tốc độ cho stress test, pentest, dịch vụ ngoài, trình duyệt |
| `templates/clone-brief.md` | Khuôn brief cho phân thân |
| `templates/swarm-report.md` | Khuôn báo cáo tổng hợp gửi user |
| `scripts/kage.py` | `up` / `shard` / `run` / `status` / `collect` / `down` / `gc` |
