# Dashboard spec — <tên>

- Màn hình đích: <1440×900 / TV 1920×1080 / mobile> · Thư viện biểu đồ: <…> · Design system: <…>
- Bộ lọc chung (một hàng, trên cùng): <khoảng thời gian, kênh, …> · Mặc định: <7 ngày gần nhất>
- Dòng độ tươi: "Dữ liệu tới <thời điểm>, <múi giờ>"

## Bố cục
```
┌──────────────────────────── bộ lọc ────────────────────────────┐
│ [KPI chính]  [KPI dẫn dắt 1]  [KPI dẫn dắt 2]  [KPI bảo vệ]      │  hàng 1: stat tile
├───────────────────────────────┬────────────────────────────────┤
│ Xu hướng metric chính (đường)   │ Phân rã theo <chiều> (thanh)    │  hàng 2
├───────────────────────────────┴────────────────────────────────┤
│ Chẩn đoán / bảng chi tiết (drill-down)                           │  hàng 3
└─────────────────────────────────────────────────────────────────┘
```

## Ô
| Vị trí | Metric (thẻ) | Hình thức | Mốc so sánh | Tương tác | Trạng thái rỗng / lỗi |
|---|---|---|---|---|---|
| H1-1 | <…> | stat tile + sparkline 14 ngày | tuần trước | click → drill-down | "chưa có dữ liệu" + link spec |

## Màu
- Định danh (theo thứ tự cố định): <…> · Tuần tự: <một sắc độ> · Phân cực: <cực A / xám / cực B> · Trạng thái (dành riêng): <…>
- Đã kiểm mù màu bằng: <công cụ> → <kết quả>
