# Mổ xẻ một repo tham khảo

1. **Lấy về an toàn**: `git clone --depth 50 <url>` vào một thư mục mới, trống, trong scratchpad. Không chạy install script hay build tool từ bên trong repo lạ trước khi đã đọc chúng. Python đọc dữ liệu từ repo thì chạy với `-I`.
2. **Bản đồ**: ngôn ngữ, entrypoint (`main`, `bin`, `cli`, `server`), các module cấp 1, manifest dependency, thư mục test, CI.
3. **Luồng chính**: theo một request hoặc tác vụ điển hình từ entrypoint tới đầu ra. Ghi lại chuỗi `file:line`. Đây là "xương sống". Phần còn lại là thịt quanh xương.
4. **Kiểu dữ liệu cốt lõi**: những struct, type, schema mà mọi thứ xoay quanh. Hiểu được chúng là hiểu 70% thiết kế.
5. **Lịch sử**: `git log --stat` của các file lõi, những issue hoặc PR lớn (`gh issue list --label`, `gh pr view`), CHANGELOG. Tìm các lần **đổi hướng**, vì mỗi lần như vậy là một bài học.
6. **Sẹo**: tìm comment `HACK`, `workaround`, `because`, `don't`, những đoạn retry hay timeout lạ, những test có tên kể chuyện. Đây là kiến thức mà README không viết.
7. **Đo**: chạy được thì chạy ví dụ hoặc benchmark của chính họ trên máy mình. Không chạy được thì ghi rõ là chưa kiểm chứng.
8. **Tóm tắt** trong ≤ 15 dòng: xương sống, kiểu dữ liệu cốt lõi, 3 quyết định thiết kế quan trọng nhất kèm lý do (có trích dẫn), 3 thứ đáng lấy, 3 thứ không cần.
