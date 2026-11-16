# Anti-slop — <phạm vi> — <YYYY-MM-DD>

- Phạm vi: <diff từ `<base>` | danh sách file> · <n> file, <n> dòng
- Máy bắt <n> cờ → xác nhận <n> · bác bỏ <n> (báo nhầm)
- Test: mốc <xanh/đỏ, lệnh> → sau khi sửa <xanh/đỏ> | không sửa

## MUST KILL
| file:line | Mã | Vấn đề | Cách sửa | Đã sửa? |
|---|---|---|---|---|

## SHOULD
| file:line | Mã | Vấn đề | Cách sửa | Đã sửa? |
|---|---|---|---|---|

## KEEP (có lý do)
| file:line | Mã | Lý do giữ | Bằng chứng |
|---|---|---|---|

## Kết quả sửa
- `git diff --stat`: −<n> / +<n> dòng
- Nhóm bị revert vì test đỏ: <…>

## Còn mở / ngoài phạm vi
- <…>
