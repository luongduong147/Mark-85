# Tín hiệu cần săn khi mining

## Quy trình (ứng viên cho workflow skill)
- User dẫn agent qua cùng một chuỗi bước ở ≥2 phiên, ví dụ "đọc log → tìm gốc → viết test → sửa → báo cáo".
- User gõ prompt dài gần giống nhau nhiều lần, tức là đang tự làm template bằng tay.
- User đặt tên cho quy trình ("chạy factory", "stress test", "review kiểu X").
- Đầu ra có định dạng cố định mà user hay yêu cầu: file `*_REPORT.md`, bảng, file xlsx test case.

## Sửa lưng (giá trị cao nhất)
- "không", "sai rồi", "đừng", "tôi đã bảo", "làm lại", "ngắn thôi", "giải thích đơn giản hơn".
- User tự làm lại phần agent vừa làm.
- User từ chối một tool call. Ghi lại tool nào và lý do nếu có.
→ Mỗi lần sửa lưng là một luật phòng ngừa. Ghi lại cả **lý do**.

## Sở thích phản hồi
- Ngôn ngữ (tiếng Việt, giữ thuật ngữ tiếng Anh), độ dài, định dạng (bảng hay đoạn văn), mức chi tiết.
- Khi nào muốn được hỏi, khi nào muốn agent cứ làm.

## Tiêu chí "xong"
- User chấp nhận khi nào: có test pass, có số liệu, có báo cáo, có demo chạy thật?
- User hay hỏi lại điều gì sau khi agent báo xong? Đó chính là thứ cần có sẵn trong bàn giao.

## Công cụ & môi trường
- Lệnh, script, MCP, CLI dùng lặp lại; model ưa dùng cho từng loại việc.
- Đường dẫn, repo, thư mục output quen thuộc.
- Việc "mỗi khi X thì Y" là ứng viên cho hook.

## Bỏ qua
- Câu chào, câu hỏi một lần, nội dung nghiệp vụ riêng của một task (trừ khi lặp lại).
- Thông tin nhạy cảm: key, mật khẩu, dữ liệu khách hàng, nội dung email.
