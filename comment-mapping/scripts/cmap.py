#!/usr/bin/env python3
"""cmap.py — quét, tìm, dựng lịch sử và lint các comment block [CMAP] trong repo.

Chỉ đọc, chỉ dùng thư viện chuẩn.

Usage:
    python cmap.py scan    <root> [--json]
    python cmap.py find    <root> <query...> [--json]
    python cmap.py history <root> <module-or-path> [--json]
    python cmap.py lint    <root>
    python cmap.py next-id <root> <module>

Định dạng block (prefix comment bất kỳ: #, //, --, ;, *, <!--):
    # [CMAP] auth-003 | FIX | Token refresh race
    #   Ref:     spec=docs/SPEC.md#4.2 plan=docs/PLAN.md#P2 task=T-014
    #   When:    found=2026-11-10 fixed=2026-11-13
    #   Why:     ...
    #   Impact:  ...
    #   How:     ...  (dòng tiếp theo thụt sâu hơn được nối vào field trước)
    #   Updated: 2026-11-13
"""
import argparse, json, os, re, subprocess, sys, unicodedata

SKIP_DIRS = {'.git', 'node_modules', 'dist', 'build', 'target', '.venv', 'venv', '__pycache__',
             '.next', 'coverage', 'vendor', '.mypy_cache', '.pytest_cache'}
TEXT_EXT = {'.py', '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.rs', '.go', '.java', '.kt', '.rb',
            '.php', '.cs', '.c', '.cc', '.cpp', '.h', '.hpp', '.swift', '.sql', '.vue', '.svelte',
            '.sh', '.bash', '.ps1', '.yaml', '.yml', '.toml', '.lua', '.html', '.css', '.scss', '.md'}
PREFIX = r'^\s*(?:#|//|--|;|\*|/\*|<!--)?\s*'
HEAD_RE = re.compile(PREFIX + r'\[CMAP\]\s+(?P<id>[\w.\-/]+)\s*\|\s*(?P<status>[A-Z]+)\s*\|\s*(?P<title>.*?)\s*(?:-->|\*/)?\s*$')
FIELD_RE = re.compile(PREFIX + r'(?P<key>Ref|When|Why|Impact|How|Updated|Supersedes|Author)\s*:\s*(?P<val>.*?)\s*(?:-->|\*/)?\s*$')
CONT_RE = re.compile(r'^\s*(?:#|//|--|;|\*)\s{3,}(?P<val>\S.*?)\s*$')
COMMENT_RE = re.compile(r'^\s*(?:#|//|--|;|\*|/\*|<!--)')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')
STATUSES = {'NEW', 'FIX', 'CHANGE', 'REFACTOR', 'DEPRECATED'}
REQUIRED = {'NEW': ['Ref', 'When', 'Why', 'How'],
            'DEFAULT': ['Ref', 'When', 'Why', 'Impact', 'How']}


def iter_files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if os.path.splitext(fn)[1].lower() in TEXT_EXT:
                yield os.path.join(dp, fn)


def parse_file(path, root):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            lines = f.read().splitlines()
    except OSError:
        return []
    blocks, cur, last_key = [], None, None
    for i, line in enumerate(lines, 1):
        m = HEAD_RE.match(line)
        if m:
            cur = {'id': m['id'], 'status': m['status'], 'title': m['title'],
                   'file': os.path.relpath(path, root), 'line': i, 'fields': {}}
            blocks.append(cur)
            last_key = None
            continue
        if cur is None:
            continue
        fm = FIELD_RE.match(line)
        if fm:
            last_key = fm['key']
            cur['fields'][last_key] = fm['val']
            continue
        cm = CONT_RE.match(line)
        if cm and last_key:
            cur['fields'][last_key] += ' ' + cm['val']
            continue
        if not COMMENT_RE.match(line) or not line.strip():
            cur, last_key = None, None
    for b in blocks:
        b['code_line'] = _first_code_line(lines, b['line'])
        dates = DATE_RE.findall(b['fields'].get('Updated', '') + ' ' + b['fields'].get('When', ''))
        b['date'] = max(dates) if dates else ''
    return blocks


def _first_code_line(lines, start):
    for j in range(start, len(lines)):
        if lines[j].strip() and not COMMENT_RE.match(lines[j]):
            return j + 1
    return None


def scan(root):
    out = []
    for p in iter_files(root):
        out.extend(parse_file(p, root))
    return out


def fmt(b):
    f = b['fields']
    return (f"{b['file']}:{b['line']}  [{b['id']}] {b['status']} {b['title']}  ({b['date'] or 'no-date'})\n"
            f"    Ref: {f.get('Ref', '-')}\n    Why: {f.get('Why', '-')}\n    How: {f.get('How', '-')}")


STOP = {'tim', 'doan', 'code', 'xu', 'ly', 'viec', 'nay', 'cho', 'cua', 'la', 'o', 'dau', 'nao',
        'find', 'the', 'where', 'which', 'handles', 'handle'}


def norm(s):
    s = unicodedata.normalize('NFD', s.lower().replace('đ', 'd'))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def cmd_find(root, terms):
    words = [w for w in re.findall(r'\w+', norm(' '.join(terms))) if w not in STOP] or \
            re.findall(r'\w+', norm(' '.join(terms)))
    need = max(1, (len(set(words)) + 1) // 2)
    hits = []
    for b in scan(root):
        hay = norm(' '.join([b['id'], b['title'], b['file']] + list(b['fields'].values())))
        matched = {w for w in words if w in hay}
        if len(matched) >= need:
            hits.append((len(matched), sum(hay.count(w) for w in matched), b))
    hits.sort(key=lambda x: (-x[0], -x[1]))
    return [b for _, _, b in hits]


def cmd_history(root, target):
    t = target.strip('/').lower()
    blocks = [b for b in scan(root)
              if b['id'].lower().startswith(t) or b['file'].lower().startswith(t) or t in b['file'].lower()]
    blocks.sort(key=lambda b: (b['date'], b['id']))
    git = ''
    path = os.path.join(root, target)
    if os.path.exists(path):
        r = subprocess.run(['git', 'log', '--date=short', '--format=%ad %h %s', '--follow', '--', target]
                           if os.path.isfile(path) else
                           ['git', 'log', '--date=short', '--format=%ad %h %s', '--', target],
                           cwd=root, capture_output=True, text=True)
        git = r.stdout.strip()
    return blocks, git


def cmd_lint(root):
    problems, seen = [], {}
    for b in scan(root):
        loc = f"{b['file']}:{b['line']}"
        if b['status'] not in STATUSES:
            problems.append(f"{loc} status '{b['status']}' không hợp lệ ({'|'.join(sorted(STATUSES))})")
        for k in REQUIRED.get(b['status'], REQUIRED['DEFAULT']):
            if not b['fields'].get(k):
                problems.append(f"{loc} [{b['id']}] thiếu field {k}")
        if not b['date']:
            problems.append(f"{loc} [{b['id']}] không có ngày YYYY-MM-DD trong When/Updated")
        for ref in re.findall(r'(?:spec|plan)=([^\s#|]+)', b['fields'].get('Ref', '')):
            if not os.path.exists(os.path.join(root, ref)):
                problems.append(f"{loc} [{b['id']}] Ref trỏ tới file không tồn tại: {ref}")
        key = (b['id'], b['status'], b['date'])
        if key in seen:
            problems.append(f"{loc} [{b['id']}] trùng block với {seen[key]}")
        seen[key] = loc
    return problems


def cmd_next_id(root, module):
    nums = [int(m.group(1)) for b in scan(root)
            for m in [re.fullmatch(re.escape(module) + r'-(\d+)', b['id'])] if m]
    return f"{module}-{(max(nums) + 1) if nums else 1:03d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['scan', 'find', 'history', 'lint', 'next-id'])
    ap.add_argument('root')
    ap.add_argument('rest', nargs='*')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    root = os.path.abspath(a.root)

    if a.cmd == 'scan':
        res = scan(root)
        res.sort(key=lambda b: (b['file'], b['line']))
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else
              '\n'.join(fmt(b) for b in res) + f"\n\n{len(res)} block(s)")
    elif a.cmd == 'find':
        if not a.rest:
            sys.exit('find cần <query>')
        res = cmd_find(root, a.rest)
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else
              ('\n'.join(fmt(b) for b in res) or 'Không có CMAP block khớp — chuyển sang tìm trong code.'))
    elif a.cmd == 'history':
        if not a.rest:
            sys.exit('history cần <module-or-path>')
        blocks, git = cmd_history(root, a.rest[0])
        if a.json:
            print(json.dumps({'cmap': blocks, 'git': git.splitlines()}, ensure_ascii=False, indent=1))
        else:
            print('## CMAP timeline')
            for b in blocks:
                print(f"- {b['date'] or '????-??-??'} [{b['id']}] {b['status']} {b['title']} — {b['file']}:{b['line']}")
            print('\n## git log\n' + (git or '(không có / không phải git)'))
    elif a.cmd == 'lint':
        probs = cmd_lint(root)
        print('\n'.join(probs) if probs else 'OK: mọi CMAP block hợp lệ')
        sys.exit(1 if probs else 0)
    elif a.cmd == 'next-id':
        if not a.rest:
            sys.exit('next-id cần <module>')
        print(cmd_next_id(root, a.rest[0]))


if __name__ == '__main__':
    main()
