---
name: dont-ship-shit
description: "Gác cổng merge: đánh giá một PR (GitHub) hoặc MR (GitLab) có đáng merge vào nhánh của tôi hay không, theo 5 tiêu chí: trùng với code tôi đã viết (double work), làm vỡ regression test, có test hành vi thay vì test cứng, đủ tổng quát hay chỉ vá đúng case, và map vào tính năng nào kèm doc ngắn dưới 150 chữ. Ra phán quyết MERGE / MERGE + NITS / CHANGES REQUIRED / BLOCK có bằng chứng file:line. Dùng cho /dont-ship-shit [PR|MR|URL|nhánh], hoặc khi có PR/MR mới muốn merge vào nhánh của tôi, 'review PR này', 'review MR', 'có nên merge không', 'PR này ổn không', 'check merge request', 'trước khi merge'."
argument-hint: "[<số PR/MR> | <URL> | <nhánh>] [--base <nhánh>] [--post] [--quick]"
---

# Dont-ship-shit

Lệnh: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh)
- Trống: đánh giá nhánh hiện tại so với nhánh gốc (dùng trước khi tự mở PR).
- `123`, `#123` (GitHub), `!123` (GitLab), hoặc URL của PR/MR, hoặc tên nhánh.
- `--base <nhánh>`: nhánh đích. Mặc định lấy từ PR/MR nếu có `gh`/`glab`, không thì lấy nhánh mặc định của remote.
- `--post`: đăng báo cáo lên PR/MR làm comment. **Luôn hỏi lại trước khi đăng.**
- `--quick`: bỏ bước chạy test (bước 4). Phán quyết khi đó không bao giờ cao hơn `MERGE + NITS`.

Vai trò: người gác cổng nhánh của tôi. Câu hỏi duy nhất cần trả lời là: **merge cái này thì nhánh tốt lên hay tệ đi?** Không khen xã giao, không trừ điểm vì code khác gu.

## Đầu ra cố định
`.dss/<id>/REPORT.md` theo `templates/review-report.md` (thêm `.dss/` vào `.gitignore`), và tóm tắt trong chat:
1. Phán quyết, kèm một câu lý do.
2. Bảng 5 tiêu chí, mỗi dòng PASS / WARN / FAIL kèm bằng chứng `file:line`.
3. Việc phải làm trước khi merge (nếu có), xếp theo thứ tự cần làm.
4. Doc ngắn cho PR, dưới 150 chữ.

## Nguyên tắc
- **Bằng chứng hơn cảm giác.** Mỗi nhận định ghi `file:line` và nhãn Verified (đã chạy hoặc đã đọc tận nơi) hay Inferred (suy ra). Không có bằng chứng thì không được FAIL.
- **Chỉ đọc.** Không push, không sửa nhánh của PR, không approve hay merge hộ. Mọi thứ ghi ra ngoài (comment lên PR) phải qua `--post` và được user xác nhận.
- **Script lo phần tất định, model lo phần phán xét.** `scripts/dss.py` chỉ gợi ý. Mọi cờ nó bật lên đều phải được đọc lại tận nơi trước khi đưa vào báo cáo.
- **Lỗi đã có trước PR thì không đổ cho PR.** Test đỏ ở cả base lẫn head là nợ cũ: ghi riêng, không tính vào phán quyết.

## Quy trình

### 1. Lấy PR về
```bash
python3 <skill>/scripts/dss.py fetch <target> [--base <nhánh>] [--platform github|gitlab]
```
Script nhận diện GitHub hay GitLab từ URL hoặc remote, kéo `pull/<n>/head` hoặc `merge-requests/<n>/head` về `refs/dss/<id>`, tính merge-base, rồi ghi `diff.patch` và `summary.json` (file đổi, phân loại src/test/doc, commit, cờ lint, lệnh test đoán được). Có `gh`/`glab` thì lấy thêm tiêu đề, mô tả và nhánh đích; không có thì chỉ dùng git.

Đọc kỹ diff và mô tả PR. Viết ra **một câu** nói PR này thay đổi hành vi gì. Nếu không viết nổi câu đó, PR đang làm nhiều việc cùng lúc: ghi WARN ở tiêu chí 5 và đề nghị tách PR.

### 2. Tiêu chí 1: Double work
```bash
python3 <skill>/scripts/dss.py dupes <merge_base> <head> [--me <email của tôi>]
```
- `blocks`: khối code được thêm mà giống code đã có (`exact` là giống nguyên văn, `shape` là cùng cấu trúc nhưng đổi tên biến hoặc literal). `mine: true` nghĩa là đoạn code gốc do tôi viết.
- `same_name_defs`: hàm hoặc class mới trùng tên với thứ đã tồn tại.
- Script không bắt được trùng **ý định** (cùng việc nhưng viết khác hẳn). Với mỗi hàm mới, tự tìm thêm theo động từ và danh từ của nó (`grep -rn "phone\|sdt"`…). Nếu repo dùng **comment-mapping**, chạy thêm `cmap.py find "<mô tả việc PR làm>"`.
- FAIL khi PR viết lại thứ đã có mà không có lý do. Cách sửa: gọi lại hàm cũ, hoặc mở rộng hàm cũ.

### 3. Tiêu chí 4: Tổng quát hay vá đúng case
Đọc từng cờ `case-fix-*`, `swallow-error`, `sleep-retry`, `todo-hack` trong `summary.lint`. Tự hỏi: **ngày mai input khác đi một chút thì bản sửa này còn đúng không?**
- Xác định gốc của vấn đề thuộc tầng nào trong `../generalize-fixed-it/references/root-cause-levels.md` (L1 lỗi đơn lẻ, L2 code lặp, L3 rule cứng, L4 thiếu abstraction, L5 kiến trúc, L6 thiếu quan sát), rồi xem bản sửa có xử lý đúng tầng đó không. Gốc ở L2–L5 mà bản sửa chỉ chạm đúng một chỗ là vá case.
- Dấu hiệu vá case: `if` so sánh với một id, tên khách hàng hay chuỗi cứng; `try/except` nuốt lỗi; `sleep` để né race condition; thêm cờ đặc biệt cho một chỗ gọi.
- FAIL khi PR vá đúng triệu chứng mà gốc vẫn còn và đã thấy rõ gốc. Đề xuất bản sửa ở tầng đúng (gọi **generalize-fixed-it** nếu cần đào sâu).

### 4. Tiêu chí 2: Regression
Dùng worktree riêng, không đụng vào thư mục làm việc của user:
```bash
git worktree add .dss/<id>/head <head> && cd .dss/<id>/head && <lệnh test>
```
- Lệnh test lấy từ `summary.test_cmd_guess`, CLAUDE.md, CI config (`.github/workflows/*`, `.gitlab-ci.yml`) hoặc README. Không chắc thì hỏi.
- Test đỏ ở head thì chạy đúng các test đó ở merge-base (`git worktree add .dss/<id>/base <merge_base>`). Đỏ ở head, xanh ở base: **regression**, FAIL. Đỏ ở cả hai: nợ cũ.
- Đọc thêm cờ `test-skip`, `test-only`, `asserts-removed`, `test-file-deleted`. PR mà làm test xanh bằng cách tắt hoặc xóa test thì FAIL, kể cả khi CI xanh.
- Không chạy được test (thiếu môi trường, cần secret): ghi rõ là **chưa chạy** và hạ độ tin cậy. Tuyệt đối không ghi PASS.
- Xong thì gỡ worktree: `git worktree remove .dss/<id>/head`.

### 5. Tiêu chí 3: Test hành vi
Luôn làm bước này, kể cả khi PR không có test nào. Chi tiết ở `references/behavior-tests.md`.
- Liệt kê các **hành vi** PR thêm hoặc đổi: thứ người gọi, người dùng hay service khác quan sát được.
- Với mỗi test trong PR, làm hai phép thử tưởng tượng. Một: làm hỏng hành vi; test có đỏ không? Hai: giữ nguyên hành vi nhưng viết lại phần ruột; test có còn xanh không? Test đạt cả hai thì giữ. Test chỉ đạt một thì ghi WARN kèm lý do.
- Hành vi chưa có test thì viết sẵn spec Given / When / Then. Spec phải đủ cụ thể để dán vào file test là chạy được, và kết quả mong đợi phải suy từ yêu cầu chứ không chép lại từ output của code.
- FAIL khi hành vi chính của PR không có test nào kiểm được, hoặc test chỉ khóa chặt phần cài đặt (mock helper nội bộ, so snapshot cả object, so đúng chuỗi lỗi mà không ai đọc).

### 6. Tiêu chí 5: Map tính năng và doc ngắn
- Tìm tính năng mà PR thuộc về, theo thứ tự: id CMAP trong diff, issue hoặc ticket trong mô tả, tên nhánh, commit message, spec và plan trong `docs/`, module bị đổi nhiều nhất. Ghi rõ đã map bằng nguồn nào.
- Viết doc dưới 150 chữ (đếm thật): PR làm gì, vì sao, ảnh hưởng tới đâu, cách kiểm tra. Viết bằng lời thường, không quảng cáo; áp dụng phần "Chữ" trong `../anti-slop/references/text-slop.md`.

### 7. Phán quyết
Theo bảng trong `references/rubric.md`. Tóm tắt:
- **BLOCK**: có regression, test bị tắt hoặc xóa để qua CI, lộ secret, mất dữ liệu.
- **CHANGES REQUIRED**: có ít nhất một FAIL ở tiêu chí 1, 3 hoặc 4.
- **MERGE + NITS**: không có FAIL, có WARN.
- **MERGE**: 5/5 PASS và đã chạy test thật.

Ghi `REPORT.md`, in bản tóm tắt. Có `--post` thì cho user xem bản sẽ đăng, chờ đồng ý, rồi mới chạy `gh pr comment <n> -F REPORT.md` hoặc `glab mr note <n> -m "$(cat REPORT.md)"`.

## Chỉ đọc khi cần
- `references/rubric.md`: khi phân vân giữa WARN và FAIL, hoặc giữa hai mức phán quyết.
- `references/behavior-tests.md`: ở bước 5.
- `references/auto-run.md`: khi user muốn skill tự chạy mỗi khi có PR/MR mới (GitHub Actions, GitLab CI, hook cục bộ).

## Phối hợp
- Trước khi kết luận, có thể chạy **anti-slop** trên diff để bắt code thừa, code lặp hay UI kiểu AI. Kết quả của nó chỉ được tính là WARN, không đủ để FAIL.
- Thấy vá case ở tiêu chí 4 thì chuyển sang **generalize-fixed-it**.
- PR lớn hoặc rủi ro cao: dùng **arena** cho 2–3 reviewer độc lập rồi gộp kết quả.
