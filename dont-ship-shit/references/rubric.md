# Rubric chấm PR/MR

## Từng tiêu chí

| # | Tiêu chí | PASS | WARN | FAIL |
|---|---|---|---|---|
| 1 | Double work | Không có khối nào trùng; hoặc có trùng nhưng PR dùng lại hoặc mở rộng code cũ | Trùng ở mức `shape` với code người khác, hoặc trùng tên định nghĩa, cần người viết xác nhận | Viết lại thứ đã có (nhất là `mine: true`) mà không có lý do; tạo ra hai nguồn sự thật cho cùng một quy tắc |
| 2 | Regression | Đã chạy test ở head, không có test nào đỏ mới so với base | Chưa chạy được test; hoặc có test flaky không tái hiện được | Có test xanh ở base mà đỏ ở head; tắt, skip, xóa test hay bỏ assert để qua CI |
| 3 | Test hành vi | Mỗi hành vi mới hoặc đổi có ít nhất một test qua được cả hai phép thử | Có test nhưng một số chỉ khóa phần cài đặt; hoặc thiếu test cho nhánh phụ | Hành vi chính không có test nào kiểm được; hoặc toàn bộ test chỉ khóa phần cài đặt |
| 4 | Tổng quát | Bản sửa đánh đúng tầng gốc, input khác vẫn đúng | Đúng tầng nhưng còn literal hoặc cờ đặc biệt có thể rút ra cấu hình | Vá đúng case (so id hay chuỗi cứng, nuốt lỗi, sleep né race) khi gốc đã rõ và nằm trong phạm vi PR |
| 5 | Map + doc | Map được tính năng bằng nguồn rõ ràng; doc dưới 150 chữ | Map bằng suy luận (Inferred); hoặc PR làm hơn một việc, nên tách | Không xác định được PR phục vụ việc gì |

## Phán quyết

| Phán quyết | Điều kiện |
|---|---|
| **BLOCK** | Regression đã xác minh; tắt hoặc xóa test để qua; lộ secret hay dữ liệu khách hàng; migration làm mất dữ liệu; đổi API công khai mà không có đường chuyển tiếp |
| **CHANGES REQUIRED** | Có ít nhất một FAIL ở tiêu chí 1, 3 hoặc 4 |
| **MERGE + NITS** | Không có FAIL; có WARN; hoặc chạy với `--quick` |
| **MERGE** | 5/5 PASS, test đã chạy thật và xanh |

## Phân xử ca khó
- **Trùng code nhưng cố ý** (ví dụ tách module để sau này bỏ module cũ): PASS nếu mô tả PR nói rõ kế hoạch gỡ code cũ, không thì WARN.
- **Hotfix khẩn**: được phép vá case, nhưng phải có issue theo dõi bản sửa tận gốc và ghi trong mô tả. Có thì WARN, không có thì FAIL.
- **PR chỉ refactor**: tiêu chí 3 xét xem test cũ còn xanh mà không phải sửa không. Phải sửa test cũ thì nghĩa là test đang khóa phần cài đặt; ghi WARN cho test, không đổ lỗi cho PR.
- **PR chỉ đổi doc hay config**: tiêu chí 2 và 3 ghi N/A. Phán quyết dựa vào 1, 4, 5 cộng với kiểm tra config có hợp lệ không.
- **Tôi tự review PR của chính mình**: rubric giữ nguyên, không nới tay.
