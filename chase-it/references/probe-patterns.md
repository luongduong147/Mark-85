# Kiểu probe theo loại lỗi

| Loại nghi vấn | Đặt probe ở đâu | Ghi gì |
|---|---|---|
| **Race / đồng thời** | Trước và sau khi đọc/ghi state chung, chỗ lấy/nhả lock, chỗ await | thread/task id, version hoặc giá trị state trước và sau, thời điểm ns |
| **Timeout / chậm** | Bọc mỗi lời gọi ra ngoài (HTTP, DB, LLM, queue) | thời gian thực thi (ms), kích thước payload, đích gọi, lần retry thứ mấy, mã lỗi |
| **State lưu trữ** (chỉ lỗi sau restart) | Lúc load config, cache hay file lock khi khởi động | đường dẫn, mtime, hash nội dung, version schema |
| **Dữ liệu xấu** | Tại biên parse hoặc validate | kiểu dữ liệu, độ dài, các key có mặt, hash (không ghi giá trị nhạy cảm) |
| **Nhánh logic sai** | Tại if/switch/router quyết định | nhánh được chọn kèm các giá trị điều kiện |
| **LLM không ổn định** | Trước và sau khi gọi model, khi parse output | model, temperature, độ dài prompt, hash prompt, finish_reason, số token, lỗi parse, route hoặc intent và confidence |
| **Rò bộ nhớ / tài nguyên** | Định kỳ (sampled), mỗi lần mở/đóng resource | RSS, số handle hoặc kết nối đang mở, kích thước queue/cache |
| **Mất message / sự kiện** | Lúc producer gửi, consumer nhận, khi ack | message id, offset, trạng thái ack, số lần redeliver |
| **Môi trường** | Lúc khởi động | version, các env quan trọng (đã che bớt), host, DNS hoặc proxy được dùng |

## Cú pháp marker theo ngôn ngữ

Python:
```python
log.info("CHASE[ws-drop-20261113] p=3 cid=%s state=%s dt_ms=%d", cid, st, dt)  # CHASE:ws-drop-20261113
```
TS/JS:
```ts
console.error(`CHASE[ws-drop-20261113] p=3 cid=${cid} state=${st}`); // CHASE:ws-drop-20261113
```
Rust:
```rust
eprintln!("CHASE[ws-drop-20261113] p=3 cid={cid} state={st:?}"); // CHASE:ws-drop-20261113
```
Probe nhiều dòng:
```python
# CHASE:ws-drop-20261113:begin
t0 = time.perf_counter()
...
log.info("CHASE[ws-drop-20261113] p=4 dt_ms=%d", (time.perf_counter() - t0) * 1000)
# CHASE:ws-drop-20261113:end
```

## Nguyên tắc
- Mỗi probe trả lời một câu hỏi cụ thể. Không biết probe đó dùng để phân biệt giả thuyết nào thì đừng đặt.
- Log ra stderr hoặc logger sẵn có của repo, không mở thêm một file log mới nếu không cần.
- Probe không được đổi hành vi chương trình: không nuốt exception, không thêm await hay sleep làm lệch timing (trừ khi đó chính là thí nghiệm, và phải ghi rõ trong ledger).
