# Hiệu năng

**Bạn sở hữu câu chuyện đo đạc.** Mỗi bản sửa gắn với một con số. Đọc code không thay được việc đo.

1. **Đo baseline** bằng một lệnh lặp lại được: trung vị của N lần, ghi cả số lỗi và lượng việc đã làm. Kiểm con số có đo đúng thứ mình nghĩ không (Explain the number).
2. Đặt **điều kiện xong** cho số đo, gồm ngưỡng mục tiêu và số lần thử tối thiểu.
3. Thử theo thứ tự, rẻ trước:
   1. Không làm nữa.
   2. Đừng làm lại.
   3. Làm ít đi.
   4. Làm sau.
   5. Làm lúc không ai nhìn.
   6. Làm đồng thời.
   7. Làm rẻ hơn.
   Đạt mục tiêu thì dừng.
4. **Mỗi lần thử: một thay đổi, một lần đo, giữ hoặc revert.** Ghi vào sổ: `trail.py note hyp "<cơ chế>" --test "<lệnh đo>" --result "<trước→sau>" --verdict kept|reverted`.
5. Gặp vùng không tiến thêm thì đổi loại giả thuyết, đừng dừng. Đúng và đơn giản xếp trên con số.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Giả thuyết | nhiều giả thuyết song song, mỗi cái một worktree | từng cái, ngưỡng ồn đặt trước | từng cái, rẻ nhất trước |
| Báo cáo | baseline → sau, % | thêm khoảng tin cậy, thứ đang giới hạn | baseline → sau, đường dẫn sổ |
