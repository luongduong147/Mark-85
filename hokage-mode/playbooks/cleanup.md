# Dọn dẹp (cuối mọi nhiệm vụ)

1. Hủy mọi agent còn chạy (`TaskStop`). Với mỗi bầy phân thân: `kage.py down --run <id>`.
2. Commit những gì là sản phẩm của nhiệm vụ (khi nhiệm vụ có yêu cầu commit). Thứ cần giữ mà chưa commit thì đánh dấu `--keep`.
3. `trail.py sweep` để xem danh sách. Đọc kỹ, rồi `trail.py sweep --yes` cùng cờ của chế độ.
   - Bị dọn: file và thư mục **mới** không phải doc, worktree mới, nhánh mới, tiến trình mới đang nghe cổng.
   - Không bao giờ bị đụng: file đã track có thay đổi chưa commit (chỉ cảnh báo), mọi thứ có từ trước lúc `start`.
4. Kiểm cuối:
   - `git status` = lúc bắt đầu + sản phẩm;
   - `git worktree list` chỉ còn worktree chính;
   - `ss -ltnp` không còn cổng do nhiệm vụ mở.
5. `trail.py end`.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Cờ sweep | `--yes --purge` (thùng rác xóa ngay) | `--yes` (thùng rác giữ 7 ngày) | `--yes` cuối mỗi đợt |
