# Chữ kiểu AI trong comment, doc và UI

Rút gọn và chuyển sang tiếng Việt từ skill `unslop` của pstack (Lauren Tan, MIT). Mã T1, T2… là của skill này, không trùng với số luật gốc.

## Từ ngữ
- **T1. Từ vựng AI.** additionally, crucial, delve, enhance, fostering, intricate, pivotal, showcase, tapestry, testament, underscore, vibrant, robust, seamless, comprehensive, leverage, utilize, facilitate. Tiếng Việt: "đóng vai trò then chốt", "mang tính đột phá", "liền mạch", "toàn diện", "tối ưu hóa trải nghiệm". Cách sửa: từ thường. "use" thay cho "leverage", "dùng" thay cho "tận dụng".
- **T2. Nói vòng thay cho "là".** "serves as", "stands as", "đóng vai trò là". Cách sửa: "là", "có".
- **T3. "Không chỉ X mà còn Y".** Cách sửa: nói thẳng ý chính.
- **T4. Bộ ba gượng ép.** Ép mọi thứ thành nhóm ba. Cách sửa: dùng số lượng thật.
- **T5. Đổi từ đồng nghĩa liên tục.** Cùng một thứ mà gọi bằng ba tên. Cách sửa: chọn một tên và dùng nhất quán. Trong code, điều này còn gây hiểu nhầm là ba thứ khác nhau.
- **T6. Danh từ ẩn dụ trừu tượng.** substrate, vector (với nghĩa "cách"), north star, flywheel, paradigm, "bề mặt API". Cách sửa: từ cụ thể.

## Câu
- **T7. Nói cảm giác thay vì cơ chế.** "Giúp code dễ bảo trì hơn" thì không nói được gì. "Đổi tên cột thì build lỗi" mới nói được điều cụ thể. Cách kiểm: câu này đặt vào README của dự án khác mà vẫn đúng thì nó vô nghĩa với dự án này. Xóa đi.
- **T8. Bị động che chủ thể.** "Request được validate". Cách sửa: "middleware `auth` validate request".
- **T9. Trạng từ đỡ cho động từ yếu.** "chạy rất nhanh", "cải thiện đáng kể". Cách sửa: nêu con số.
- **T10. Rào đón quá mức.** "có thể có khả năng sẽ". Cách sửa: "có thể", hoặc khẳng định luôn.
- **T11. Câu đệm.** "in order to", "it is important to note that", "cần lưu ý rằng", "điều quan trọng là". Cách sửa: xóa phần đệm.
- **T12. Nén quá mức.** Mũi tên, ký hiệu, câu cụt không động từ. "Parse lỗi → exit 2" nên viết thành "Parser gặp ngày sai thì thoát với mã 2 và không ghi gì". Áp dụng cho doc và commit; với comment ngắn trong code thì chấp nhận được.
- **T13. Câu quá dài.** Người đọc phải đọc lại mới hiểu. Cách sửa: tách ra, mỗi câu một ý.

## Định dạng
- **T14. Lạm dụng in đậm.** Mỗi danh từ một lần in đậm. Cách sửa: chỉ in đậm thứ người đọc lướt mà vẫn phải thấy.
- **T15. Danh sách có nhãn lặp lại nội dung.** "**Hiệu năng:** Hiệu năng được cải thiện…". Cách sửa: viết thành văn xuôi.
- **T16. Emoji trang trí** trong heading, bullet, log và commit message. Cách sửa: xóa.
- **T17. Lạm dụng gạch ngang dài (—).** Cách sửa: dùng dấu chấm hoặc dấu phẩy.

## Giọng chatbot
- **T18. Câu xã giao.** "Hy vọng điều này giúp ích!", "Let me know if…", "Great question!". Cách sửa: xóa.
- **T19. Kết luận chung chung.** "Tương lai rất hứa hẹn." Cách sửa: nêu kế hoạch hoặc sự kiện cụ thể, hoặc không cần kết luận.
- **T20. Nguồn mơ hồ.** "Các chuyên gia cho rằng". Cách sửa: nêu nguồn cụ thể, hoặc xóa.

## Riêng cho comment trong code
- Comment chỉ nên trả lời *vì sao*. *Cái gì* và *thế nào* thì code đã nói.
- Docstring nêu hợp đồng: input, output, lỗi ném ra, tác dụng phụ. Không kể lại cách cài đặt.
- Commit message: dòng đầu nói hành vi đổi gì; phần thân nói vì sao. Không viết "Enhanced robustness and improved overall code quality".
