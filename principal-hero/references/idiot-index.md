# Idiot index cho phần mềm

Gốc ý tưởng: tỉ lệ giữa giá thành phẩm và giá nguyên liệu thô của nó. Tỉ lệ càng cao thì càng có nhiều "chi phí do cách làm" chứ không phải "chi phí do bản chất".

## Bảng
| Thành phần | Nó làm gì (nguyên tử) | Chi phí thực tế | Chi phí sàn | Tỉ lệ (≈) | Vì sao chênh (Verified / Inferred) | Cần trong bối cảnh ta? |
|---|---|---|---|---|---|---|
| vd: Agent framework X | gọi LLM + chạy tool trong vòng lặp | 40k LOC dep, 12 khái niệm, debug khó | ~300 LOC: while + dispatch tool + giới hạn context | ~100× | đa provider, tracing, memory plugin (Verified: src/…) | chỉ cần tracing |

## Các trục chi phí
- **Khái niệm**: số khái niệm người mới phải học để sửa một lỗi.
- **Code / dependency**: LOC tự viết, số dependency trực tiếp và bắc cầu, bề mặt API.
- **Vận hành**: số service hay process phải chạy, giám sát, nâng cấp.
- **Runtime**: độ trễ, bộ nhớ, token, tiền trên mỗi request.
- **Thay đổi**: số file phải chạm khi thêm một tính năng điển hình.
- **Lock-in**: chi phí rời bỏ sau 1 năm.

## Đọc tỉ lệ
- < 3×: hợp lý, đừng phí công.
- 3–20×: đào "vì sao". Thường là có tính năng ta không dùng tới.
- > 20×: hoặc có một bài học đắt giá ẩn bên dưới (Chesterton), hoặc là cơ hội lớn để xóa hay tự xây bản tối thiểu. Phải biết đó là trường hợp nào trước khi khuyến nghị.
