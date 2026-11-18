# Công thức bầy đàn

Mỗi công thức ghi:
- **Trục chia**: chia việc theo cái gì.
- **N**: số phân thân gợi ý.
- **Công cụ**: công cụ phân thân cần.
- **Phát hiện**: mỗi phát hiện chứa gì, và `key` dùng để gộp trùng.

Model mặc định là haiku. Nâng lên sonnet khi có ghi rõ.

## 1. Thu thập thông tin / web search số lượng lớn
- **Trục chia**: theo câu hỏi con hoặc theo nhóm truy vấn, không theo từ khóa lẻ. Orchestrator tách câu hỏi lớn thành 3–8 câu hỏi con. Mỗi phân thân nhận 1 câu hỏi con và 5–10 truy vấn gợi ý, được tự mở rộng thêm.
- **N**: 3–8.
- **Công cụ**: WebSearch, WebFetch. Không có công cụ Write.
- **Phát hiện**: `{key: <url chuẩn hóa>, claim, quote (≤ 2 câu, nguyên văn), url, date, confidence}`.
  - Mỗi claim phải có trích dẫn nguyên văn và URL.
  - Không có nguồn thì không ghi.
- **Orchestrator**:
  - gộp theo URL rồi theo claim;
  - đánh dấu các claim mâu thuẫn giữa các phân thân;
  - mở lại nguồn của mọi claim đưa vào kết luận.

## 2. Rà soát codebase toàn cục
- **Trục chia**: `kage.py shard --n N`, chia theo số dòng và giữ các file cùng thư mục chung một phần.
  - Muốn soi chéo thì cho 2 phân thân cùng đọc một phần với 2 góc nhìn khác nhau, vd bảo mật và hiệu năng.
  - Chia theo góc nhìn tốt hơn chia đôi file khi repo nhỏ mà cần nhiều loại lỗi.
- **N**: khoảng tổng số dòng chia 3000, tối đa 8.
- **Công cụ**: Read, Grep, Glob. Chỉ đọc, trừ khi việc là sửa.
- **Phát hiện**: `{key: "<file>:<line>:<loại>", file, line, kind, severity, evidence (đoạn code ≤ 5 dòng), why}`.
- **Phân thân sửa code** (vd đổi API hàng loạt): mỗi con commit trên nhánh `kage/<run>/NN` của mình. Orchestrator đọc diff từng nhánh rồi cherry-pick. Chia sao cho hai con không bao giờ sửa cùng một file.

## 3. Stress test như người dùng thật (web)
- **Trục chia**: theo persona và hành trình. Mỗi phân thân là một người dùng có tính cách, mục tiêu và thiết bị riêng. Ví dụ:
  - khách mới trên mobile 375px, mạng chậm;
  - người dùng quen tay, thao tác nhanh, mở nhiều tab;
  - người gõ sai và bấm back liên tục;
  - người dùng trình đọc màn hình (chỉ dùng bàn phím);
  - người nhập dữ liệu biên (emoji, chuỗi rất dài, ký tự có dấu, số âm).
- **N**: 4–10 persona. Tải lớn hơn thì dùng công cụ tải chuyên dụng (k6, locust) với giới hạn tốc độ, không dùng LLM.
- **Công cụ**:
  - Playwright, viết script Python hoặc Node trong worktree của mình;
  - hoặc Chrome DevTools: `--remote-debugging-port=$((KAGE_PORT+1000))` cùng `--user-data-dir=$KAGE_PROFILE`.
  - Mỗi con một hồ sơ trình duyệt riêng, không dùng chung cookie.
- **Nhịp như người**: có thời gian đọc, gõ từng phím, cuộn, có do dự. Mục đích là tìm lỗi UX và lỗi trạng thái mà người thật sẽ gặp, không phải qua mặt hệ thống chống bot.
- **Phát hiện**: `{key: "<trang>:<loại>", persona, step, expected, actual, screenshot, console_errors, network_failures, repro (các bước)}`.
- **Bắt buộc**: chạy trên môi trường của user (local hoặc staging). Đụng production phải có phạm vi trong rules-of-engagement.

## 4. Tìm asset theo mô tả
- **Trục chia**: theo asset (mỗi con tìm 1–3 asset), hoặc theo nguồn (Unsplash, Wikimedia, kho icon, repo nội bộ).
- **N**: bằng số asset, tối đa 8.
- **Công cụ**: WebSearch, WebFetch, Bash (curl để tải về `assets/` trong worktree).
- **Phát hiện**: `{key: <url>, asset_for, url, license, author, resolution, file (đường dẫn đã tải), match_note}`.
  - Không rõ giấy phép thì ghi `license: unknown` và không đề xuất dùng.
- **Orchestrator**: xem từng ảnh trước khi đưa cho user, chọn 1 trong các ứng viên cho mỗi asset, rồi chép vào repo của user.

## 5. Gọi dịch vụ ngoài hàng loạt
- **Trục chia**: theo endpoint hoặc theo lô dữ liệu đầu vào. Mỗi phân thân có giới hạn tốc độ riêng, và **tổng tốc độ của cả bầy** không vượt giới hạn của dịch vụ.
- **N**: thường 2–5. Giới hạn tốc độ của dịch vụ mới là nút cổ chai, thêm phân thân không nhanh hơn.
- **Công cụ**: Bash (curl/httpie), hoặc script trong worktree. Khóa API lấy từ biến môi trường, không đưa vào brief.
- **Phát hiện**: `{key: "<endpoint>:<input-id>", status, latency_ms, error, sample_response (đã cắt bớt, đã che dữ liệu nhạy cảm)}`.
- **Idempotent**: gọi có ghi dữ liệu (POST tạo đơn, gửi tin nhắn) thì phải có xác nhận của user và có cách hoàn tác.

## 6. Pentest (trong phạm vi được phép)
- **Trục chia**: theo bề mặt tấn công:
  - xác thực và phiên;
  - phân quyền (IDOR, leo quyền);
  - nhập liệu (injection, XSS);
  - cấu hình (header, CORS, TLS, lộ file);
  - logic nghiệp vụ;
  - phụ thuộc (CVE).
- **N**: 4–6. Phần logic nghiệp vụ giao cho sonnet.
- **Công cụ**: Read, Grep để soát mã nguồn; Bash (curl, script Python); Playwright. Công cụ quét chỉ dùng khi phạm vi cho phép.
- **Phát hiện**: `{key: "<endpoint|file>:<CWE>", cwe, severity (CVSS ước lượng), target, request/response tối thiểu để tái hiện, impact, fix}`.
- **Bắt buộc**: phạm vi viết ra trong brief (host, đường dẫn, tài khoản test, khung giờ).
  - Không DoS, không đọc hay xuất dữ liệu thật quá mức cần để chứng minh.
  - Không duy trì truy cập, không thử lên hệ thống ngoài phạm vi.
  - Phát hiện lỗ hổng nghiêm trọng thì dừng phần đó và báo ngay.

## 7. Hành vi như người dùng thật và captcha
- Trên hệ thống của user:
  - dùng khóa test của nhà cung cấp captcha (reCAPTCHA, hCaptcha và Turnstile đều có site key test luôn trả về thành công);
  - hoặc cờ tắt captcha ở môi trường test;
  - hoặc tài khoản test có allowlist.
- Ghi rõ trong brief cách nào đang được dùng.
- Trên site của người khác: phân thân gặp captcha, trang xác minh hay rate limit thì **dừng và báo `blocked`**. Không giải captcha, không xoay IP, không giả dấu vân tay trình duyệt để lách.
- Việc thật sự cần người thì trả về cho user làm tay, rồi phân thân tiếp tục từ trạng thái đó (vd user đăng nhập và lưu `storage_state`).

## 8. Giao việc riêng (orchestrator giao từng việc khác loại)
Ví dụ: một phân thân viết test, một con cập nhật doc, một con tìm chỗ gọi API cũ.
- Mỗi brief viết riêng, có thể khác model và khác công cụ.
- Vẫn dùng chung khuôn JSON ở cuối brief để `collect` gom được.
- Việc phụ thuộc nhau thì xếp thành đợt: đợt 2 chỉ spawn khi đợt 1 đã gom và kiểm xong.

## Chọn N nhanh
| Việc | N |
|---|---|
| Search / nghiên cứu | số câu hỏi con (3–8) |
| Quét code | tổng số dòng / 3000, tối đa 8 |
| Persona web | 4–10 |
| Dịch vụ ngoài | do rate limit quyết định (2–5) |
| Pentest | số bề mặt tấn công (4–6) |
