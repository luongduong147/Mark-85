# Mark 85 — Agent Armor

> *"Mấy cái suit trước cũng ổn. Cái này thì khác: nó tự lắp vào người bạn trong vòng một lệnh `./install.sh`."*

Chào mừng tới xưởng. Đây là bộ giáp skill dành cho agent của tôi, chạy được cả trên **Claude Code** lẫn **dsh**. Không phải một prompt dài lê thê dán vào chat, mà là các module rời: mỗi cái làm một việc, làm cho ra hồn, và biết khi nào nên gọi module bên cạnh.

Tôi đã làm hỏng đủ nhiều bản Mark trước để biết ba điều:

1. **Vá triệu chứng là trò của nghiệp dư.** Tìm gốc, sửa cả lớp lỗi.
2. **Một bộ não thì có điểm mù.** Cho chúng đấu với nhau, rồi lấy bản thắng.
3. **Không có dữ liệu thì chỉ là đoán mò.** Mà tôi không đoán.

---

## Kho vũ khí

| Module | Kích hoạt | Nó làm gì (bản ngắn, vì tôi bận) |
|---|---|---|
| **`factory`** — *dây chuyền lắp ráp* | `/factory <feature>` | Spec → build → 4 reviewer song song → approve → merge. Tôi chỉ ký tên ở cuối. Repo riêng: [AI-Factory](https://github.com/luongduong147/AI-Factory). |
| **`refactor-or-nothing`** — *máy quét hư hại* | tự kích hoạt: "có nên refactor không" | Đo nợ kỹ thuật có bằng chứng và ra phán quyết LEAVE / CONTAIN / REFACTOR / REWRITE. Không có "tùy anh". |
| **`generalize-fixed-it`** — *phòng thí nghiệm* | `/generalize-fixed-it <problem>` | Truy gốc qua log và trace, xếp nguyên nhân vào 6 tầng (L1–L6), đưa ra ≥3 giải pháp, cho subagent chạy thử từng cái, rồi một model mạnh hơn chấm điểm. Bản vá đúng case luôn có mặt, nhưng chỉ để làm mốc so sánh. |
| **`comment-mapping`** — *hộp đen* | `/comment-mapping init \| annotate \| find \| history` | Comment When–Why–How có ID, trỏ về spec/plan/task. Sáu tháng sau, đứng ở bất kỳ hàm nào cũng biết nó từ đâu ra. |
| **`arena`** — *đấu trường* | `/arena <n> <task>` | Thả N agent giải cùng một bài, cho chúng chứng minh lỗi của nhau, judge chấm mà không biết bài nào của ai, rồi ghép những phần tốt nhất lại. |
| **`clone-me`** — *J.A.R.V.I.S. học việc* | `/clone-me [session \| project]` | Đọc cách tôi làm việc, những lần tôi phải sửa lưng agent, rồi đóng gói thành skill mới. Sau đó phát lại một tình huống cũ để chứng minh nó thật sự giống tôi. |
| **`show-me-the-simply-dump`** — *chế độ Happy* | `/show-me-the-simply-dump` | Giải thích như cho người không làm kỹ thuật. Không thuật ngữ, có ví dụ đời thường, dưới 150 chữ. |
| **`chase-it`** — *radar* | `/chase-it <hiện tượng>` | Lỗi lúc có lúc không? Đặt log theo dõi có đánh dấu, khoanh vùng dần, bắt được rồi thì gỡ sạch log tạm. |
| **`principal-hero`** — *bàn vẽ* | `/principal-hero <chủ đề \| repo>` | Tư duy từ gốc: phân rã thành phần, tính idiot index, xóa trước rồi mới tối ưu. Không hỏi tên lửa giá bao nhiêu, mà hỏi vì sao nó đắt thế. |
| **`dont-ship-shit`** — *cổng an ninh xưởng* | `/dont-ship-shit [PR \| MR \| URL]` | Gác cổng merge cho GitHub lẫn GitLab. Soi 5 thứ: code có trùng thứ tôi đã viết không, có làm vỡ regression không, test có kiểm hành vi thật không, sửa tổng quát hay vá đúng case, và PR thuộc tính năng nào (kèm doc dưới 150 chữ). Ra phán quyết MERGE / CHANGES REQUIRED / BLOCK, kèm `file:line`. |
| **`anti-slop`** — *máy mài vỏ giáp* | `/anti-slop [phạm vi] [--fix]` | Mài hết phần thừa: code chết, code lặp, abstraction đầu cơ, nuốt lỗi, comment kể lể, UI gradient tím kiểu "AI dựng hộ", chữ kiểu chatbot. Xóa trước, sửa sau, hành vi giữ nguyên. |

### Combo

```
chase-it ──(bắt được gốc)──► generalize-fixed-it ──(sửa xong)──► comment-mapping annotate
principal-hero --arena ──► arena ──► SYNTHESIS.md
factory ──(builder gặp bài khó)──► claude.ai bridge
PR/MR mới ──► dont-ship-shit ──(soi diff)──► anti-slop ──(vá case?)──► generalize-fixed-it
```

Từng module đứng riêng đã ổn. Ghép lại với nhau mới là bộ giáp.

---

## Lắp giáp

```bash
git clone --recursive https://github.com/luongduong147/Mark-85.git Mark85skill
cd Mark85skill
./install.sh --dry-run   # xem trước sẽ làm gì
./install.sh             # lắp thật
```

Quên `--recursive` thì `factory` sẽ trống. Chạy thêm `git submodule update --init` là xong.

Script này làm gì:
- Symlink từng skill vào `~/.claude/skills/` (Claude Code) và `$DSH_HOME/skills/` (dsh). Sửa một chỗ, cả hai nơi thấy ngay.
- Sinh skill `factory` từ `AI-Factory/skills/factory.md`, gắn đường dẫn thật vào. **Mỗi lần sửa AI-Factory thì chạy lại.**
- Gặp bản cài cũ không phải symlink thì cất vào `.backup/<thời điểm>/` trước khi thay. Tôi phá đồ nhiều, nhưng không phá đồ của bạn.
- Chạy lại bao nhiêu lần cũng được.

> Trên dsh, biến `$ARGUMENTS` không được thay. Mỗi skill đã tự biết lấy tham số từ phần bạn gõ kèm lệnh, nên bạn không cần làm gì.

---

## Tự chế module mới

Mọi module trong xưởng dùng chung một khung. Muốn làm module của riêng bạn thì cứ theo khung này, hoặc dùng `/clone-me` cho nhanh.

```
<skill-name>/
├── SKILL.md       # bắt buộc: frontmatter + quy trình
├── references/    # tài liệu chỉ đọc khi cần, để SKILL.md gọn
├── scripts/       # script tất định, chạy lại được, ưu tiên chỉ đọc
├── agents/        # (skill điều phối) mỗi file là prompt cho một subagent
└── templates/     # khung đầu ra
```

```yaml
---
name: kebab-case-name
description: "<làm gì>. Dùng khi <tình huống>, hoặc khi gõ /<name>, '<câu bạn hay gõ thật>'…"
argument-hint: "<tham số>"
disable-model-invocation: true   # bỏ dòng này nếu muốn model tự kích hoạt
---
```

`description` là bộ kích hoạt. Viết dở thì module nằm trong kho mà không bao giờ được gọi tới.

Phần thân nên theo thứ tự này: vai trò và mục tiêu → đầu ra cố định → nguyên tắc → quy trình đánh số → "chỉ đọc file X khi gặp Y" → quy tắc bàn giao → cách mở rộng.

---

## Nguyên tắc của xưởng

- **Bằng chứng hơn cảm giác.** Mỗi nhận định ghi `file:line` và đánh dấu Verified hay Inferred.
- **Xóa trước, thêm sau.** Bộ giáp nhẹ thì bay nhanh.
- **Tự động hóa cái gì lặp lại.** Hai lần thì viết script. Ba lần thì viết skill.
- **Không push, không xóa, không deploy khi chưa được duyệt.** Ngầu thì ngầu, nhưng có kỷ luật.

---

## Ghi công

- Ý tưởng `arena` và một phần của `clone-me`, `principal-hero` mượn từ [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan (giấy phép MIT). Phần chữ của `anti-slop` rút từ skill `unslop`, tiêu chí test hành vi của `dont-ship-shit` rút từ `principle-test-behavior-not-implementation`, cũng của pstack ([bản mirror](https://github.com/backnotprop/pstack)). Thiên tài cũng biết đứng trên vai người khổng lồ.
- Lắp ráp tại xưởng bởi **luongduong147@gmail.com**.

> *Bộ giáp chỉ ngầu bằng người mặc nó. Nhưng ngầu hơn nữa thì cứ thêm module vào.*
