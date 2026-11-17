# Metric spec — <tên dashboard>

- Người dùng: <ai> · Quyết định chính: <làm gì với dashboard này> · Tần suất xem: <…> · Độ tươi cần: <…>
- Múi giờ: <GMT+7> · Loại trừ chung: <đơn test, nội bộ, bot>

## Cây metric
```
<Metric chính>
├── <dẫn dắt 1>
├── <dẫn dắt 2>
└── bảo vệ: <…>
```

## Thẻ metric

### <Tên metric>
| Trường | Giá trị |
|---|---|
| Loại | chính / dẫn dắt / bảo vệ / chẩn đoán |
| Quyết định | <số này đổi thì ai làm gì> |
| Công thức | `<tử số> / <mẫu số>` |
| Grain | <user / phiên / đơn / ngày> |
| Cửa sổ thời gian | <…> |
| Chiều cắt | <…> |
| Loại trừ | <…> |
| Nguồn | **HAVE / DERIVABLE / MISSING**: <event, bảng, file:line hoặc link spec instrumentation> |
| Truy vấn kiểm chứng | ```sql …``` → kết quả <giá trị> tại <mốc> |
| Độ tươi | <…> |
| Mốc so sánh | <kỳ trước / mục tiêu / cùng kỳ> |
| Ngưỡng | xanh <…> · vàng <…> · đỏ <…> |
| Chủ sở hữu | <…> |
| Hình thức | <stat tile / đường / thanh…>, vì người đọc cần <việc> |

## Thiếu nguồn (MISSING)
- <metric>: spec instrumentation ở <đường dẫn>; trên dashboard hiển thị "chưa có dữ liệu".
