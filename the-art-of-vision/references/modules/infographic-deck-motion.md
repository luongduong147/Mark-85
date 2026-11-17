# Module: Infographic, slide, motion

Đi qua cây cầu hẹp trong SKILL.md trước. Có số liệu thì đọc thêm `../chart-choice.md`, và nếu số là số thật thì cả `../metric-definition.md`.

## Infographic và ảnh dài
- **Chốt khoảng cách xem và khung trước.**
  - Lướt trên điện thoại: rộng 1080px, màn đầu (khoảng 1080×1350) phải tự đứng được với tiêu đề, hình chính và con số mạnh nhất.
  - In hoặc màn hình lớn: tính cỡ chữ theo kích thước vật lý và khoảng cách xem.
  - Chèn trong bài viết: rộng theo cột chữ, chữ trong hình không nhỏ hơn chữ thân bài.
- **Dữ liệu là nhân vật chính.** Chỉ dùng số user đưa hoặc kiểm chứng được. Hình minh họa thì ghi "minh họa" lên hình.
- **Hỏi các con số muốn nói quan hệ gì, rồi mới chọn hình thức:**
  - tỷ lệ: diện tích hoặc vật thật theo đúng tỷ lệ;
  - thay đổi: một đường hoặc dòng thời gian;
  - không gian: bản đồ;
  - cấu thành: tách rời một tổng thể;
  - quy mô: một vật rất lớn đặt cạnh một vật quen thuộc làm mốc.
- Một màu chỉ mang một nghĩa. Chú giải đặt ngay trên hình.
- Cỡ chữ cho ảnh 1080px xem trên điện thoại: thân ≥ 36px, nhãn ≥ 28px (tính theo pixel canvas).

## Slide
- Một slide, một ý. Tiêu đề slide là **kết luận** ("Doanh thu Q3 tăng 18% nhờ kênh B2B"), không phải chủ đề ("Doanh thu Q3").
- Canvas 1920×1080. Chữ thân ≥ 24px, nhãn ≥ 16px.
- Nhịp: đổi kiểu bố cục giữa các slide (chữ lớn, hình toàn màn, biểu đồ, so sánh), không lặp lại tiêu đề + 3 gạch đầu dòng.
- Biểu đồ trên slide: bỏ bớt chi tiết so với dashboard, chỉ giữ thứ phục vụ kết luận. Dùng kiểu nhấn mạnh: chuỗi chính có màu, còn lại xám.
- Cổng 3 hướng cho slide: mỗi hướng 2 slide đại diện (bìa và một slide nội dung khó nhất).
- Xuất: HTML → PDF bằng trình duyệt headless; cần PPTX chỉnh sửa được thì dùng skill pptx nếu harness có.

## Motion và video
- Viết **kịch bản phân cảnh** trước: mỗi cảnh ghi thời lượng, hình chính, chuyển động chính và câu chữ trên màn hình. Clip từ 20 giây trở lên thì kịch bản là file cổng bắt buộc.
- Easing: không dùng `linear` cho vật thể; vào chậm ra nhanh khi xuất hiện, vào nhanh ra chậm khi biến mất. Mỗi cảnh chỉ một chuyển động chính, các thứ khác phụ họa.
- Nhịp theo nội dung: cảnh có chữ phải đủ lâu để đọc, khoảng 3 từ mỗi giây.
- Kiểm: chụp các khung hình chính (đầu, giữa, cuối mỗi cảnh) và xem như vòng đánh bóng.
- Xuất MP4/GIF: ghi khung hình bằng trình duyệt headless rồi ghép bằng ffmpeg; báo trước với user về thời gian render.
