# Đánh giá PR/MR

1. `/dont-ship-shit <PR|MR>`: 5 tiêu chí, có phán quyết.
2. `anti-slop` trên diff. Diff chạm tới auth, dữ liệu người dùng hay quyền thì thêm `security-review`.
3. Gộp lại thành một phán quyết duy nhất. Lỗi có từ trước PR thì ghi riêng, không tính vào PR.
4. Đăng comment lên PR **chỉ khi user đồng ý**.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Test | `--quick` | chạy đủ regression | test hẹp vùng bị chạm, full suite chạy ngầm |
