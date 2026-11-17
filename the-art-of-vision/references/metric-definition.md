# Định nghĩa metric

Metric không có định nghĩa viết ra giấy thì mỗi người trong phòng họp sẽ hiểu một kiểu. Mỗi metric là một thẻ trong `metric-spec.md`.

## Các trường bắt buộc của thẻ
| Trường | Câu hỏi | Ví dụ |
|---|---|---|
| Tên | Gọi là gì, thống nhất ở mọi nơi | Tỷ lệ chuyển đổi checkout |
| Quyết định | Số này lên hay xuống thì ai làm gì | Giảm dưới 2,5% hai ngày liền thì PM checkout điều tra |
| Công thức | Tử số / mẫu số, viết như code | `count(distinct order_completed.user_id) / count(distinct checkout_started.user_id)` |
| Đơn vị hạt (grain) | Đếm theo gì: user, phiên, đơn, ngày | user–ngày |
| Cửa sổ thời gian | Kỳ tính, múi giờ, cách gán sự kiện vào kỳ | ngày theo GMT+7, theo thời điểm `checkout_started` |
| Chiều cắt | Có thể chia theo gì | kênh, thiết bị, quốc gia |
| Loại trừ | Bỏ ai, bỏ gì | đơn test, nhân viên nội bộ, bot |
| Nguồn | Event, bảng, metric nào; trạng thái HAVE / DERIVABLE / MISSING | `analytics.track('checkout_started')` src/checkout.ts:1 |
| Độ tươi | Trễ bao lâu so với thực tế | 15 phút |
| Mốc so sánh | So với gì | cùng ngày tuần trước, mục tiêu 3% |
| Ngưỡng | Khi nào thì xanh, vàng, đỏ | < 2,5% đỏ; 2,5–3% vàng |
| Loại | Chính, dẫn dắt, bảo vệ hay chẩn đoán | Dẫn dắt (cho doanh thu) |
| Chủ sở hữu | Ai chịu trách nhiệm định nghĩa | PM checkout |
| Hình thức | Biểu đồ nào và vì sao | Stat tile + sparkline 14 ngày; việc người đọc làm: thấy hôm nay so với tuần trước |

## Phân loại theo bản chất
- **Đếm** (count): số đơn, số user. Cộng dồn được theo thời gian và theo chiều cắt.
- **Tổng** (sum): doanh thu. Cộng dồn được.
- **Tỷ lệ** (ratio): chuyển đổi, churn. **Không cộng hay lấy trung bình các tỷ lệ**; phải cộng tử số và mẫu số riêng rồi mới chia.
- **Trung bình** và **phân vị**: thời gian xử lý, độ trễ. Dùng p50/p95 thay cho trung bình khi phân bố lệch. Không lấy trung bình của các p95.
- **Đếm duy nhất** (distinct): DAU, MAU. Không cộng DAU các ngày lại để ra MAU.
- **Snapshot** (gauge): tồn kho, số ticket đang mở. Không cộng theo thời gian; lấy giá trị cuối kỳ hoặc trung bình.

## Bẫy hay gặp
- **Mẫu số trôi**: "tỷ lệ chuyển đổi" lúc chia cho phiên, lúc chia cho user. Ghi rõ trong công thức.
- **Nghịch lý Simpson**: tỷ lệ tổng tăng trong khi mọi nhóm đều giảm, do cơ cấu nhóm thay đổi. Khi so kỳ, xem thêm theo chiều cắt chính.
- **Múi giờ**: dữ liệu UTC, người xem ở GMT+7, nên "hôm nay" lệch 7 tiếng.
- **Dữ liệu chưa đủ kỳ**: kỳ hiện tại mới đi một nửa mà đặt cạnh kỳ trước đã đủ. Đánh dấu kỳ chưa hoàn tất, hoặc so cùng điểm trong kỳ (cùng giờ hôm qua).
- **Sống sót**: chỉ đo những user còn ở lại. Retention phải tính theo cohort.
- **Vanity metric**: tổng lũy kế chỉ đi lên (tổng số user đã đăng ký). Thay bằng số mới trong kỳ hoặc số đang hoạt động.
- **Goodhart**: metric trở thành mục tiêu thì sẽ bị tối ưu méo. Luôn đi kèm ít nhất một metric bảo vệ.
- **Sai lệch đếm trùng**: join một-nhiều làm tổng doanh thu bị nhân lên. Kiểm tra lại bằng một truy vấn đếm đơn giản.

## Cây metric (ví dụ thương mại điện tử)
```
Doanh thu thuần (chính)
├── Số đơn = Lượt truy cập × Tỷ lệ chuyển đổi (dẫn dắt)
│   └── chẩn đoán: tỷ lệ rơi ở từng bước của phễu
├── Giá trị đơn trung bình (dẫn dắt)
└── bảo vệ: tỷ lệ hoàn tiền, p95 thời gian tải trang checkout
```
