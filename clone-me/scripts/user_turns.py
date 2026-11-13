#!/usr/bin/env python3
"""user_turns.py — rút các lượt NGƯỜI DÙNG gõ (bỏ tool result, system reminder, lệnh nội bộ)
từ transcript Claude Code của MỘT project, để mining convention.

Chỉ đọc, thư viện chuẩn.
Usage:
    python user_turns.py <project-transcript-dir> [--since YYYY-MM-DD] [--max-chars 1500] [--session ID]
    # dir mặc định của project hiện tại: ~/.claude/projects/<cwd với / thay bằng ->
Output: markdown, nhóm theo session, mỗi lượt có timestamp.
"""
import argparse, glob, json, os, re

NOISE = re.compile(r'^\s*<(system-reminder|local-command-caveat|command-name|local-command-stdout|task-notification)')
STRIP = re.compile(r'<system-reminder>.*?</system-reminder>', re.S)


def texts(msg):
    c = msg.get('content')
    if isinstance(c, str):
        yield c
    elif isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get('type') == 'text':
                yield b.get('text', '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--since', default='')
    ap.add_argument('--max-chars', type=int, default=1500)
    ap.add_argument('--session', default='')
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(os.path.expanduser(a.dir), '*.jsonl')), key=os.path.getmtime)
    total = 0
    for f in files:
        sid = os.path.basename(f)[:-6]
        if a.session and not sid.startswith(a.session):
            continue
        rows = []
        with open(f, encoding='utf-8', errors='replace') as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if d.get('type') != 'user' or d.get('isMeta') or d.get('isSidechain'):
                    continue
                ts = d.get('timestamp', '')
                if a.since and ts[:10] < a.since:
                    continue
                for t in texts(d.get('message', {})):
                    t = STRIP.sub('', t).strip()
                    if not t or NOISE.match(t):
                        continue
                    rows.append((ts[:16].replace('T', ' '), t[:a.max_chars]))
        if rows:
            print(f'\n## session {sid} ({len(rows)} lượt)\n')
            for ts, t in rows:
                print(f'- [{ts}] ' + t.replace('\n', '\n  '))
            total += len(rows)
    print(f'\n<!-- {total} lượt người dùng từ {len(files)} file -->')


if __name__ == '__main__':
    main()
