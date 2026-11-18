# Refactor (đổi cấu trúc, giữ hành vi)

**Bạn sở hữu hợp đồng hành vi.** Cấu trúc thay đổi, hành vi thì không. Phát hiện bug hay thiếu tính năng thì tách ra thành việc riêng.

1. `refactor-or-nothing`: có đáng làm không? Câu trả lời là LEAVE thì dừng ở đây.
2. **Ghim hành vi** trước khi động vào cấu trúc: viết test đặc tả, snapshot, hoặc script so sánh đầu ra cũ với mới. Type check và lint không tính là ghim.
3. Gọi tên shape đích. Bản refactor phải xóa được nhánh rẽ hoặc trạng thái sai, không được thêm lớp gián tiếp.
4. **Xóa trước**: code chết, wrapper chỉ có một chỗ gọi, validator thừa (`anti-slop --fix`).
5. Đi từng bước nhỏ, mỗi bước giữ test ghim xanh. Đổi API thì chuyển hết chỗ gọi và xóa API cũ trong cùng một đợt. Đổi tên thì grep cả chuỗi và tài liệu.
6. Chứng minh hành vi không đổi trên sản phẩm thật, rồi đo xem người đọc có đỡ vất vả hơn không. Không đỡ hơn thì revert.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Ghim | test hẹp trên vùng chạm tới | ghim đầy đủ + script so sánh tương đương | test hẹp, chạy sau mỗi bước |
| Đổi hàng loạt | codemod + bầy `kage-bunshin` chia theo file | codemod, kiểm mẫu | codemod chạy một lần, không sửa tay |
