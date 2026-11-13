# Prompt tranh biện (Pha C, mỗi vòng)

---

Vòng tranh biện <k>. Dưới đây là bài của các đối thủ (đã đổi nhãn):
<danh sách: nhãn → đường dẫn artifact + rationale>

Bài của bạn: <đường dẫn bản hiện tại>
Các đòn đã đánh vào bài bạn ở vòng trước (nếu có): <trích>

Làm ba việc:

**1. Tấn công.** Với mỗi đối thủ, chỉ ra tối đa 2 lỗi mạnh nhất. Mỗi lỗi phải kèm:
- bằng chứng: lệnh đã chạy và output, ví dụ phản chứng cụ thể, hoặc trích `file:line` mâu thuẫn với task;
- hậu quả: lỗi này phá vỡ yêu cầu nào của task.
Không chê về style, cách đặt tên hay "tôi thích cách khác hơn". Không chứng minh được thì không nộp.

**2. Phòng thủ.** Với mỗi đòn nhắm vào bài bạn, chọn đúng một:
- `ACCEPT`: đòn đúng, sẽ sửa;
- `REBUT`: đòn sai, kèm bằng chứng;
- `OUT-OF-SCOPE`: ngoài phạm vi task, kèm lý do.

**3. Sửa bài.** Nộp bản `v<k+1>` trong chỗ làm riêng. Được phép học ý tưởng của đối thủ, nhưng phải tự diễn đạt lại cho khớp với thiết kế của mình. Đổi hẳn hướng thì phải ghi rõ bằng chứng nào thuyết phục bạn.

Viết `debate-r<k>.md`:
```
ATTACKS:
- target=<nhãn> | claim=<...> | evidence=<lệnh/output/ví dụ> | breaks=<yêu cầu>
DEFENSE:
- from=<nhãn> | claim=<...> | verdict=ACCEPT|REBUT|OUT-OF-SCOPE | reason=<...>
CHANGES_IN_V<k+1>: <danh sách>
STILL_BELIEVE: <1-2 câu: vì sao hướng của bạn vẫn tốt nhất, hoặc vì sao bạn đã đổi>
```
