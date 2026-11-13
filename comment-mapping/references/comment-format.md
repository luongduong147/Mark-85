# Định dạng CMAP block

Một block = một sự kiện (tạo mới, sửa lỗi, đổi hành vi, refactor, ngừng dùng). Block đặt **ngay trên** hàm/class/đoạn code nó mô tả. Code thay đổi nhiều lần → **thêm block mới lên trên block cũ**, không xóa block cũ (đó là lịch sử phiên bản). Khi đã quá 3 block ở một chỗ, gộp các block cũ nhất vào `docs/CMAP.md` (mục Archive) và để lại 1 dòng `Supersedes:`.

## Khung chuẩn

```
# [CMAP] <id> | <STATUS> | <tiêu đề ngắn>
#   Ref:     spec=<file>#<mục> plan=<file>#<bước> task=<id checklist>
#   When:    found=<YYYY-MM-DD> fixed=<YYYY-MM-DD>
#   Why:     <tại sao phải sửa: lỗi gì, ai/gì bị ảnh hưởng, bằng chứng>
#   Impact:  <phần nào bị ảnh hưởng bởi thay đổi: module, API, dữ liệu, caller>
#   How:     <đã sửa thế nào: cơ chế, không phải diff>
#   Updated: <YYYY-MM-DD>
```

- `id` = `<module>-<NNN>`, lấy bằng `python scripts/cmap.py next-id <root> <module>`.
- `STATUS` ∈ `NEW | FIX | CHANGE | REFACTOR | DEPRECATED`.
- Field dài → xuống dòng, thụt ≥3 khoảng trắng sau ký tự comment, sẽ được nối vào field trước.
- `Ref` chỉ ghi phần có thật; thiếu cả spec/plan/task → `Ref: none (lý do)`.
- Trường tùy chọn: `Supersedes: <id cũ>`, `Author: <tên>`.

## Theo trạng thái

| STATUS | When | Bắt buộc |
|---|---|---|
| `NEW` | `created=<date>` | Ref, When, Why (vì sao module tồn tại), How (thiết kế chính / pattern) |
| `FIX` | `found=<date> fixed=<date>` | Ref, When, Why, Impact, How |
| `CHANGE` | `changed=<date>` | Ref, When, Why, Impact, How |
| `REFACTOR` | `changed=<date>` | Ref, When, Why, Impact (phải ghi "không đổi hành vi" nếu đúng), How |
| `DEPRECATED` | `deprecated=<date> remove-after=<date>` | Ref, When, Why, Impact (caller cần chuyển sang đâu), How |

## Ví dụ theo ngôn ngữ

Python / Shell / YAML:
```python
# [CMAP] router-004 | FIX | Intent "hoàn tiền" route nhầm sang "thanh toán"
#   Ref:     spec=docs/SPEC.md#3.2 plan=docs/PLAN.md#P2.1 task=T-031
#   When:    found=2026-11-10 fixed=2026-11-13
#   Why:     Keyword "tiền" match cả 2 intent; câu không dấu "hoan tien" rơi vào fallback.
#            12/40 câu test held-out sai.
#   Impact:  semantic_router.py, routes.yaml; không đổi API /classify
#   How:     Bỏ keyword list, dùng embedding + ngưỡng 0.78, fallback LLM classifier.
#   Updated: 2026-11-13
def classify(text: str) -> Route:
```

TS / JS / Rust / Go / Java:
```ts
// [CMAP] auth-001 | NEW | Refresh token rotation
//   Ref:     spec=docs/SPEC.md#4 plan=docs/PLAN.md#P1 task=T-002
//   When:    created=2026-11-13
//   Why:     Spec yêu cầu phiên 30 ngày nhưng access token chỉ 15 phút.
//   How:     Rotation một lần dùng; token cũ bị thu hồi khi dùng lại (phát hiện replay).
//   Updated: 2026-11-13
export async function rotate(...)
```

SQL / Lua: dùng `--`. HTML / Markdown: `<!-- [CMAP] ... -->` mỗi dòng.

## Không làm
- Không chép diff vào How. How = cơ chế.
- Không viết CMAP cho thay đổi lặt vặt (đổi tên biến, format, typo).
- Không ghi bí mật, token, dữ liệu khách hàng vào Why.
