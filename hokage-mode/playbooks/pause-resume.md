# Dừng an toàn / tiếp tục

## Dừng (chỉ khi user bảo dừng, hoặc sắp mất ngữ cảnh)
1. Dừng ở một ranh giới an toàn: làm xong bước nguyên tử đang dở, hoặc lùi ra khỏi nó. Hủy các agent con.
2. Thay đổi chưa commit thì gom thành một commit `wip:` trên nhánh làm việc (không phải nhánh chung). Tree đang hỏng thì ghi một dòng trong body commit.
3. `trail.py note checkpoint "<đang ở đâu, đã kiểm gì, bước kế tiếp, file then chốt, bẫy>"` rồi `trail.py resume` để sinh `resume.md`.

## Tiếp tục (phiên mới, sau compact, "làm tiếp")
1. `trail.py resume`. Sổ là nguồn sự thật, đừng suy luận lại từ đầu.
2. Đối chiếu sổ với thực tế: `git log` và `git diff` so với base, todo còn mở.
3. Tìm điểm tiếp tục, đưa phần còn lại qua router. Không chạy lại những gì sổ ghi là đã VERIFIED.
4. Kiểm lại các nhận định thừa hưởng từ phiên trước trên sản phẩm thật trước khi tuyên bố xong.
