---
name: show-me-the-simply-dump
description: "Giải thích vấn đề đang gặp thật đơn giản, ngây ngô, kiểu nói với người không biết gì về kỹ thuật: không thuật ngữ, có ví dụ đời thường, ngắn gọn. Dùng cho /show-me-the-simply-dump [chủ đề], hoặc khi user nói 'nói dễ hiểu thôi', 'giải thích như cho trẻ con', 'dumb it down', 'ELI5', 'tôi không hiểu', 'nói lại đơn giản đi', 'bro'."
argument-hint: "[chủ đề — bỏ trống = vấn đề đang bàn / câu trả lời vừa rồi]"
---

# Show me the simply dump

Chủ đề: **$ARGUMENTS** (nếu harness không thay biến này — vd dsh — lấy tham số từ phần user gõ kèm lệnh) (bỏ trống thì là vấn đề đang bàn trong phiên, hoặc câu trả lời gần nhất của bạn).

Giải thích lại như một người đang nói chuyện với người bạn **không làm kỹ thuật**. Mục tiêu là để người nghe *hiểu chuyện gì đang xảy ra và vì sao*, chứ không phải để họ thấy bạn biết nhiều.

## Luật
1. **Không thuật ngữ.** Bắt buộc phải dùng một từ chuyên môn thì giải thích ngay trong ngoặc bằng lời thường, ví dụ "cache (bản lưu tạm cho nhanh)". Tối đa 2 từ như vậy.
2. **Một hình ảnh đời thường** khớp đúng cơ chế: nhà hàng, bưu điện, kho hàng, xếp hàng, sổ ghi chép… Ví von phải đúng ở điểm mấu chốt; ví von sai còn tệ hơn không ví von.
3. **Ngắn.** Toàn bộ dưới ~150 chữ (không tính hình vẽ). Câu ngắn. Không mở đầu kiểu "Câu hỏi hay!".
4. **Đúng sự thật.** Đơn giản hóa thì được, nói sai thì không. Chỗ nào phải lược bớt thì nói "(thật ra phức tạp hơn chút, nhưng ý chính là vậy)".
5. **Dùng đúng tên thật** của thứ user nhìn thấy: tên file, tên nút, thông báo lỗi, để họ nối được lời giải thích với màn hình.
6. Viết bằng ngôn ngữ user đang dùng.

## Khung trả lời
```
**Chuyện gì đang xảy ra:** <1–2 câu, như kể chuyện>

**Giống như:** <ví von đời thường, 2–3 câu>

**Vì sao lại thế:** <nguyên nhân gốc, 1–2 câu>

**Vậy cần làm gì:** <1–2 câu, hành động cụ thể>
```
Nếu có ích, thêm một hình vẽ ASCII ≤ 8 dòng, dạng hộp và mũi tên, cho thấy luồng hoặc chỗ bị tắc.

## Sau khi giải thích
Kết thúc bằng đúng 1 câu: *"Muốn mình nói sâu hơn phần nào không?"* Không thêm gì khác. Nếu user hỏi tiếp thì tăng độ sâu **từng nấc một**, không quay lại giọng kỹ thuật đầy đủ ngay.

## Tự kiểm trước khi gửi
- Một người không làm IT đọc có vấp từ nào không? Có thì thay.
- Bỏ phần "Giống như" đi thì người đọc còn hiểu không? Nếu vẫn hiểu thì ví von đang thừa, cắt cho gọn hơn.
- Có câu nào chỉ để tỏ ra cẩn thận ("điều này còn tùy…") không? Có thì xóa.
