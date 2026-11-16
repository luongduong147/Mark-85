# Cho skill tự chạy khi có PR/MR mới

Ba mức, từ nhẹ tới nặng. Chọn mức thấp nhất đáp ứng được nhu cầu.

## 1. Cục bộ, theo yêu cầu
Trong Claude Code hoặc dsh, gõ `/dont-ship-shit 123`. Không cần cài thêm gì.

## 2. Cục bộ, theo lịch
Dùng `/loop` (Claude Code) để quét định kỳ các PR/MR đang mở nhắm vào nhánh của bạn:
```
/loop 30m liệt kê PR/MR mở nhắm vào <nhánh> chưa có .dss/<id>/REPORT.md, chạy /dont-ship-shit cho từng cái
```
Cần `gh` hoặc `glab` đã đăng nhập để liệt kê PR/MR.

## 3. Trong CI
Chạy Claude Code ở chế độ không tương tác (`claude -p`). Báo cáo được lưu thành artifact. Có đăng comment hay không thì bạn tự quyết bằng một bước riêng. API key để trong secret của CI, không bao giờ ghi vào file.

GitHub Actions (`.github/workflows/dont-ship-shit.yml`):
```yaml
on:
  pull_request:
    branches: [main]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0, submodules: recursive }
      - run: npm i -g @anthropic-ai/claude-code
      - run: git clone --depth 1 https://github.com/luongduong147/Mark-85.git /tmp/mark85 && mkdir -p ~/.claude/skills && ln -s /tmp/mark85/dont-ship-shit ~/.claude/skills/
      - run: claude -p "/dont-ship-shit ${{ github.event.pull_request.number }} --base ${{ github.base_ref }}" --allowedTools "Bash,Read,Grep,Glob,Write"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ github.token }}
      - uses: actions/upload-artifact@v4
        with: { name: dss-report, path: .dss/**/REPORT.md }
```

GitLab CI (`.gitlab-ci.yml`):
```yaml
dont-ship-shit:
  image: node:22
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  variables:
    GIT_DEPTH: 0
  script:
    - npm i -g @anthropic-ai/claude-code
    - git clone --depth 1 https://github.com/luongduong147/Mark-85.git /tmp/mark85 && mkdir -p ~/.claude/skills && ln -s /tmp/mark85/dont-ship-shit ~/.claude/skills/
    - claude -p "/dont-ship-shit !$CI_MERGE_REQUEST_IID --base $CI_MERGE_REQUEST_TARGET_BRANCH_NAME --platform gitlab" --allowedTools "Bash,Read,Grep,Glob,Write"
  artifacts:
    paths: [.dss/]
```
`ANTHROPIC_API_KEY` đặt trong Settings → CI/CD → Variables, chọn masked và protected.

Lưu ý:
- Job CI chỉ nên **báo cáo**. Đặt nó thành required check chỉ khi bạn đã tin phán quyết qua vài chục PR.
- Không cho job quyền push. `GH_TOKEN` mặc định của Actions đủ để đọc PR.
- Pin phiên bản Claude Code và commit của Mark-85 khi đã ổn định, tránh hành vi đổi ngầm.
