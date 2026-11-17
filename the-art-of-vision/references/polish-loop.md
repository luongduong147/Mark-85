# Vòng đánh bóng: xem, bắt lỗi, sửa, xem lại

Bản đầu tiên chỉ là bản nháp. Khác biệt lớn nhất giữa nhà thiết kế và người viết code nằm ở đây: làm xong thì ngồi xem lại, thấy chỗ sai, sửa, rồi xem tiếp.

## Cách xem
```bash
python3 <skill>/scripts/shot.py <file.html|URL> --viewports 1440x900,375x812
```
Mở **từng ảnh gốc**, đừng xem ảnh cả trang đã thu nhỏ: thu nhỏ thì chữ và khoảng cách nhòe hết, không thấy lỗi. Slide thì xem từng slide. Motion thì xem các khung hình chính. Dashboard thì xem thêm trạng thái rỗng, đang tải và lỗi.

## Chín câu hỏi cho mỗi vòng
Ghi **3 chỗ tệ nhất** vào `polish-log.md`, cụ thể tới màn hình nào, phần tử nào, sai thế nào.
1. **Ba giây đầu**: người chưa từng thấy dự án có hiểu trong 3 giây đây là gì, dành cho ai không? Thứ đặc trưng của đề tài có nằm trong cái nhìn đầu tiên không?
2. **Chất liệu chính**: chất liệu ghi trong thẻ hướng đã có mặt chưa? Ảnh bắt buộc theo nội dung có đủ không?
3. **Mỗi màn hình có điểm dừng**: cuộn xuống, mỗi màn có một thứ khiến người xem dừng lại, hay "tiêu đề + ba card" lặp tới cuối?
4. **Phân cấp**: nheo mắt nhìn từng màn, thứ nổi lên đầu tiên có phải thứ quan trọng nhất không?
5. **Tay nghề**: căn lề, nhịp khoảng cách, chữ mồ côi cuối dòng, ngắt dòng xấu, tràn, ảnh vỡ, phần tử lạc tông.
6. **Mobile**: hỏi lại các câu trên ở màn hẹp. Không phải "không vỡ" là đủ, mà phải trông như được thiết kế cho mobile.
7. **Đối chiếu thẻ hướng**: đặt ảnh cạnh thẻ hướng và ảnh tham chiếu. Các quy tắc đã mượn có được thực hiện không? Lệch ở đâu?
8. **Bớt một thứ**: bỏ thứ gì đi thì màn này tốt hơn?
9. **Số liệu** (khi có dữ liệu): mỗi số có đơn vị, mốc so sánh và độ tươi không? Có biểu đồ nào vi phạm `chart-choice.md` không? Số có khớp với truy vấn kiểm chứng không?

## Sửa gì
Mỗi vòng chỉ sửa 3 chỗ tệ nhất, rồi chụp lại. Sửa chục chỗ một lúc thì không biết thay đổi nào có tác dụng, lại dễ làm hỏng chỗ đang tốt. Sửa phần cấu trúc trước (màn đầu không đứng được, thiếu chất liệu chính, cả màn tầm thường), tay nghề sau.

Một màn xem thế nào cũng tầm thường thì đừng vá: đập đi, đổi cách tổ chức thông tin. Trước khi làm lại, tự hỏi: một studio hàng đầu nhận dự án này sẽ dành thêm 3 ngày cho màn này để làm gì?

## Bao nhiêu vòng
| Giai đoạn | Số vòng |
|---|---|
| Bản nháp của mỗi hướng | 1 |
| Bản chính thức | Ít nhất 2; dừng khi xem kỹ không còn 3 chỗ đáng sửa (thường 3–5) |
| User đang gấp | 1, và nói rõ khi giao là chỉ đánh bóng 1 vòng |

Tới vòng 5 mà vẫn đang sửa lớn thì vấn đề nằm ở hướng hoặc cấu trúc, không ở đánh bóng. Dừng lại, báo user những gì thấy và đưa 2 cách sửa để chọn.

## Chế độ `--critique`
Chấm thiết kế có sẵn theo chín câu trên, mỗi câu từ 0 tới 3 điểm, kèm bằng chứng là ảnh chụp và vị trí. Kết luận bằng 3 việc đáng làm nhất, xếp theo tác động. Không sửa file khi user chưa yêu cầu.
