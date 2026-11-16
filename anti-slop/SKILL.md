---
name: anti-slop
description: "Rà soát code vừa viết (thường do AI viết) để tìm và gỡ slop: code thừa, code lặp, abstraction đầu cơ, guard phòng thủ vô lý, comment kể lể, nuốt lỗi; giao diện FE trông 'giống AI' (gradient tím, glassmorphism, emoji, copy kiểu landing page); và chữ kiểu AI trong comment, docstring, UI, doc. Báo cáo theo file:line, phân loại MUST KILL / SHOULD / KEEP, và với --fix thì xóa trước, sửa sau. Dùng cho /anti-slop [phạm vi] [--fix], hoặc khi nói 'rà code thừa', 'code này lặp không', 'dọn code AI viết', 'UI trông AI quá', 'unslop', 'deslop', 'clean up', 'gọn lại đi'."
argument-hint: "[<file|thư mục|--diff <base>>] [--fix] [--only code|fe|text]"
---

# Anti-slop

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh)
- Phạm vi: file hoặc thư mục được nêu; không nêu thì lấy **diff so với `main`, gồm cả working tree và file chưa track**. Nếu không có `main`, dùng nhánh mặc định của remote.
- `--fix`: sửa những mục đã được chấp nhận. Không có cờ này thì chỉ báo cáo.
- `--only code|fe|text`: chỉ chạy một lăng kính.

Slop là phần code có mặt mà không trả được tiền thuê chỗ: xóa đi thì hành vi không đổi, còn người đọc thì đỡ mệt. Mục tiêu là **ít dòng hơn, cùng hành vi, đọc nhanh hơn**. Không phải để code đẹp theo gu ai đó.

## Đầu ra cố định
1. Bảng phát hiện, mỗi dòng gồm `file:line`, lăng kính, mã luật, mức (MUST KILL / SHOULD / KEEP) và cách sửa trong một câu.
2. Có `--fix`: số dòng xóa và thêm (lấy từ `git diff --stat`), test trước và sau khi sửa, các mục còn mở.
3. Lưu theo `templates/slop-report.md` nếu phạm vi lớn hơn 10 file; nhỏ hơn thì chỉ in trong chat.

## Nguyên tắc
- **Không đổi hành vi.** Mọi lần xóa phải giữ nguyên thứ người dùng của code quan sát được. Không chắc thì không xóa; ghi vào mục còn mở.
- **Xóa trước, thêm sau.** Cách sửa đúng gần như luôn là bỏ bớt. Một abstraction mới chỉ được thêm khi nó thay thế được ít nhất hai bản lặp có thật.
- **Script chỉ gợi ý.** `scripts/slop_scan.py` dùng regex nên có báo nhầm, ví dụ `console.log` trong một CLI là hợp lệ. Mỗi cờ phải được đọc tận nơi rồi mới xếp mức.
- **Ở trong phạm vi.** Thấy slop ngoài phạm vi thì ghi vào "ngoài phạm vi", không sửa.
- **Đừng thay slop này bằng slop khác.** Gỡ xong một guard thừa không có nghĩa là thêm comment giải thích vì sao gỡ.

## Quy trình

### 1. Khoanh phạm vi và đo mốc
- Xác định danh sách file và dòng cần xét.
- Có `--fix` thì chạy test và linter trước, ghi kết quả làm mốc. Không tìm được lệnh test thì hỏi, hoặc ghi rõ là sẽ sửa mà không có lưới an toàn và chỉ làm các mục MUST KILL hiển nhiên.

### 2. Quét bằng máy
Chạy từ gốc repo:
```bash
python3 <skill>/scripts/slop_scan.py --diff main      # hoặc: slop_scan.py <file|thư mục>
```
Chạy thêm linter sẵn có của repo để bắt import, biến và tham số không dùng (`ruff`, `eslint`, `tsc --noEmit`, `cargo clippy`…). Script này không làm lại việc của linter.

### 3. Đọc bằng mắt
Script không bắt được phần lớn slop đáng tiền, vì đó là vấn đề hình dạng chứ không phải từ khóa. Đọc toàn bộ phạm vi theo ba lăng kính:
- **Code**: theo `references/code-slop.md`. Tự hỏi: dòng này mất đi thì có test nào đỏ, có người dùng nào thấy khác không?
- **FE**: theo `references/fe-slop.md`, chỉ khi phạm vi có UI. Tự hỏi: bỏ logo đi thì màn hình này có lẫn với một nghìn landing page do AI dựng không? Nếu có thể, mở app (skill **run**, hoặc screenshot qua trình duyệt) thay vì chỉ đọc class.
- **Chữ**: theo `references/text-slop.md`, áp dụng cho comment, docstring, chuỗi UI, README và commit message.

Phạm vi lớn hơn khoảng 20 file thì giao bước này cho một subagent có góc nhìn mới, dùng prompt ở `references/reviewer-prompt.md` kèm danh sách file. Sau đó đọc lại báo cáo của nó và loại những mục mà nó nói sai lý do.

### 4. Xếp mức
- **MUST KILL**: code chết, code lặp nguyên văn, nuốt lỗi làm mất thông tin, debug sót lại, comment kể lại đúng điều dòng code đã nói, cast `any` hay ignore che lỗi thật, emoji hay copy giả trong UI production.
- **SHOULD**: abstraction đầu cơ (một interface chỉ có một cài đặt, factory chỉ tạo một thứ), guard cho trường hợp không thể xảy ra, lặp theo cấu trúc, phong cách FE chung chung, chữ kiểu AI.
- **KEEP**: thứ trông như slop nhưng có lý do thật. Lý do phải nằm ngoài tầm kiểm soát của chúng ta (ràng buộc của thư viện, API bên ngoài, yêu cầu pháp lý) hoặc phải có test chứng minh. Ghi lý do đó, kèm `file:line` làm bằng chứng.

### 5. Sửa (chỉ khi có `--fix`)
Làm theo thứ tự, chạy lại test sau mỗi nhóm:
1. Xóa: code chết, debug, comment kể lể, code bị comment lại.
2. Gộp: các khối lặp về **một** nguồn sự thật, đặt ở chỗ code gọi sẵn có. Không tạo file `utils` mới chỉ để chứa một hàm.
3. Làm phẳng: gỡ wrapper, factory hay layer chỉ chuyển tiếp lời gọi; gỡ guard không thể kích hoạt; để lỗi nổi lên thay vì bị nuốt.
4. FE: thay giá trị cứng bằng token sẵn có của design system; bỏ gradient, glow, emoji và copy giả. Không tự sáng tác một style mới; nếu repo chưa có design system, chỉ báo cáo.
5. Chữ: viết lại theo `text-slop.md`.

Test đỏ sau một nhóm thì revert nhóm đó, ghi vào mục còn mở, rồi làm tiếp nhóm sau. Không commit; user tự xem diff.

### 6. Báo cáo
Ghi: số cờ máy bắt và số mục được xác nhận; danh sách theo mức; số dòng (−/+) nếu đã sửa; test trước và sau; KEEP kèm lý do; những gì ngoài phạm vi.

## Chỉ đọc khi cần
- `references/code-slop.md`: luôn đọc ở bước 3.
- `references/fe-slop.md`: khi phạm vi có `.tsx/.jsx/.vue/.svelte/.html/.css`.
- `references/text-slop.md`: khi có comment, doc hay chuỗi UI dài.
- `references/reviewer-prompt.md`: khi giao bước 3 cho subagent.

## Phối hợp
- **dont-ship-shit** có thể gọi skill này trên diff của PR. Khi đó chỉ báo cáo, không `--fix`, vì không sửa nhánh của người khác.
- Khối lặp có `mine: true` từ `dss.py dupes`: gộp về hàm cũ thay vì giữ hai bản.
- Muốn đánh giá sâu hơn (có nên refactor cả module không) thì dùng **refactor-or-nothing**.
- Sửa xong mà đụng tới logic có comment-mapping thì cập nhật block `[CMAP]` (STATUS `REFACTOR`).
