# Mẫu `docs/CMAP.md` (tạo khi chạy `/comment-mapping init`)

```markdown
# CMAP — Comment Mapping Playbook

Mọi thay đổi đáng kể trong code mang một CMAP block (When–Why–How) trỏ ngược về spec / plan / task.
Định dạng: xem mục "Định dạng" bên dưới. Công cụ: `python <skill>/scripts/cmap.py {scan|find|history|lint|next-id} .`

## Tài liệu nguồn
| Loại | File | Cách trỏ |
|---|---|---|
| Spec | docs/SPEC.md | `spec=docs/SPEC.md#<số mục>` |
| Plan | docs/PLAN.md | `plan=docs/PLAN.md#<bước>` |
| Checklist | docs/TASKS.md | `task=<T-xxx>` |

## Module & tiền tố ID
| Module | Thư mục | Tiền tố ID | Chủ sở hữu |
|---|---|---|---|

## Định dạng
<chép phần "Khung chuẩn" và bảng "Theo trạng thái" từ comment-format.md>

## Archive
<block cũ đã gộp khỏi code, theo id>
```

# Dòng rule thêm vào CLAUDE.md / AGENTS.md

Thêm đúng một mục (nếu chưa có):

```markdown
## Comment mapping
Mọi thay đổi code không tầm thường (module mới, fix lỗi, đổi hành vi, refactor, deprecate) phải có CMAP block When–Why–How theo `docs/CMAP.md`, trỏ về spec/plan/task. Dùng skill `/comment-mapping` để viết, tìm (`find "<việc>"`) và xem lịch sử module (`history <module>`).
```
