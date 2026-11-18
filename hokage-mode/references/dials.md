# Bảng núm của ba chế độ

Cùng một quy trình, khác ở cách vặn núm. Chế độ nào cũng giữ luật bất biến của `SKILL.md` (kiểm trên sản phẩm thật, dừng trước việc không đảo ngược được).

| Núm | Shinobi | Sage | Bruiser |
|---|---|---|---|
| **Tối ưu** | thời gian thực tới khi xong | độ đúng, kiểm chứng được | token trên mỗi kết quả, sức bền |
| **Lập kế hoạch** | ≤ 5 dòng: đường găng + những gì chạy song song | cây giả thuyết: mỗi nhánh có dự đoán và phép thử | điều kiện xong + danh sách đơn vị nhỏ, ghi vào sổ |
| **Song song** | tối đa: mọi nhánh độc lập chạy cùng lúc; đua 2 cách khi chưa chắc | 2–4 nhánh | 1; tối đa 2 khi đang chờ IO |
| **Agent đọc rộng** | `Explore` hoặc `haiku`, nhiều con một lượt | `haiku`, kiểm mẫu kết quả | 1 con `haiku`, trả về ≤ 20 dòng |
| **Agent viết code** | `sonnet` (nhanh, đủ giỏi); đường găng khó thì `opus` | `sonnet`, `effort: high`; phần tinh vi thì `opus` | `haiku`; thất bại 2 lần cùng việc thì lên `sonnet` |
| **Agent phán xét / verify** | không có panel; tự kiểm điều kiện xong | 1 verifier độc lập, **khác model với tác giả**, chỉ thấy claim + artifact | tự kiểm bằng lệnh; verifier `haiku` khi kết quả khó đọc |
| **`opus`** | cho đường găng khi nó nhanh hơn thử nhiều lần | phán xét, thiết kế, verify | không, trừ khi user cho phép |
| **Kiểm chứng** | 1 lần ở điều kiện xong, chạy ngay khi có thể; test hẹp trước, full suite chạy ngầm | mỗi giả thuyết then chốt có phép thử có thể bác bỏ nó; ngưỡng đặt trước khi đo | mỗi đơn vị một kiểm rẻ; kiểm lớn cuối mỗi đợt |
| **Ngữ cảnh** | đọc thẳng, không tiếc, nhưng không đọc lại | tóm tắt có dẫn chứng | grep/`head` trước khi đọc; đọc theo offset; output test `-q`; log ra file, không vào chat |
| **Hỏi user** | không; chọn cách đảo ngược được | chỉ với lựa chọn sản phẩm mà không phép thử nào trả lời được | không; ghi `blocked`, làm phần khác |
| **Sổ nhiệm vụ** | `start` + `sweep` | ghi đủ `hyp` / `check` / `decision`; trích vào câu trả lời | `checkpoint` sau **mỗi** đơn vị; `resume` sau compact |
| **Dọn dẹp** | `sweep --yes --purge`: xóa mọi rác trừ doc và sản phẩm đã commit; `kage.py down --purge`; tắt server; xóa nhánh tạm | `sweep --yes`, giữ log kiểm chứng trong thùng rác 7 ngày | `sweep --yes` cuối mỗi đợt; sổ giữ lại |
| **Dừng khi** | điều kiện xong đạt: hủy ngay mọi agent còn chạy | kết luận chính đã VERIFIED, hoặc báo rõ INCONCLUSIVE | điều kiện xong đạt, hoặc ngõ cụt thật (ghi đã thử gì) |
| **Trả lời** | ≤ 5 dòng: đã xong gì, kiểm bằng gì, đã dọn gì | chuỗi lập luận, bảng giả thuyết, độ tin cậy, điều gì sẽ làm đổi kết luận | ngắn: tiến độ so với điều kiện xong, đơn vị tiếp theo |

## Ghi model vào Agent
```
Agent({ description: "shinobi 02: sửa parser", subagent_type: "general-purpose",
        model: "sonnet", isolation: "worktree", prompt: "Đọc <HOKAGE>/worker.md trước khi làm bất cứ gì.\nChế độ: shinobi\nMục tiêu: …" })
```
- Có file `~/.claude/rules/hokage-models.md` (do user viết, mỗi dòng `vai: model`) thì dòng trong đó thắng bảng này.
- Model nào bị công cụ từ chối thì không truyền lại lần nữa. Lùi về model kế bên cùng họ, hoặc bỏ trường `model`, và nói rõ đã làm vậy.
