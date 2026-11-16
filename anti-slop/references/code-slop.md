# Danh mục slop trong code

Mỗi mục gồm: dấu hiệu, vì sao là slop, cách sửa. Mã ở đầu dòng (C1, C2…) cố định để báo cáo trích dẫn được.

## Thừa
- **C1. Code chết.** Hàm hoặc biến không ai gọi, nhánh `if` không bao giờ đúng, flag luôn bật, export không ai import. Cách sửa: xóa. Đã có git lưu lại.
- **C2. Code bị comment lại.** Khối code nằm trong comment "để sau dùng". Cách sửa: xóa.
- **C3. Debug sót lại.** `console.log`, `print`, `dbg!`, `debugger`, log level INFO cho việc chỉ dùng lúc debug. Cách sửa: xóa, hoặc hạ xuống DEBUG nếu thật sự có giá trị khi vận hành.
- **C4. Comment kể lể.** Comment nói lại đúng điều code đã nói (`// tăng i lên 1`, `# Helper function to get user`), hoặc docstring chỉ lặp lại tên hàm. Cách sửa: xóa. Chỉ giữ comment trả lời câu hỏi *vì sao* mà code không tự nói được. Repo dùng comment-mapping thì block `[CMAP]` không tính là kể lể.
- **C5. Tham số và cấu hình đầu cơ.** Option, tham số hay biến môi trường không có chỗ gọi nào truyền giá trị khác mặc định. Cách sửa: bỏ, dùng hằng.

## Lặp
- **C6. Lặp nguyên văn.** Cùng khối code ở hai chỗ trở lên. Cách sửa: giữ một bản ở chỗ hợp lý nhất, các chỗ khác gọi vào đó.
- **C7. Lặp theo cấu trúc.** Cùng hình dạng, khác tên biến hoặc literal (map field A→B ở ba chỗ, ba endpoint giống nhau trừ tên bảng). Cách sửa: tham số hóa phần khác nhau. Chỉ làm khi có ít nhất 3 bản, hoặc 2 bản mà đã từng sửa lệch nhau.
- **C8. Hai nguồn sự thật.** Cùng một quy tắc (regex validate, danh sách trạng thái, giới hạn số) được định nghĩa ở hai nơi. Cách sửa: một hằng hoặc một hàm, mọi chỗ khác import từ đó.
- **C9. Viết lại thứ đã có.** Tự cài lại thứ mà thư viện chuẩn, dependency sẵn có hoặc chính repo đã có (`deepClone` tự chế khi đã có `structuredClone`; hàm format ngày thứ ba). Cách sửa: dùng bản có sẵn.

## Phình
- **C10. Abstraction đầu cơ.** Interface hay abstract class chỉ có một cài đặt; factory chỉ tạo một loại; strategy chỉ có một strategy; class `XxxManager` hay `XxxHelper` chỉ có một method. Cách sửa: thay bằng hàm hoặc class cụ thể. Khi nào có cài đặt thứ hai thì hẵng tách.
- **C11. Wrapper chuyển tiếp.** Hàm chỉ gọi đúng một hàm khác với cùng tham số; layer service chỉ chuyển lời gọi xuống repository. Cách sửa: gọi thẳng.
- **C12. Guard không thể kích hoạt.** Kiểm `null` cho giá trị mà kiểu dữ liệu hoặc code ngay phía trên đã đảm bảo; `try/catch` quanh code không thể ném lỗi; validate lại input đã được validate ở biên. Cách sửa: xóa, để kiểu dữ liệu hoặc biên hệ thống chịu trách nhiệm.
- **C13. Thoát khỏi hệ thống kiểu.** `as any`, `@ts-ignore`, `# type: ignore`, `unwrap()` khắp nơi, cast qua `unknown`. Cách sửa: sửa kiểu cho đúng. Nếu thật sự cần thoát (thư viện thiếu type), giữ một chỗ duy nhất có ghi lý do.

## Che lỗi
- **C14. Nuốt lỗi.** `except: pass`, `catch {}`, `.catch(() => {})`, trả `None` hay `[]` khi lỗi mà người gọi không phân biệt được với kết quả rỗng thật. Cách sửa: để lỗi nổi lên, hoặc bắt đúng loại lỗi và xử lý có chủ đích.
- **C15. Fallback giả.** Lỗi thì trả dữ liệu mặc định trông như thật (giá 0, user "guest") làm bug âm thầm lan ra. Cách sửa: báo lỗi rõ ràng.
- **C16. Retry hoặc sleep thay cho sửa race condition.** Cách sửa: tìm thứ tự hoặc điều kiện đúng (await, lock, event). Không tìm ra thì chuyển sang **chase-it**.

## Test slop
- **C17. Test khóa phần cài đặt.** Mock helper nội bộ, assert thứ tự gọi, snapshot cả object. Xem `../../dont-ship-shit/references/behavior-tests.md`.
- **C18. Test không chứng minh gì.** `expect(result).toBeDefined()`, assert trên dữ liệu test tự dựng, test không gọi code thật. Cách sửa: assert đúng hợp đồng.

## Không phải slop
- Code lặp ở hai chỗ có lý do để thay đổi độc lập với nhau (hai bounded context khác nhau).
- Guard ở biên hệ thống: input từ user, network, file, env.
- Comment giải thích ràng buộc bên ngoài, workaround cho bug của thư viện (kèm link), hoặc yêu cầu pháp lý.
- Log có chủ đích ở level phù hợp.
