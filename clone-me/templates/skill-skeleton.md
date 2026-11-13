```markdown
---
name: <kebab-case>
description: "<Làm gì, 1 câu>. Dùng khi <tình huống>, hoặc khi gõ /<name>, '<cụm user thật sự hay gõ 1>', '<cụm 2>', '<cụm 3>'."
argument-hint: "<tham số>"
disable-model-invocation: true   # bỏ dòng này nếu muốn model tự kích hoạt
---

# <Tên>

Lệnh: **$ARGUMENTS**

<1 đoạn: vai trò + mục tiêu + đầu ra là gì.>

## Nguyên tắc
- <luật cụ thể, lấy từ những lần sửa lưng; mỗi luật 1 dòng, kèm "vì …" nếu không hiển nhiên>

## Quy trình
### 1. <bước>
### 2. <bước>
...

## Đầu ra
<định dạng, tên file, những gì phải có khi bàn giao>

## Khi không nên dùng
<…>
```

Cấu trúc thư mục:
```
<name>/
├── SKILL.md
├── references/   # đọc khi cần (giữ SKILL.md < ~200 dòng)
├── scripts/      # lever chạy được, chỉ đọc nếu có thể
└── templates/    # khung đầu ra
```
