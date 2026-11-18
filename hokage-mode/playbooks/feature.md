# Tính năng

**Bạn sở hữu thiết kế.** Phần viết code giao cho agent. Bạn giữ vai dẫn dắt.

1. Lần theo phần hệ thống bị ảnh hưởng. Gọi tên kiểu dữ liệu và cấu trúc tổ chức (state machine, bảng, kiểu dữ liệu) **trước** khi viết logic.
2. Thiết kế còn tranh cãi thì dùng `arena`. Đã rõ thì đi tiếp.
3. **Mốc thông lượng**, ghi 4 dòng vào sổ. Dòng nào không áp dụng thì ghi `n/a: <lý do>`:
   - Bước chặn: cái gì phải xong trước khi chia việc.
   - Luồng độc lập: file, service hay tầng nào tách rời được thì chạy song song.
   - Trạng thái ghi chung: tách nơi ghi trước, chỉ tuần tự hóa khi có bất biến thật.
   - Cách chia nhỏ nhất an toàn: nếu một agent là tốt nhất, nói vì sao.
4. **Giao việc** cho agent kèm phạm vi cụ thể: đường dẫn file, kiểu dữ liệu đã chọn, tiêu chí xong. Ghi song song thì mỗi con một worktree.
5. **Kiểm trên sản phẩm thật**: chạy app, chụp màn hình, gọi API.
6. `anti-slop` trên diff → `dont-ship-shit` (tự review) → commit nhỏ, đúng thứ tự.
7. Mở PR chỉ khi user yêu cầu, hoặc khi việc đó đã nằm trong nhiệm vụ.

| | Shinobi | Sage | Bruiser |
|---|---|---|---|
| Thiết kế | chốt nhanh 1 shape, không arena | arena khi có ≥ 2 shape hợp lý | shape đơn giản nhất chạy được |
| Giao việc | chia tối đa theo đường nối, `sonnet` | 2–4 luồng, verifier khác model | tuần tự từng đơn vị, `haiku` → `sonnet` |
| Bước 6 | `anti-slop` chỉ MUST KILL, `dont-ship-shit --quick` | đầy đủ | chỉ trên diff |
