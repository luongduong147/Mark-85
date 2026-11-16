# Test hành vi, không test cách cài đặt

Ý tưởng lấy từ `principle-test-behavior-not-implementation` của pstack (Lauren Tan, MIT), viết lại cho quy trình review PR.

## Hành vi và cài đặt
- **Hành vi** là thứ người dùng của code quan sát được qua giao diện họ dùng: giá trị trả về, lỗi ném ra, trạng thái đọc lại được, request đã gửi, row đã ghi, message đã phát.
- **Cài đặt** là thứ họ không thấy: helper private, thứ tự gọi nội bộ, dữ liệu trung gian, collaborator nội bộ nào đã làm việc.

## Hai phép thử cho mỗi test
1. **Làm hỏng hành vi**: cho code trả sai, bỏ một tác động, hoặc làm tác động hai lần. Test vẫn xanh thì nó không chứng minh gì. Nguyên nhân thường gặp:
   - assert lỏng hơn hợp đồng (`assert result`, `toBeTruthy()`);
   - kết quả mong đợi được tính bằng chính code đang test;
   - assert trên dữ liệu mà test tự dựng ra;
   - lặp lại hằng số hoặc prompt nhưng không chạy code dùng nó.
2. **Đổi phần ruột**: giữ mọi kết quả quan sát được, viết lại cấu trúc bên dưới. Test đỏ thì nó đang khóa phần cài đặt; lần refactor nào cũng phải sửa test mà vẫn không bắt được bug.

Test qua được cả hai thì giữ. Còn lại thì viết lại hoặc xóa.

## Hợp đồng quyết định, không phải hình dạng assert
- Hợp đồng là "giỏ hàng trống thì không bao giờ trừ tiền": assert payment client không bị gọi **là** hành vi. Cần thêm một case có trừ tiền để chứng minh test thấy được lời gọi.
- Payload gửi tới service bên ngoài (đã mock) là hành vi, vì service đó quan sát được nó.
- Gọi helper nội bộ là cài đặt.
- So đúng nguyên văn chuỗi lỗi là khóa câu chữ mà không ai đọc. **Loại lỗi** mà người gọi dựa vào để rẽ nhánh mới là hợp đồng.
- Test có thể khóa một bất biến thay cho một lời gọi, ví dụ một key phải có mặt ở hai bảng. Bất biến đó chính là hành vi.

## Mẫu spec cho hành vi chưa có test
```
Hành vi: <câu một dòng, ngôn ngữ của người dùng code>
Given  <trạng thái hoặc input cụ thể, có giá trị thật>
When   <gọi qua giao diện công khai nào>
Then   <kết quả quan sát được, suy từ yêu cầu>
Phá thử: <sửa gì trong code thì test này phải đỏ>
Vị trí: <file test nên đặt> — <tên test>
```
Mỗi hành vi cần ít nhất một case đúng và một case biên hoặc case lỗi. Với bản sửa lỗi, case đầu tiên là input đã gây ra bug, và test này phải đỏ ở merge-base.

## Mùi test cần soi trong PR
- Mock chính module đang test, hoặc mock tới mức không còn dòng code thật nào chạy.
- Snapshot cả object hay cả component khi hợp đồng chỉ là một trường.
- `sleep` trong test; test phụ thuộc thứ tự chạy hay giờ hệ thống.
- Test được thêm cùng lúc với code nhưng chưa từng đỏ. Thử revert phần code: test phải đỏ.
- Test bị sửa expected value cho khớp output mới mà không có giải thích vì sao hành vi đổi.
