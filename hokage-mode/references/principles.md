# Nguyên tắc nền

Rút gọn từ các skill `principle-*` của pstack (Lauren Tan, MIT). Mỗi nguyên tắc ghi: khi nào dùng, rồi làm gì. Khi một nguyên tắc làm đổi quyết định, nêu tên nó trong báo cáo.

## Lõi
- **Laziness protocol.** Dùng khi định thêm abstraction, layer hay tham số. Nghiêng về xóa; thay đổi nhỏ nhất giải được vấn đề là thay đổi được ship.
- **Foundational thinking.** Dùng trước khi viết logic. Gọi tên kiểu dữ liệu và cấu trúc lõi trước, nói rõ các actor chạy đồng thời dùng chung cái gì. Dựng khung trước, tính năng sau.
- **Redesign from first principles.** Dùng khi yêu cầu mới không vừa thiết kế cũ. Thiết kế lại như thể yêu cầu đó có từ ngày đầu, đừng vá thêm một nhánh `if`.
- **Attack the premise.** Dùng khi hai bản sửa dựa trên cùng một tiền đề đều thất bại. Viết tiền đề đó ra và kiểm nó trực tiếp, trước khi viết bản sửa thứ ba.
- **Subtract before you add.** Xóa phần chết trước, rồi mới xây lên nền đã gọn.
- **Minimize reader load.** Đếm số lớp và trạng thái ẩn. Gộp wrapper chỉ có một chỗ gọi, thu hẹp phạm vi của biến mutable.
- **Build the lever.** Việc lặp lại thì viết công cụ làm thay (codemod, script, generator). Công cụ đó chính là thứ reviewer chạy lại được.
- **Exhaust the design space.** Quyết định mới, chưa có tiền lệ: làm 2–3 prototype rồi so sánh, rồi mới chốt.

## Kiến trúc
- **Model the domain.** Logic có trạng thái, rẽ nhánh nhiều, hoặc lặp một giả định về shape qua nhiều file: dùng state machine, bảng/registry, hoặc kiểu dữ liệu có cấu trúc, thay cho if rải rác.
- **Boundary discipline.** Kiểm tra dữ liệu ở biên hệ thống. Bên trong thì tin kiểu dữ liệu; logic nghiệp vụ giữ thuần.
- **Make operations idempotent.** Lệnh có thể chạy lại sau crash hay retry thì chạy bao nhiêu lần cũng về cùng một trạng thái.
- **Separate before serializing shared state.** Các actor có thể ghi chung một thứ: tách nơi ghi trước, khóa sau. Mỗi agent một worktree.
- **Migrate callers then delete legacy APIs.** Có API mới thì chuyển hết chỗ gọi và xóa API cũ trong cùng một đợt. Không để lớp tương thích.

## Kiểm chứng
- **Prove it works.** Kiểm trên sản phẩm thật, không trên thứ thay thế.
- **Fix root causes.** Lần từ triệu chứng về chỗ đầu tiên hệ thống đi sai. Thêm guard chỉ là bản sửa khi trạng thái nó chặn là trạng thái hợp lệ.
- **Sequence verifiable units.** Chia thành đơn vị nhỏ, mỗi đơn vị kết thúc bằng một lần kiểm, kiểm xong mới làm đơn vị tiếp.
- **Test behavior, not implementation.** Assert thứ người dùng code quan sát được. Đổi phần ruột thì test vẫn xanh; vỡ hành vi thì test đỏ.
- **Explain the number.** Trước khi tin một con số, tìm thứ đang giới hạn nó, và loại trừ khả năng nó đo nhầm thứ khác.

## Ủy quyền
- **Guard the context window.** Việc đọc khối lượng lớn giao cho subagent; luồng chính chỉ giữ kết luận.
- **Never block on the human.** Việc đảo ngược được thì làm luôn, đưa kết quả ra, để người chỉnh hướng sau.

## Meta
- **Encode lessons in structure.** Thấy mình viết cùng một chỉ dẫn lần thứ hai thì biến nó thành lint, check hoặc script.
