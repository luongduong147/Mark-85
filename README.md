# Mark 85: cuộn trục nhẫn thuật cho agent

> *"Nhẫn giả không ship thứ mình chưa kiểm. Đó là nhẫn đạo của làng này."*

Chào mừng tới Làng Lá phiên bản code. Đây là cuộn trục nhẫn thuật cho agent của tôi, chạy được trên cả **Claude Code** và **dsh**. Không phải một câu thần chú dài dán vào chat, mà là 17 nhẫn thuật rời. Mỗi thuật làm một việc cho ra hồn, và biết lúc nào nên gọi đồng đội. Cái tên Mark 85 là di sản từ thời trước, giữ lại cho kỷ niệm.

Tôi đã thua đủ trận để rút ra bốn điều:

1. **Vá triệu chứng là trò của genin.** Tìm gốc, sửa cả lớp lỗi.
2. **Một mình thì có điểm mù.** Gọi phân thân, cho chúng đấu với nhau, rồi lấy chiêu thắng.
3. **Không có dữ liệu thì chỉ là đoán mò.** Shikamaru không đoán, Shikamaru tính.
4. **Thứ gì vào làng cũng phải qua cổng.** Kể cả chính Hokage.

---

## Bốn chế độ chỉ huy

Từng nhẫn thuật thì ai cũng học được. Biết dùng thuật nào, lúc nào, với đội hình nào mới là việc của Hokage. Gõ một chế độ cùng nhiệm vụ, nó tự lập kế hoạch, chọn playbook, ghép combo nhẫn thuật và điều phối agent với model hợp vai.

| Chế độ | Gọi | Tối ưu cho | Phong cách |
|---|---|---|---|
| **`hokage-mode`**: *ghế Hokage* | `/hokage-mode <nhiệm vụ>` | tự chọn 1 trong 3 chế độ dưới | Đọc nhiệm vụ, xếp hạng, chọn đội. Không rõ thì chọn Sage. |
| **`shinobi-mode`**: *nhẫn giả* | `/shinobi-mode <nhiệm vụ>` | thời gian thực ngắn nhất, không tiếc token | Chạy ngầm việc chậm ngay lượt đầu, mọi nhánh độc lập chạy cùng lúc, có 2 cách thì cho đua, kiểm đúng một lần. Xong là rút: xóa sạch file tạm, worktree, nhánh, tiến trình. Chỉ để lại doc và sản phẩm. |
| **`sage-mode`**: *tiên nhân thuật* | `/sage-mode <nhiệm vụ>` | độ chính xác, logic nhìn thấy được | Giả thuyết viết ở dạng có thể sai, ngưỡng đặt trước khi đo, verifier độc lập khác model. Báo cáo có chuỗi lập luận, bảng giả thuyết và "điều gì sẽ làm tôi đổi ý". |
| **`bruiser-mode`**: *Rock Lee* | `/bruiser-mode <nhiệm vụ>` | việc dài hơi, tiết kiệm token tối đa | Không có ninjutsu xịn, chỉ có lì: đơn vị nhỏ, checkpoint mỗi bước để sống qua compact, `haiku` trước, đọc theo đoạn, log ra file. Gặp vùng không tiến thêm thì đổi cách, không dừng. |

Cả ba dùng chung một bộ máy: router, playbook, luật cho subagent và sổ nhiệm vụ `trail.py`. Khác nhau ở cách vặn núm:

| Núm | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Song song | tối đa, đua 2 cách | 2–4 nhánh | 1–2 |
| Agent viết code | `sonnet`, `opus` cho đường găng | `sonnet` high, `opus` cho phần tinh vi | `haiku` → `sonnet` sau 2 lần trượt |
| Kiểm chứng | 1 lần, ngay khi có thể | mỗi giả thuyết có phép thử bác bỏ | mỗi đơn vị một kiểm rẻ |
| Dọn dẹp | xóa hẳn, giữ doc | thùng rác 7 ngày | cuối mỗi đợt |
| Báo cáo | ≤ 5 dòng | lập luận + độ tin cậy | tiến độ so với điều kiện xong |

Luật không chế độ nào bỏ được:
- kiểm trên sản phẩm thật;
- dừng hỏi trước deploy, force-push nhánh chung, xóa dữ liệu thật và tin nhắn gửi ra ngoài.

Nhanh cỡ nào cũng không mua được ngoại lệ.

---

## Cuộn trục nhẫn thuật

### Nhãn thuật: nhìn ra vấn đề

| Nhẫn thuật | Kết ấn | Công dụng |
|---|---|---|
| **`chase-it`**: *ninken truy vết* | `/chase-it <hiện tượng>` | Lỗi lúc có lúc không? Thả chó ninja đánh hơi: đặt log có đánh dấu, khoanh vùng dần. Bắt được rồi thì thu hết dấu vết tạm. |
| **`refactor-or-nothing`**: *Byakugan* | tự kích hoạt: "có nên refactor không" | Nhìn xuyên kinh mạch codebase, đo nợ kỹ thuật có bằng chứng, ra phán quyết LEAVE / CONTAIN / REFACTOR / REWRITE. Không có "tùy anh". |
| **`principal-hero`**: *bàn shogi của Shikamaru* | `/principal-hero <chủ đề \| repo>` | Tư duy từ gốc: phân rã thành phần, tính idiot index, xóa trước rồi mới tối ưu. Phiền phức thật, nhưng phải nghĩ cho tới. |
| **`show-me-the-simply-dump`**: *talk-no-jutsu* | `/show-me-the-simply-dump` | Giải thích như Naruto nói chuyện: không thuật ngữ, ví dụ đời thường, dưới 150 chữ, nghe xong là hiểu. |

### Nhẫn thuật tấn công: làm ra thứ mới

| Nhẫn thuật | Kết ấn | Công dụng |
|---|---|---|
| **`factory`**: *xưởng nhẫn cụ của Tenten* | `/factory <feature>` | Spec → build → 4 reviewer song song → approve → merge. Tôi chỉ đóng dấu ở cuối. Repo riêng: [AI-Factory](https://github.com/luongduong147/AI-Factory). |
| **`generalize-fixed-it`**: *y thuật của Tsunade* | `/generalize-fixed-it <problem>` | Chữa tận gốc chứ không băng bó. Truy gốc qua log và trace, xếp nguyên nhân vào 6 tầng (L1–L6), đưa ít nhất 3 phương án, cho subagent thử từng cái, model mạnh hơn chấm. Bản vá đúng case luôn có mặt, nhưng chỉ làm mốc so sánh. |
| **`arena`**: *kỳ thi Chunin* | `/arena <n> <task>` | N agent giải cùng một bài, chỉ ra lỗi của nhau, giám khảo chấm mà không biết bài nào của ai, rồi ghép những phần tốt nhất. |
| **`clone-me`**: *Sharingan sao chép* | `/clone-me [session \| project]` | Nhìn cách tôi làm việc và những lần tôi phải chỉnh agent, chép lại thành nhẫn thuật mới, rồi diễn lại một trận cũ để chứng minh nó đánh giống tôi thật. |
| **`the-art-of-vision`**: *Choju Giga của Sai* | `/the-art-of-vision <brief>` | Vẽ ra là sống: landing page, UI app, dashboard, infographic, slide, motion, 3D. Một studio cộng một BI Developer. Đưa 3 hướng thật để chọn, tự chụp màn hình và đánh bóng tới khi không còn trông "AI vẽ". Chi tiết ở [Phòng vẽ của Sai](#phòng-vẽ-của-sai). |
| **`kage-bunshin`**: *ảnh phân thân chi thuật* | `/kage-bunshin <việc> [--n N]` | Tách việc cho N phân thân `haiku`, mỗi con một worktree riêng, chạy song song: search hàng loạt, quét toàn codebase, giả lập người dùng bằng Playwright, tìm asset, pentest trong phạm vi được phép. Bản thể kiểm lời khai, gộp báo cáo, rồi giải thuật: "pụp", worktree, nhánh và tiến trình biến mất hết. |

### Cổng làng: không cho rác lọt qua

| Nhẫn thuật | Kết ấn | Công dụng |
|---|---|---|
| **`dont-ship-shit`**: *Izumo và Kotetsu gác cổng* | `/dont-ship-shit [#PR \| !MR \| URL \| nhánh]` | Gác cổng merge cho cả GitHub và GitLab. Hỏi 5 câu, ra phán quyết MERGE / MERGE + NITS / CHANGES REQUIRED / BLOCK kèm `file:line`. Chi tiết ở [Luật cổng làng](#luật-cổng-làng). |
| **`anti-slop`**: *nhu quyền Hyuga* | `/anti-slop [phạm vi] [--fix]` | Bấm đúng huyệt, cắt dòng chakra thừa: code chết, code lặp, abstraction đầu cơ, nuốt lỗi, comment kể lể, UI gradient tím kiểu "AI dựng hộ", chữ kiểu chatbot. Xóa trước, sửa sau, hành vi giữ nguyên. |
| **`comment-mapping`**: *sổ tay của Jiraiya* | `/comment-mapping init \| annotate \| find \| history` | Comment theo When–Why–How, có ID, trỏ về spec/plan/task. Sáu tháng sau đứng ở hàm nào cũng biết nó từ đâu ra. |

### Hợp thể thuật

```
hokage-mode ──(chọn chế độ)──► router ──► playbook ──► combo nhẫn thuật bên dưới ──► trail.py sweep
chase-it ──(bắt được gốc)──► generalize-fixed-it ──(sửa xong)──► comment-mapping annotate
principal-hero --arena ──► arena ──► SYNTHESIS.md
factory ──(builder gặp bài khó)──► claude.ai bridge
brief ──► the-art-of-vision ──(metric → bộ đo → biểu đồ → 3 hướng → đánh bóng)──► anti-slop --only fe
việc to ──► kage-bunshin ──(N phân thân haiku, mỗi con một worktree)──► collect ──► kiểm chứng ──► down
PR/MR mới ──► dont-ship-shit ──(soi diff)──► anti-slop
                    └──(vá đúng case?)──► generalize-fixed-it
```

Một nhẫn thuật đứng riêng đã dùng được. Ghép đúng đội hình mới thắng được trận lớn.

---

## Luật cổng làng

Nhánh của tôi không phải bãi tập công cộng. Mỗi PR/MR muốn vào làng đều bị `dont-ship-shit` hỏi 5 câu:

| # | Câu hỏi | Vì sao |
|---|---|---|
| 1 | **Đã có ai viết cái này chưa?** | Dò code trùng nguyên văn lẫn code chép rồi đổi tên biến, và đánh dấu riêng đoạn trùng do chính tôi viết. Làm một việc hai lần không phải chăm chỉ. |
| 2 | **Có làm vỡ thứ đang chạy không?** | Chạy test ở PR, test nào đỏ thì chạy lại ở nhánh gốc. Chỉ tính lỗi do PR gây ra. Tắt hay xóa test để CI xanh thì BLOCK ngay. |
| 3 | **Test có kiểm hành vi thật không?** | Mỗi test qua hai phép thử: làm hỏng hành vi thì test đỏ, viết lại phần ruột thì test vẫn xanh. Hành vi chưa có test thì có sẵn spec Given/When/Then. |
| 4 | **Sửa tận gốc hay vá đúng case?** | Bắt các `if customer == "ACME"`, `except: pass`, `sleep` để né race condition, đối chiếu với các tầng L1–L6. |
| 5 | **PR này phục vụ tính năng nào?** | Map qua CMAP, issue, tên nhánh, commit. Kèm doc dưới 150 chữ, vì không ai đọc mô tả PR dài hơn thế. |

Thuật này chỉ đọc: không push, không sửa nhánh người khác, không tự approve. Muốn nó comment lên PR thì thêm `--post`, nó sẽ hỏi lại trước khi đăng. Muốn cổng tự đóng khi có PR mới thì xem mẫu GitHub Actions và GitLab CI trong `dont-ship-shit/references/auto-run.md`.

---

## Phòng vẽ của Sai

Tranh vẽ mà trông như AI vẽ thì không con thú mực nào sống dậy được. `the-art-of-vision` vận hành như một studio, và đổi người cầm cọ theo chất liệu:

| Chất liệu | Ai dẫn | Điều không thương lượng |
|---|---|---|
| Dashboard / BI | BI Developer | **Metric trước, biểu đồ sau.** Mỗi ô map về một thẻ metric (công thức, grain, nguồn, ngưỡng) và một quyết định. Chưa đo được thì ghi "chưa có dữ liệu", không bao giờ điền số giả. |
| Landing page, web | Art director | Màn đầu mở bằng thứ đặc trưng nhất của đề tài. Sản phẩm phải nhìn thấy được trên trang. |
| UI app | Visual designer + frontend | Bắt đầu từ tác vụ, có đủ trạng thái rỗng, tải và lỗi. Bấm được thật. |
| 3D / WebGL | Motion/3D designer | 3D phải có lý do. 60 fps, có ảnh dự phòng, không chiếm cuộn trang. |
| Infographic, slide, motion | Visual designer | Dữ liệu là nhân vật chính. Tiêu đề slide là kết luận. |

Dashboard đi theo thứ tự cố định, chưa xong bước 3 thì chưa vẽ một nét:

1. **Định nghĩa metric.** Ai xem, để quyết định gì. Dựng cây metric gồm metric chính, dẫn dắt, bảo vệ và chẩn đoán; mỗi metric một thẻ ghi công thức, grain, múi giờ và ngưỡng.
2. **Kiểm tra bộ đếm/đo.** `instrument_scan.py` quét event, counter, bảng và cột, rồi xếp từng metric vào HAVE / DERIVABLE / MISSING kèm `file:line`. Thiếu nguồn thì có sẵn spec event cần thêm.
3. **Chọn biểu đồ** theo việc người đọc phải làm: một trục y, màu đi theo thực thể, kiểm mù màu bằng công cụ chứ không bằng mắt.
4. **Đưa 3 hướng bố cục**, metric giữ nguyên ở cả ba.
5. **Đánh bóng**: chụp màn hình bằng `shot.py`, mỗi vòng sửa 3 chỗ tệ nhất, dừng khi xem kỹ không còn gì đáng sửa.

Chất liệu khác bỏ bước 1–3 nhưng giữ cổng 3 hướng và vòng đánh bóng. Không có file cổng (`metric-spec.md`, `direction-approved.md`, `polish-log.md`) nghĩa là bước đó chưa làm.

---

## Kết ấn (cài đặt)

```bash
git clone --recursive https://github.com/luongduong147/Mark-85.git Mark85skill
cd Mark85skill
./install.sh --dry-run   # xem trước sẽ làm gì
./install.sh             # kết ấn thật
```

Quên `--recursive` thì `factory` sẽ trống. Chạy thêm `git submodule update --init` là xong.

Script này làm gì:
- Symlink từng nhẫn thuật vào `~/.claude/skills/` (Claude Code) và `$DSH_HOME/skills/` (dsh). Sửa một chỗ, cả hai nơi thấy ngay.
- Sinh skill `factory` từ `AI-Factory/skills/factory.md`, gắn đường dẫn thật vào. **Mỗi lần sửa AI-Factory thì chạy lại.**
- Gặp bản cài cũ không phải symlink thì cất vào `.backup/<thời điểm>/` trước khi thay. Tôi phá làng nhiều, nhưng không phá đồ của bạn.
- Chạy lại bao nhiêu lần cũng được. Có nhẫn thuật mới thì chạy lại là nó tự nhận.

Yêu cầu: `git`, `python3` ≥ 3.8. Phần còn lại là tùy chọn:
- `gh` / `glab`: `dont-ship-shit` lấy thêm được tiêu đề và nhánh đích của PR/MR.
- Playwright hoặc Chrome/Chromium: `the-art-of-vision` chụp màn hình để đánh bóng. Có thêm Pillow thì ảnh được cắt thành từng màn hình.
- `claude` CLI: `kage-bunshin --headless` gọi `claude -p` trong từng worktree. Trong Claude Code thì không cần, vì nó dùng thẳng subagent.
- `ss` (iproute2): `trail.py sweep` tìm tiến trình do nhiệm vụ mở để tắt.

> Trên dsh, biến `$ARGUMENTS` không được thay. Mỗi nhẫn thuật đã tự biết lấy tham số từ phần bạn gõ kèm lệnh, nên bạn không cần làm gì.

---

## Tự sáng tạo nhẫn thuật

Mọi nhẫn thuật trong làng dùng chung một khung. Muốn có thuật của riêng bạn thì theo khung này, hoặc dùng `/clone-me` cho nhanh.

```
<skill-name>/
├── SKILL.md       # bắt buộc: frontmatter + quy trình
├── references/    # tài liệu chỉ đọc khi cần, để SKILL.md gọn
├── scripts/       # script tất định, chạy lại được, ưu tiên chỉ đọc
├── playbooks/     # (chế độ chỉ huy) các bước theo loại việc
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

`description` quyết định thuật có được gọi hay không. Viết dở thì thuật nằm trong cuộn trục mà không bao giờ được dùng tới.

Phần thân nên theo thứ tự: vai trò và mục tiêu → đầu ra cố định → nguyên tắc → quy trình đánh số → "chỉ đọc file X khi gặp Y" → quy tắc bàn giao → cách mở rộng.

Thuật mới cũng phải qua cổng làng: chạy `/anti-slop` trên chính nó trước khi commit.

---

## Nhẫn đạo của làng

- **Bằng chứng hơn cảm giác.** Mỗi nhận định ghi `file:line` và đánh dấu Verified hay Inferred.
- **Xóa trước, thêm sau.** Nhẫn giả mang nhẹ thì chạy nhanh.
- **Tự động hóa cái gì lặp lại.** Hai lần thì viết script. Ba lần thì viết nhẫn thuật.
- **Script lo phần đo đạc, model lo phần phán xét.** Regex chỉ gợi ý, mắt người hoặc agent mới quyết.
- **Xong nhiệm vụ thì không để lại dấu vết.** Worktree, nhánh tạm, tiến trình nền đều phải thu hồi.
- **Không push, không xóa, không deploy khi chưa được duyệt.** Nhẫn giả có kỷ luật, không phải lính đánh thuê.

---

## Ghi công

- Khung `hokage-mode` (router, playbook, luật cho subagent) chắt lọc từ `poteto-mode`. Ý tưởng `arena` và một phần của `clone-me`, `principal-hero` cũng mượn từ đây. Tất cả đều nằm trong [pstack](https://github.com/cursor/plugins/tree/main/pstack) của Lauren Tan (giấy phép MIT).
- Cũng từ pstack ([bản mirror](https://github.com/backnotprop/pstack)):
  - phần chữ của `anti-slop` rút từ skill `unslop`;
  - tiêu chí test hành vi của `dont-ship-shit` rút từ `principle-test-behavior-not-implementation`.
- Khung studio, cổng 3 hướng và vòng đánh bóng của `the-art-of-vision` chắt lọc từ [huashu-design](https://github.com/alchaincyf/huashu-design) của 花叔 (MIT). Phần chọn biểu đồ dựa trên nguyên tắc của skill `dataviz` đi kèm Claude Code.
- Tên gọi và không khí lấy cảm hứng từ *Naruto* của Kishimoto Masashi. Đây là dự án fan, không liên quan tới chủ sở hữu bản quyền.
- Làng do **Luong Duong** (luongduong147@gmail.com) dựng.

> *Hokage không phải người mạnh nhất làng. Hokage là người biết gọi đúng thuật, giao đúng người, và chịu trách nhiệm tới cùng.*
