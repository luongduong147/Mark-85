# Kiểm tra nguồn đo và viết spec instrumentation

## Tìm ở đâu
`scripts/instrument_scan.py` quét theo tên. Còn phải tự xem thêm:
- **Analytics phía client**: Segment, PostHog, Mixpanel, Amplitude, GA4 (`gtag('event', …)`), `dataLayer.push`.
- **Metric phía server**: Prometheus (`Counter`, `Histogram`), OpenTelemetry (`meter.createCounter`), StatsD, Datadog.
- **Log có cấu trúc**: log dạng JSON có trường `event` hay `action`; có thể là nguồn tạm thời nếu đã được gom về một chỗ.
- **Cơ sở dữ liệu nghiệp vụ**: bảng đơn hàng, thanh toán, subscription; các cột thời gian `created_at`, `cancelled_at`.
- **Kho dữ liệu**: model dbt (`models/**/*.sql`), view, bảng tổng hợp sẵn. Thường có sẵn metric đã định nghĩa trong `metrics:` hoặc semantic layer.
- **Hệ thống bên ngoài**: Stripe, App Store, CRM. Ghi rõ là cần API hoặc export, đừng giả định là có sẵn.

## Kiểm một nguồn HAVE có dùng được không
1. Event bắn **đúng thời điểm nghiệp vụ** chưa? Ví dụ `order_completed` phải bắn sau khi thanh toán thành công, không phải lúc bấm nút.
2. Có **định danh** để đếm duy nhất chưa (user_id, session_id, order_id)?
3. Có đủ **thuộc tính để cắt** theo các chiều trong thẻ chưa?
4. Có **bắn trùng** không (retry, bấm hai lần, reload trang)? Có idempotency key không?
5. Có **đủ lịch sử** cho mốc so sánh không? Event mới thêm tuần trước thì chưa so được cùng kỳ năm trước.
6. Client-side có bị **chặn bởi ad blocker** không? Với metric tiền thì ưu tiên nguồn server.

Trượt điểm nào thì hạ xuống DERIVABLE hoặc MISSING, kèm lý do.

## Spec cho metric MISSING
```
Event: <object_action, snake_case, thì quá khứ>   ví dụ: refund_issued
Bắn ở đâu: <file / service / hàm>, phía server hay client
Thời điểm: <sự kiện nghiệp vụ chính xác>
Thuộc tính:
  - user_id (string, bắt buộc)
  - order_id (string, bắt buộc, khóa chống trùng)
  - amount (number, đơn vị: VND)
  - reason (enum: damaged | late | other)
  - occurred_at (ISO 8601, UTC)
Ví dụ payload: {...}
Metric dùng nó: <tên thẻ trong metric-spec.md>
Cách kiểm sau khi thêm: <truy vấn đếm thử, so với nguồn đối chiếu>
```
Quy ước tên: `object_action` ở thì quá khứ, snake_case, một nghĩa duy nhất. Theo quy ước sẵn có của repo nếu đã có.

Thiết kế dashboard vẫn tiếp tục được: ô của metric MISSING hiển thị trạng thái "chưa có dữ liệu" và link tới spec. Không lấp bằng số giả.
