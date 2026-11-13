---
name: clone-me
description: "Skill để tạo skill: gom những việc tôi làm lặp đi lặp lại, các quy trình dài, những lần tôi sửa lưng agent và những bài học đúc rút trong phiên làm việc (cùng transcript cũ của project), lọc ra working convention của chính tôi, rồi đóng gói thành skill mới (workflow skill hoặc <handle>-mode), rule trong CLAUDE.md, hoặc script/hook. Có bước replay để kiểm chứng skill có thật sự 'giống tôi'. Dùng cho /clone-me, 'clone me', 'đóng gói cách tôi làm thành skill', 'biến cái này thành skill', 'tôi làm cái này nhiều lần rồi'."
argument-hint: "[session | project | --since YYYY-MM-DD] [gợi ý chủ đề]"
disable-model-invocation: true
---

# Clone-me

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh). Phạm vi nguồn:
- `session` (mặc định): chỉ phiên hiện tại.
- `project`: toàn bộ transcript của project hiện tại.
- `--since <ngày>`: chỉ lấy từ ngày đó.

Phần chữ còn lại trong lệnh là gợi ý chủ đề.

Một phần ý tưởng lấy từ skill `automate-me` trong pstack của Lauren Tan (MIT). Khác biệt: skill này không chỉ sinh một `-mode` skill, mà **phân loại** mỗi mẫu hành vi vào đúng nơi chứa phù hợp, và có bước **replay** để kiểm chứng.

Mở todo list theo 7 bước.

## 1. Gom nguyên liệu (chỉ trong phạm vi được phép)
- **Phiên hiện tại**: đọc lại hội thoại. Tìm các yêu cầu lặp lại, những lần user sửa lưng ("không, làm thế này"), quy trình nhiều bước user đã dẫn dắt, và tiêu chí "xong" user chấp nhận.
- **Transcript của project**: chạy `python scripts/user_turns.py ~/.claude/projects/<cwd-slug> [--since …]`. `<cwd-slug>` là cwd với mỗi `/` thay bằng `-`. **Chỉ đọc thư mục của project hiện tại**, không quét sang project khác vì đó là hội thoại riêng tư của việc khác. Nhiều tài liệu thì chia theo thời gian và giao 2–3 subagent chạy song song, mỗi agent trả về danh sách mẫu kèm trích dẫn (session id và timestamp).
- **Đã đúc kết sẵn**: `CLAUDE.md`, `AGENTS.md`, memory (`~/.claude/projects/<slug>/memory/`), các skill đã có trong `Mark85skill/` hoặc `~/.claude/skills/`. Đọc để không tạo trùng.
- Danh sách tín hiệu cần săn nằm ở `references/mining-signals.md`.

## 2. Trích mẫu
Mỗi mẫu ghi lại:
- **mô tả**: user làm hoặc muốn gì;
- **bằng chứng**: ≥1 trích dẫn kèm session và timestamp;
- **tần suất**: số lần, số phiên;
- **loại**: quy trình, sở thích, sửa lưng, tiêu chí xong, hoặc công cụ.

Quy tắc tin cậy:
- Mẫu xuất hiện ≥2 lần hoặc ở ≥2 phiên được tính là **mạnh**.
- Mẫu chỉ xuất hiện 1 lần là **yếu**. Chỉ giữ nếu user tự nói "luôn luôn / từ giờ…".
- Hai tín hiệu mâu thuẫn nhau thì **không** codify, đưa vào câu hỏi cho user.

## 3. Phân loại: mỗi mẫu đặt vào đâu
| Mẫu | Đặt vào | Vì sao |
|---|---|---|
| Quy trình nhiều bước, có đầu vào và đầu ra rõ, lặp lại | **Workflow skill** mới (`/ten-viec`) | Gọi lại được, có cấu trúc |
| Phong cách làm việc chung (độ dài trả lời, ngôn ngữ, mức tự chủ, cách verify) | **`<handle>-mode` skill**, hoặc cập nhật nếu đã có | Áp cho mọi việc |
| Một dòng luật ngắn, luôn đúng trong repo | **Rule trong CLAUDE.md / AGENTS.md** | Rẻ, luôn được nạp |
| Việc phải xảy ra tự động ("mỗi khi…", "trước khi commit…") | **Hook / script / CI check** | Máy làm thì chắc hơn lời nhắc |
| Sự thật về user hoặc dự án | **Memory** | Không phải quy trình |
| Mẫu chỉ là bổ sung cho một skill đang có | **Sửa skill đó** | Tránh trùng |

## 4. Hỏi user (ngắn)
Dùng AskUserQuestion, tối đa 2 lượt:
1. Chọn nhiều trong danh sách mẫu mạnh: giữ cái nào. Mỗi option kèm loại và nơi đặt đề xuất.
2. Hỏi riêng những mẫu mâu thuẫn hoặc mơ hồ.

Sau đó hỏi thêm một câu tự do: "còn thói quen nào tôi chưa thấy?". Không hỏi dồn 20 câu.

## 5. Soạn
- Skill mới theo khung `templates/skill-skeleton.md`, cũng là template chung trong `Mark85skill/README.md`:
  - phần frontmatter có `description` nêu rõ skill làm gì và khi nào dùng, kèm các câu user thực sự đã gõ (lấy từ transcript, đây là cụm kích hoạt thật nhất);
  - phần thân gồm nguyên tắc, quy trình đánh số, quy tắc đầu ra, và các file `references/` nếu dài.
- Viết bằng **chính giọng và thuật ngữ của user** (lấy từ transcript), mệnh lệnh ngắn, có tính thao tác. Không ẩn dụ, không văn hoa.
- **Tham chiếu, không chép lại**: cần skill khác thì ghi tên skill đó, không dán nội dung.
- Chỉ viết những mục có luật cụ thể, không theo mặc định. "Giao tiếp rõ ràng" không phải là một luật.
- Đặt skill mới vào `Mark85skill/<ten-skill>/` (hỏi user nếu muốn đặt chỗ khác). Rule CLAUDE.md thì sửa trực tiếp file. Hook thì dùng skill `update-config`.

## 6. Kiểm chứng bằng replay (bước khó nhưng bắt buộc với workflow skill)
Theo `references/replay-eval.md`:
1. Từ transcript, chọn 1–2 **tình huống thật** mà user đã làm việc đó, gồm đầu vào ban đầu và kết quả user chấp nhận cuối cùng.
2. Spawn subagent A **có** skill mới (nhét SKILL.md vào prompt) và subagent B **không có** skill. Cả hai nhận đúng đầu vào ban đầu đó.
3. Một judge (context sạch) so output của A và B với kết quả user đã chấp nhận. Judge chấm: A có đi đúng các bước user đã dẫn dắt không, có tránh được những lần user phải sửa lưng không, và số lần cần user can thiệp ước tính là bao nhiêu.
4. Nếu A không hơn B rõ rệt thì skill chưa nắm được điều cốt lõi. Quay lại bước 2 hoặc bước 5.

Với `-mode` skill thì kiểm bằng cảm nhận của user: cho user đọc bản nháp và hỏi "đọc có giống bạn không, thiếu gì?".

## 7. Bàn giao
Báo user:
- danh sách đã tạo hoặc sửa (đường dẫn);
- mẫu nào đi đâu, bảng tóm tắt;
- kết quả replay;
- mẫu đã bỏ và lý do (yếu, mâu thuẫn, trùng).

Đề xuất cách cài: symlink `Mark85skill/<skill>` vào `~/.claude/skills/` hoặc `<repo>/.claude/skills/`. **Không** tự cài vào nơi đồng bộ dùng chung, không push.

## Rào chắn
- Không overfit theo một hội thoại. Một câu nói lúc bực mình không phải là luật.
- Không ghi secret, token hay dữ liệu khách hàng từ transcript vào skill.
- Ghi theo nghĩa "user", không ghi tên người trong câu mệnh lệnh.
- Skill mới không được mâu thuẫn với CLAUDE.md đang có. Thấy mâu thuẫn thì hỏi user.
