# Kage-bunshin — <việc> (<run id>)

**Kết quả**: <2–3 câu: trả lời câu hỏi gốc / kết luận chính>

## Bầy
| # | Phần việc | Model | Trạng thái | Phát hiện | Thời gian |
|---|---|---|---|---|---|
| 01 | <…> | haiku | done | <n> | <…> |

Chi phí ước lượng: <N> phân thân × <model> · <số đợt> đợt

## Phát hiện (đã gộp trùng)
| Mức | Phát hiện | Bằng chứng | Phân thân | Kiểm chứng |
|---|---|---|---|---|
| high | <…> | `file:line` / URL | 02, 05 | Verified / Inferred |

## Chưa xong
- <phần `blocked` / `not_covered`, lý do, đề xuất: giao lại / cần user làm tay / ngoài phạm vi>

## Thay đổi code (nếu có)
- `kage/<run>/NN`: <tóm tắt diff>. Đề xuất: cherry-pick / bỏ (chờ user đồng ý)

## Dọn dẹp
- Worktree: <đã gỡ hết / giữ theo --keep: lệnh `kage.py down --run <id>`>
- Nhánh `kage/*`: <đã xóa> · Tiến trình nền: <đã tắt> · Patch đã cất: `~/.cache/kage/<repo>/<run>/salvage/`
