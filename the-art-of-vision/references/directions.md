# Cổng 3 hướng

Chất lượng thiết kế phụ thuộc vào độ rộng của khám phá: đã cân nhắc bao nhiêu phương án và loại bỏ bao nhiêu. Ứng viên thì nhiều, thứ giao thì ít.

## Ba cách nghĩ, mỗi cách 2 ứng viên (tổng 6)
1. **Nhà thiết kế giỏi nhất**: nếu ngân sách không giới hạn, ai là người hợp nhất với đề tài này? Nghĩ bằng cách của họ, làm lại từ đầu.
2. **Tác phẩm thật làm mốc**: tìm tác phẩm xuất sắc đã được kiểm chứng trong cùng chất liệu (dashboard của công ty làm tốt việc này, landing page đoạt giải). Chụp lại và xem tận mắt trước khi mượn, rồi rút ra 3 quy tắc ngôn ngữ thiết kế của nó. Mượn quy tắc, không chép bề mặt.
3. **Vòng quay phong cách**: chọn ngẫu nhiên một phong cách mà bạn ít dùng (Swiss, editorial, brutalist, bản đồ kỹ thuật, tạp chí in, giao diện thiết bị đo…), rồi áp nó một cách nghiêm túc vào đề tài.

## Thẻ hướng
Viết cho mỗi ứng viên theo `templates/direction-card.md`: một câu định vị, chất liệu chính, bảng màu, cặp font, nguyên tắc bố cục, mượn gì từ đâu. Thẻ thì rẻ, còn làm lại một hướng chỉ khác lớp sơn thì đắt.

## Từ 6 xuống 3
1. Vẽ 6 ứng viên thành một trang thumbnail. Mỗi ô là màn hình quan trọng nhất của ứng viên đó, với tiêu đề thật, màu thật và chất liệu chính nhìn thấy được, không phải khối màu giữ chỗ.
2. Chọn 3 ô **mạnh nhất và khác nhau nhất**. Ba hướng không được cùng một họ ngoại hình (ví dụ cả ba đều nền tối một điểm nhấn).
3. Trong 3 hướng, nhiều nhất một hướng được "làm quá tay" (biến cả trang thành đạo cụ, ẩn dụ phủ toàn bộ). Kiểm tra: bỏ thủ pháp đó đi mà thông tin rõ hơn thì nó đang quá tay.
4. Làm 3 hướng thành bản đầy đủ, mỗi hướng qua 1 vòng đánh bóng, rồi đưa cả 3 bản đầy đủ cùng 3 thumbnail dự bị cho user.

## Hình thức bản nháp theo chất liệu
| Chất liệu | Mỗi hướng đưa |
|---|---|
| Landing page, web | 1 file HTML hoàn chỉnh + ảnh màn đầu + ảnh cả trang |
| UI app | 2–3 màn hình của luồng chính, bấm được |
| Dashboard | 1 màn hình đầy đủ với metric đã chốt (số thật hoặc ô "chưa có dữ liệu") |
| Infographic | 1 file hoàn chỉnh, ảnh dài theo chiều rộng đích |
| Slide | 2 slide đại diện |
| Motion | 1 bảng hướng: khung hình chính đã render, bảng màu, câu định vị |
| 3D | 1 cảnh dựng được, kèm ảnh 3 góc |

## Khi đưa ra
- Đưa xong thì **dừng lượt**, chờ user chọn (kể cả khi đang chạy không có người giám sát).
- User có thể ghép ("bố cục của A với màu của C"). Ghi nguyên văn câu đó vào `direction-approved.md`.
- Từ khóa phong cách (ví dụ "kiểu Apple") chỉ thu hẹp không gian diễn giải, không lấy đi quyền chọn: vẫn đưa 3 cách diễn giải khác nhau trong ngữ cảnh đó.
