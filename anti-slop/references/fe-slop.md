# FE trông "giống AI"

Giao diện do AI dựng mặc định thường hội tụ về cùng một khuôn. Từng chi tiết riêng lẻ không sai; chúng thành vấn đề khi xuất hiện cùng nhau và không xuất phát từ sản phẩm hay design system của bạn. Câu hỏi để soi: **bỏ logo đi thì màn hình này có phân biệt được với một nghìn trang khác không?**

Mã F1, F2… cố định để trích dẫn.

## Thị giác
- **F1. Gradient tím–xanh–hồng.** `from-purple-500 to-pink-500`, `indigo → violet`, nền gradient toàn trang. Cách sửa: màu phẳng từ token của brand; nếu thật sự cần gradient thì dùng một lần, có chủ đích.
- **F2. Glassmorphism khắp nơi.** `backdrop-blur` cộng nền trắng mờ cho mọi card, navbar, modal. Cách sửa: nền đặc, phân lớp bằng màu nền và viền.
- **F3. Card bo to và đổ bóng to.** `rounded-2xl shadow-xl` cho mọi thứ, `hover:scale-105` cho cả thứ không bấm được. Cách sửa: dùng radius và shadow theo token; hiệu ứng hover chỉ cho phần tử bấm được.
- **F4. Chữ gradient.** `bg-clip-text text-transparent` cho tiêu đề. Cách sửa: chữ màu đặc. Độ tương phản và khả năng đọc quan trọng hơn hiệu ứng.
- **F5. Glow và blob trang trí.** Vòng tròn mờ màu tím sau hero, `shadow-[0_0_40px_…]`. Cách sửa: xóa.
- **F6. Emoji làm icon.** 🚀 ✨ ⚡ trong tiêu đề, nút, danh sách tính năng. Cách sửa: dùng bộ icon của dự án, hoặc không dùng icon.
- **F7. Font mặc định không chủ đích.** Inter hay Poppins vì là mặc định chứ không phải lựa chọn. Cách sửa: dùng font của brand. Nếu chưa có thì font hệ thống, chỉ báo cáo, không tự chọn font mới.

## Bố cục
- **F8. Khuôn landing page.** Hero căn giữa, tiêu đề hai dòng, hai nút "Get started" / "Learn more", tiếp theo là lưới 3 card tính năng có icon, rồi testimonial, rồi pricing 3 cột (cột giữa "Most popular"). Áp vào cả màn hình **ứng dụng** (dashboard, form) là dấu hiệu rõ nhất. Cách sửa: bố cục theo tác vụ của người dùng màn hình đó.
- **F9. Lưới 3 cột cho mọi thứ.** Kể cả khi có 2 hay 5 mục. Cách sửa: số cột theo nội dung thật (cùng tinh thần với "rule of three" bên phần chữ).
- **F10. Mọi thứ căn giữa.** Văn bản dài căn giữa, form căn giữa trên màn hình rộng. Cách sửa: căn trái cho nội dung đọc.
- **F11. Khoảng cách đồng đều vô hồn.** `p-8 gap-8` khắp nơi, không có phân cấp. Cách sửa: khoảng cách theo nhóm nội dung, dùng scale của design system.

## Nội dung
- **F12. Copy kiểu marketing trong app.** "Supercharge your workflow", "Seamlessly", "Unleash", "Nâng tầm trải nghiệm". Cách sửa: nói cái nút làm gì ("Xuất báo cáo CSV").
- **F13. Dữ liệu giả lọt vào production.** Lorem ipsum, "John Doe", số liệu tròn đẹp, avatar placeholder. Cách sửa: dữ liệu thật hoặc empty state thật.
- **F14. Empty, loading và error state chung chung.** "Oops! Something went wrong 😅". Cách sửa: nói cái gì hỏng và người dùng làm gì được.

## Mã nguồn
- **F15. Giá trị cứng bỏ qua token.** `#7c3aed`, `text-[#333]`, `z-[9999]` khi repo đã có theme hay token. Cách sửa: token sẵn có.
- **F16. Component nhân bản.** Ba bản `Card` gần giống nhau ở ba thư mục; nút tự style thay vì dùng `Button` của design system. Cách sửa: dùng component sẵn có.
- **F17. Animation thừa.** `framer-motion` fade-in cho từng phần tử; `transition-all duration-500` cho mọi thứ. Cách sửa: animation có chức năng (phản hồi thao tác, chuyển trạng thái), tôn trọng `prefers-reduced-motion`.
- **F18. Dark mode nửa vời.** Có toggle nhưng một nửa màu cứng không đổi theo. Cách sửa: hoặc làm đủ bằng token, hoặc bỏ toggle.

## Cách kiểm
1. Đọc class và style trong phạm vi, đối chiếu với các mục trên.
2. Tìm design system của repo (`tailwind.config.*` theme, `tokens.*`, `theme.*`, thư mục `components/ui`). Không có thì chỉ báo cáo, không sáng tác style mới.
3. Nếu chạy được app: chụp màn hình và hỏi câu "bỏ logo đi" ở trên. Ảnh chụp đáng tin hơn đọc class.
