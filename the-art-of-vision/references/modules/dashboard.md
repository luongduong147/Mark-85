# Module: Dashboard / BI

Vai dẫn: **BI Developer**. Dashboard không phải là trang trưng biểu đồ. Nó là công cụ ra quyết định. Mỗi ô trên màn hình phải trả lời được: **ai nhìn vào nó, để quyết định việc gì?**

Đi qua cây cầu hẹp trong SKILL.md, rồi làm theo thứ tự dưới đây. **Không vẽ gì trước khi xong bước 3.**

## 1. Định nghĩa metric
Trước tiên, hỏi (hoặc suy ra từ brief rồi xác nhận lại):
- **Người dùng dashboard là ai?** Ví dụ: CEO xem tuần một lần, ops xem mỗi 5 phút, PM xem sau mỗi release.
- **Họ đưa ra quyết định gì?** Mỗi quyết định thì cần metric nào để ra quyết định đó?
- **Tần suất xem và độ tươi cần thiết?** Real-time, hằng giờ hay hằng ngày.

Sau đó dựng cây metric:
- **Metric chính** (1, nhiều nhất 2): con số mà dashboard mở đầu bằng nó.
- **Metric dẫn dắt**: những thứ đẩy metric chính lên hoặc kéo xuống, có thể hành động được.
- **Metric bảo vệ (guardrail)**: những thứ không được xấu đi khi tối ưu metric chính, ví dụ tỷ lệ hoàn tiền hay độ trễ.
- **Metric chẩn đoán**: chỉ xem khi có gì bất thường, nên đặt ở tầng drill-down chứ không đặt ở màn hình đầu.

Viết mỗi metric thành một thẻ trong `metric-spec.md` (khung ở `templates/metric-spec.md`). Quy tắc viết thẻ và các bẫy hay gặp: `../metric-definition.md`.

Quá 7–9 metric ở màn hình đầu là dấu hiệu chưa chọn được. Dồn bớt xuống drill-down.

## 2. Kiểm tra đã có bộ đếm/đo chưa
Với mỗi metric trong thẻ, tìm nguồn:
```bash
python3 <skill>/scripts/instrument_scan.py catalog .
python3 <skill>/scripts/instrument_scan.py find "<metric 1>" -k <từ khóa> … "<metric 2>" -k …
```
Xếp mỗi metric vào một trong ba trạng thái:
- **HAVE**: có event hoặc counter đo trực tiếp. Vẫn phải mở file kiểm tra: event bắn đúng thời điểm chưa, có đủ thuộc tính (user, thời gian, giá trị, các chiều cần cắt) không.
- **DERIVABLE**: tính lại được từ bảng hoặc cột sẵn có. Viết sẵn câu truy vấn (SQL hoặc tương đương) vào thẻ và chạy thử nếu có quyền đọc.
- **MISSING**: chưa đo. Viết spec instrumentation (tên event, thuộc tính, chỗ bắn, ví dụ payload) theo `../instrumentation-audit.md`, và đánh dấu ô đó trên dashboard là **"chưa có dữ liệu"**. Không bao giờ điền số giả trông như thật.

Còn metric chính ở trạng thái MISSING thì dừng lại và báo user trước khi thiết kế tiếp: dashboard không có metric chính thì không có lý do tồn tại.

## 3. Chọn hình thức cho từng metric
Theo `../chart-choice.md`. Tóm tắt:
- Một con số hiện tại cộng xu hướng thì dùng **stat tile** (giá trị + chênh lệch so với kỳ trước + sparkline), không phải biểu đồ cột có đúng một cột.
- Chọn biểu đồ theo **việc người đọc phải làm**: so độ lớn dùng cột hoặc thanh ngang; xu hướng theo thời gian dùng đường; một phần so với tổng thể dùng thanh xếp hạng hoặc thanh phân đoạn, hạn chế donut; trên/dưới mục tiêu dùng thanh phân kỳ; phân bố dùng histogram hoặc box plot; quan hệ hai biến dùng scatter.
- **Một trục y duy nhất.** Hai đơn vị khác nhau thì tách thành hai biểu đồ.
- Màu theo **việc màu phải làm** (định danh, độ lớn, phân cực, trạng thái). Màu trạng thái để dành riêng.

Ghi lựa chọn và lý do vào cột "Hình thức" của `metric-spec.md`.

## 4. Bố cục
Viết `dashboard-spec.md` (khung ở `templates/dashboard-spec.md`) trước khi dựng:
- **Đọc theo hình chữ Z/F**: góc trên trái là metric chính. Hàng đầu là các KPI tile, hàng hai là xu hướng của chúng, phía dưới là phần phân rã và chẩn đoán.
- **Bộ lọc nằm ở một hàng phía trên tất cả biểu đồ**, áp dụng chung cho mọi ô. Không đặt bộ lọc riêng trong từng card.
- **Khoảng thời gian và độ tươi luôn hiện rõ**: "Dữ liệu tới 09:00 hôm nay, múi giờ GMT+7".
- **So sánh luôn có mốc**: so với kỳ trước, so với mục tiêu, hoặc so với cùng kỳ năm trước. Con số đứng một mình không nói gì.
- **Lưới thống nhất**: chiều cao card đồng bộ theo hàng, trục cùng thang đo khi đặt các biểu đồ cạnh nhau để so.
- Một màn hình (1440×900) phải đủ để trả lời câu hỏi chính, không cần cuộn.

Sau đó đi qua cổng 3 hướng cho bố cục và phong cách. Metric đã chốt thì giữ nguyên ở cả 3 hướng.

## 5. Dựng
- Dùng thư viện biểu đồ repo đang dùng. Chưa có thì: ECharts, Recharts hoặc Observable Plot cho web; Plotly cho Python; Vega-Lite khi cần đặc tả.
- **Hover/tooltip mặc định có** cho biểu đồ đường, cột, điểm. Tooltip không được là cách duy nhất để đọc giá trị: luôn có chế độ xem bảng.
- Trạng thái rỗng, đang tải, lỗi và dữ liệu cũ phải được thiết kế. Khi tải lại thì giữ số cũ, làm mờ đi, đừng nháy skeleton.
- Số: phân tách hàng nghìn theo locale, làm tròn có chủ đích (1,2 tr thay vì 1.234.567 trên tile), luôn có đơn vị.
- Chế độ tối: chọn bước màu riêng cho nền tối, không tự đảo màu.
- Có thì dùng skill `dataviz` của Claude Code để kiểm tra bảng màu cho người mù màu; không có thì theo quy tắc ở `../chart-choice.md`.

## 6. Kiểm tra trước khi giao
- [ ] Mỗi ô map được về một thẻ trong `metric-spec.md` và một quyết định.
- [ ] Số trên dashboard khớp với truy vấn kiểm chứng trên ít nhất một mốc thời gian (ghi lại truy vấn và kết quả).
- [ ] Không có biểu đồ hai trục y, pie với 2 lát, hay biểu đồ một cột.
- [ ] Mọi metric MISSING hiển thị "chưa có dữ liệu", kèm link tới spec instrumentation.
- [ ] Độ tươi, múi giờ và định nghĩa xem được ngay trên trang (tooltip ở tiêu đề hoặc một trang "Định nghĩa").
- [ ] Vòng đánh bóng ở 1440×900 và ở một màn hình nhỏ.
