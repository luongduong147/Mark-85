# Module: Landing page, website, UI app

Đi qua cây cầu hẹp trong SKILL.md trước, rồi làm theo sổ tay này.

## A. Landing page và website

### Màn hình đầu tiên
Mở bằng thứ đặc trưng nhất trong thế giới của đề tài, ở dạng hợp nhất với nó: một câu tiêu đề, một tấm ảnh, một đoạn chuyển động, một demo chơi được, một khoảnh khắc tương tác.

"Số to + nhãn nhỏ + một hàng số phụ + gradient điểm xuyết" là câu trả lời mặc định cho màn hình đầu, chỉ dùng khi nó thật sự hợp nhất. Bộ khuôn "hero lớn + 3 cột tính năng + đánh giá khách hàng + nút CTA" cũng vậy.

### Mỗi màn hình phía dưới cũng phải được thiết kế
Lỗi phổ biến nhất của landing page: màn đầu có thiết kế, còn từ đó trở xuống toàn "tiêu đề nhỏ + ba card giống nhau". Với từng khối nội dung, hỏi: hình thức nào hợp nhất với nó? Biểu đồ, demo kéo thả được, chữ cỡ lớn, ảnh giao diện sản phẩm, dòng thời gian… chứ không mặc định nhét vào card.

**Sản phẩm phải nhìn thấy được.** Giới thiệu app, công cụ hay phần cứng thì trên trang phải có chính sản phẩm đó: có ảnh chụp thì dùng ảnh chụp, không có thì dựng lại giao diện từ nội dung thật user cung cấp. Cơ chế cốt lõi mà làm thành được demo nhỏ (kéo thanh trượt để thấy giá thay đổi) thì đó thường là màn hình hay nhất trang.

### Thứ tự làm
1. Cổng 3 hướng: mỗi hướng một file HTML hoàn chỉnh, kèm ảnh màn đầu và ảnh cả trang.
2. Chọn xong thì viết danh sách giả định và khung cấu trúc cho user xem, rồi mới điền component.
3. Cấu trúc và nhịp đã ổn mới thêm tinh chỉnh (màu, cỡ chữ, nội dung).
4. Vòng đánh bóng ít nhất 2 lần, xem cả desktop lẫn mobile.

## B. UI ứng dụng và prototype

UI app khác landing page: người dùng **làm việc** trên nó hằng ngày chứ không chỉ đọc lướt một lần.
- **Bắt đầu từ tác vụ**, không bắt đầu từ bố cục. Liệt kê 3–5 tác vụ chính, đi từng luồng từ điểm vào tới khi xong, rồi mới vẽ màn hình.
- **Mật độ theo người dùng**: công cụ nội bộ cho người dùng chuyên sâu cần dày thông tin (bảng, phím tắt). App cho người dùng phổ thông thì cần thoáng và có hướng dẫn.
- **Đủ trạng thái**: rỗng, đang tải, lỗi, không có quyền, dữ liệu quá dài, dữ liệu rất ít. Thiết kế mỗi trạng thái như một màn hình thật.
- **Tương tác phải bấm được thật**: điều hướng, tab, mở rộng, form và trạng thái validate của form. Console không có lỗi.
- **Theo nền tảng**: iOS, Android và desktop có quy ước riêng (điều hướng, vị trí nút chính, cử chỉ). Đặt mockup vào khung thiết bị khi trình bày.
- **Dùng component của design system.** Không có thì giữ một bộ token tối thiểu (màu, khoảng cách, bo góc, chữ) và dùng nhất quán.

## Quy tắc cứng (áp dụng cho cả A và B)
- Chữ thân ≥ 14px (mobile 16px), vùng bấm ≥ 44×44px, tương phản chữ thân ≥ 4.5:1.
- Responsive: ít nhất kiểm ở 1440 và 375 (`shot.py --viewports 1440x900,375x812`).
- Không bịa số liệu, đánh giá hay tường logo; không có thì để chỗ trống trung thực hoặc hỏi user.
- Chuyển động: một màn tải trang được dàn dựng một lần tốt hơn mọi khối đều fade-up. Chuyển động phản hồi thao tác của người dùng (mở rộng, xác nhận) mới là chuyển động tốt. Tôn trọng `prefers-reduced-motion`.
- Ảnh và logo khi giao một file đơn lẻ thì nhúng base64. File > 1000 dòng thì tách component.
- Code đã có framework (React/Vue/Svelte) thì làm trong framework đó. HTML tĩnh chỉ dùng cho bản nháp và mockup.
