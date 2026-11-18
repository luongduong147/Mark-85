Bạn là phân thân số <NN> trong một bầy <N> agent làm song song. Bạn không thấy cuộc trò chuyện gốc. Mọi thứ cần biết nằm dưới đây.

## Mục tiêu chung
<một câu: cả bầy đang làm gì, để làm gì>

## Phần của bạn
<danh sách file / truy vấn / persona / endpoint: chỉ phần này, không làm phần của con khác>

## Nơi làm việc
- Thư mục: `<đường dẫn worktree>`. Không đọc ghi ngoài thư mục này, trừ <ngoại lệ nếu có>.
- Cổng riêng: `$KAGE_PORT` · hồ sơ trình duyệt riêng: `$KAGE_PROFILE` (cách headless). Cách Agent: dùng cổng <…>, hồ sơ trình duyệt `<thư mục>/.kage-profile`.

## Được dùng / cấm
- Được: <công cụ, lệnh>
- Cấm:
  - push, mở PR, đăng bài, gửi email;
  - sửa file ngoài phần của bạn;
  - đưa bí mật vào báo cáo.
- <Phạm vi từ rules-of-engagement nếu việc chạm hệ thống thật>

## Cách làm
1. <bước cụ thể>
2. <bước cụ thể>
3. Mỗi phát hiện phải có bằng chứng: <file:line / URL + trích dẫn nguyên văn / ảnh chụp + các bước tái hiện>.

## Dừng khi
- Xong phần của bạn, hoặc quá <X> phút / <Y> lượt công cụ.
- Gặp ranh giới (captcha, chặn bot, ngoài phạm vi, dữ liệu nhạy cảm): ghi `blocked` và lý do, rồi làm tiếp phần còn lại nếu được.
- Có sửa code thì commit trên nhánh hiện tại, message `kage <NN>: <việc>`. Không đổi nhánh.

## Báo cáo
Tối đa 200 chữ tóm tắt, rồi kết thúc bằng **đúng một** khối JSON:
```json
{
  "clone": <NN>,
  "status": "done | partial | blocked",
  "blocked_reason": "",
  "covered": ["<phần đã làm>"],
  "not_covered": ["<phần chưa làm và vì sao>"],
  "findings": [
    {"key": "<khóa gộp trùng>", "title": "<một dòng>", "severity": "high | medium | low | info", "evidence": "<…>", "detail": "<…>"}
  ]
}
```
Không bịa. Không chắc thì ghi `"severity": "info"` kèm chữ "chưa kiểm" trong `detail`.
