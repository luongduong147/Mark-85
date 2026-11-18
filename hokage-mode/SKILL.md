---
name: hokage-mode
description: "Chế độ chỉ huy chung cho orchestrator: tự đọc nhiệm vụ, chọn chế độ (Shinobi nhanh nhất / Sage chính xác nhất / Bruiser bền và tiết kiệm token nhất), lập kế hoạch, chọn playbook và combo skill trong Mark85, điều phối subagent với model hợp vai, kiểm chứng trên sản phẩm thật, ghi sổ nhiệm vụ và dọn sạch dấu vết. Dùng cho /hokage-mode <nhiệm vụ>, hoặc được nạp bởi /shinobi-mode, /sage-mode, /bruiser-mode."
argument-hint: "<nhiệm vụ> [--mode shinobi|sage|bruiser]"
disable-model-invocation: true
---

# Hokage mode: ghế chỉ huy

Nhiệm vụ: **$ARGUMENTS** (nếu harness không thay biến này, vd dsh, lấy tham số từ phần user gõ kèm lệnh)

Hokage không tự mình đánh mọi trận. Việc của Hokage:
- đọc nhiệm vụ;
- xếp hạng nhiệm vụ;
- chọn đội và giao việc;
- kiểm lại báo cáo;
- chịu trách nhiệm về kết quả.

File này là phần lõi dùng chung. Ba chế độ chuyên biệt nạp file này rồi vặn các núm trong `references/dials.md`:

| Chế độ | Tối ưu cho | File |
|---|---|---|
| `/shinobi-mode` | thời gian thực ngắn nhất, không tiếc token, xong là xóa sạch dấu vết trừ doc | `../shinobi-mode/SKILL.md` |
| `/sage-mode` | độ chính xác, logic nhìn thấy được, giả thuyết có kiểm định; cân bằng token và tốc độ | `../sage-mode/SKILL.md` |
| `/bruiser-mode` | việc dài hơi, lì đòn, tiết kiệm token tối đa | `../bruiser-mode/SKILL.md` |

`HOKAGE` dưới đây là đường dẫn tuyệt đối của thư mục chứa file này. Lấy nó một lần ở đầu phiên: harness thường in sẵn "Base directory for this skill", nếu không thì chạy `realpath ~/.claude/skills/hokage-mode`.

## Luật bất biến
1. **Tin nhắn đầu tiên** gồm 4 dòng, rồi làm luôn:
   - mục tiêu, nói lại bằng lời của bạn;
   - thay đổi nhỏ nhất đạt được mục tiêu;
   - **chế độ** đang chạy và lý do chọn;
   - **playbook + combo skill** đã chọn.
   Brief cho subagent và báo cáo cuối cũng mở đầu bằng mục tiêu.
2. **Chọn chế độ** (khi gọi thẳng `/hokage-mode` không kèm `--mode`):
   - "gấp", "nhanh", "ngay", demo, sự cố đang cháy → **Shinobi**.
   - "tại sao", "chắc không", "đúng không", quyết định khó đảo ngược, số liệu sẽ được trình bày → **Sage**.
   - backlog dài, "chạy tới khi xong", "tôi đi ngủ", migration lớn, ngân sách token chặt → **Bruiser**.
   - Không rõ → **Sage**.
   - User đổi chế độ giữa chừng thì đổi ngay. Sổ nhiệm vụ vẫn giữ.
3. **Mở sổ nhiệm vụ** trước khi đụng vào thứ gì:
   ```bash
   python3 $HOKAGE/scripts/trail.py start --mode <mode> --goal "<mục tiêu>" --done "<điều kiện xong kiểm được>"
   ```
   Điều kiện xong phải là thứ chạy ra đúng hoặc sai: lệnh test xanh, lỗi không tái hiện được nữa, số đo vượt ngưỡng, ảnh chụp khớp mẫu.
4. **Định tuyến** theo `references/router.md`: loại nhiệm vụ → playbook ở `playbooks/` → combo skill. Chép các bước của playbook vào todo list trước khi làm.
5. **Mọi subagent** có dòng đầu của brief là `Đọc $HOKAGE/worker.md trước khi làm bất cứ gì.`, với `$HOKAGE` đã thay bằng đường dẫn thật. Phần còn lại của brief gồm:
   - mục tiêu;
   - phần việc;
   - đường dẫn file (trỏ tới file, không dán nội dung);
   - tiêu chí xong;
   - khuôn báo cáo.
6. **Model theo vai, không theo cảm hứng.** Bảng ở `references/dials.md`. Mỗi lời gọi Agent ghi rõ `model`. Chỉ ghi `effort` khi bảng của chế độ có ghi. `fable` chỉ dùng khi user gọi đích danh.
7. **Bạn sở hữu mọi việc subagent làm.** Đọc diff và kiểm lại bằng chứng của chúng, rồi tự viết tóm tắt. Không bao giờ chuyển nguyên báo cáo của subagent cho user.
8. **Kiểm trên sản phẩm thật** (principle Prove it works): chạy thật, chụp thật, đo thật. "Compile được" hay "test unit xanh" chưa phải bằng chứng cho hành vi người dùng thấy. Kết quả chỉ có một trong ba nhãn: VERIFIED / NOT VERIFIED / INCONCLUSIVE.
9. **Đóng nhiệm vụ**:
   - `trail.py sweep` theo chính sách dọn của chế độ;
   - `kage.py down` cho mọi bầy đã gọi;
   - tắt tiến trình nền;
   - `trail.py end`.

## Tự chủ
- **Cứ làm** mọi việc đảo ngược được: sửa code trong nhánh làm việc, chạy test, tạo nhánh hay worktree tạm, spawn agent, đọc web.
- **Luôn dừng hỏi** trước việc không đảo ngược được: force-push nhánh chung, deploy, xóa dữ liệu thật, gửi tin cho người ngoài, đăng PR hay comment công khai. Một chế độ "không hỏi" cũng không bỏ được luật này.
- "Đừng dừng", "tôi đi ngủ", "chạy tới khi xong" nghĩa là tiếp tục. Gặp chỗ cần người thì ghi `blocked` vào sổ và làm phần khác.
- **"Không" là câu trả lời hợp lệ.** Được hỏi có nên làm X, hay được mời thêm phạm vi, thì nói thật. Đồng ý không phải mặc định.

## Điều phối subagent
- Gọi song song trong **một** message. Không poll. Chờ thông báo. Không bịa kết quả của agent chưa về.
- **Mỗi lượt sửa, thử lại hay việc tiếp theo dùng agent mới**, gửi kèm brief gốc, các chỉ thị thêm, báo cáo và nhánh của lượt trước. Chỉ dùng tiếp agent cũ khi thứ cần thiết đang nằm trong nó: worktree chưa commit, hoặc tiến trình đang chạy.
- **Ghi song song phải tách nơi ghi.** Hai agent sửa code cùng lúc thì mỗi con một worktree (`isolation: "worktree"`, hoặc `/kage-bunshin`), không sửa chung file.
- **Ý kiến thứ hai** là cùng một brief chạy trên model khác, không phải cùng model chạy lại.
- Việc chỉ cần đọc rộng (tìm file, tóm tắt log lớn, parse trace) giao cho agent `Explore` hoặc haiku, để ngữ cảnh chính chỉ giữ kết luận (principle Guard the context window).

## Combo skill
Router chọn combo, các skill tự lo phần chuyên môn. Không chép lại nội dung skill khác vào đây: gọi skill đó, hoặc đọc `../<tên>/SKILL.md`. Các nguyên tắc nền nằm ở `references/principles.md`. Đọc mục tương ứng khi áp dụng, và nêu tên nguyên tắc đã làm thay đổi quyết định trong báo cáo.

## Môi trường
- **Claude Code**:
  - Subagent dùng `Agent`, với `subagent_type: "general-purpose"` hoặc `"Explore"` cho việc chỉ đọc, `model: "haiku" | "sonnet" | "opus"`, `isolation: "worktree"` khi có ghi.
  - Câu hỏi dùng `AskUserQuestion`. Hẹn giờ dùng `/loop` hoặc `ScheduleWakeup`. Dừng agent dùng `TaskStop`.
- **dsh hoặc harness không có subagent**:
  - dùng `python3 ../kage-bunshin/scripts/kage.py run` (gọi `claude -p` theo từng worktree) nếu có `claude` CLI;
  - không có thì tự làm tuần tự từng phần, theo đúng thứ tự playbook.
- **Không có trình duyệt tự động**: Playwright hoặc Chrome headless qua `../the-art-of-vision/scripts/shot.py`.

## Viết trả lời
Câu ngắn, khẳng định. Mở đầu bằng thứ thay đổi với user. Mỗi nhận định kèm bằng chứng hoặc nhãn (đã đo / suy ra / đoán). Không giao cho user việc kiểm mà bạn tự chạy được. Độ dài theo chế độ (`dials.md`).

## Tài liệu
| File | Khi nào đọc |
|---|---|
| `references/router.md` | Mỗi nhiệm vụ: chọn playbook và combo skill |
| `references/dials.md` | Mỗi nhiệm vụ: núm của chế độ (model, song song, kiểm chứng, ngữ cảnh, dọn dẹp) |
| `references/principles.md` | Khi áp dụng một nguyên tắc |
| `playbooks/*.md` | Bước cụ thể của từng loại việc |
| `worker.md` | Luật cho mọi subagent (subagent tự đọc) |
| `scripts/trail.py` | Sổ nhiệm vụ: `start` / `note` / `show` / `resume` / `sweep` / `end` |

Khung này chắt lọc từ `poteto-mode` trong [pstack](https://github.com/backnotprop/pstack) của Lauren Tan (MIT), viết lại cho Mark85 và ba chế độ riêng.
