#!/usr/bin/env python3
"""chase_probes.py — quản lý probe CHASE trong code và log.

Usage:
    python chase_probes.py list   <root> [id]            # liệt kê probe (mọi id nếu bỏ trống)
    python chase_probes.py remove <root> <id> [--dry-run] # gỡ mọi dòng/khối mang marker CHASE:<id>
    python chase_probes.py grep   <logfile> <id> [--by-cid]

Marker trong code:  ... # CHASE:<id>       (dòng đơn)
                    # CHASE:<id>:begin ... # CHASE:<id>:end   (khối, gỡ cả hai đầu)
Dòng log:           CHASE[<id>] p=<n> cid=<...> k=v ...
Chỉ dùng thư viện chuẩn. 'remove' là thao tác duy nhất ghi file.
"""
import argparse, collections, os, re, sys

SKIP = {'.git', 'node_modules', 'dist', 'build', 'target', '.venv', 'venv', '__pycache__', '.chase', '.next'}
ANY = re.compile(r'CHASE:([\w.-]+?)(?::(begin|end))?(?![\w-])')


def marker(cid):
    return re.compile(r'CHASE:' + re.escape(cid) + r'(?::(begin|end))?(?![\w.-])')


def files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                if os.path.getsize(p) > 2_000_000:
                    continue
                with open(p, encoding='utf-8') as f:
                    yield p, f.read().splitlines(keepends=True)
            except (UnicodeDecodeError, OSError):
                continue


def plan(lines, rx):
    """Trả về tập index dòng cần xóa + lỗi (begin không có end)."""
    drop, errs, open_at = set(), [], None
    for i, ln in enumerate(lines):
        m = rx.search(ln)
        if open_at is not None:
            drop.add(i)
            if m and m.group(1) == 'end':
                open_at = None
            continue
        if not m:
            continue
        if m.group(1) == 'begin':
            open_at = i
            drop.add(i)
        elif m.group(1) == 'end':
            errs.append(i + 1)
        else:
            drop.add(i)
    if open_at is not None:
        errs.append(open_at + 1)
    return drop, errs


def cmd_list(root, cid):
    by = collections.defaultdict(list)
    for p, lines in files(root):
        for i, ln in enumerate(lines, 1):
            for m in ANY.finditer(ln):
                if cid and m.group(1) != cid:
                    continue
                by[m.group(1)].append(f"{os.path.relpath(p, root)}:{i}  {ln.strip()[:110]}")
    if not by:
        print('0 probe' + (f' cho {cid}' if cid else ''))
    for k, v in sorted(by.items()):
        print(f'## {k}: {len(v)} dòng marker')
        print('\n'.join('  ' + x for x in v))


def cmd_remove(root, cid, dry):
    rx, total, bad = marker(cid), 0, False
    for p, lines in files(root):
        if not any(rx.search(l) for l in lines):
            continue
        drop, errs = plan(lines, rx)
        rel = os.path.relpath(p, root)
        if errs:
            bad = True
            print(f'!! {rel}: begin/end không khớp ở dòng {errs} — bỏ qua file này', file=sys.stderr)
            continue
        print(f'--- {rel}: gỡ {len(drop)} dòng')
        for i in sorted(drop):
            print(f'-{i + 1}: {lines[i].rstrip()}')
        total += len(drop)
        if not dry:
            with open(p, 'w', encoding='utf-8') as f:
                f.writelines(l for i, l in enumerate(lines) if i not in drop)
    print(f"{'(dry-run) ' if dry else ''}tổng {total} dòng")
    sys.exit(2 if bad else 0)


def cmd_grep(logfile, cid, by_cid):
    tag = f'CHASE[{cid}]'
    rows = [l.rstrip('\n') for l in open(logfile, encoding='utf-8', errors='replace') if tag in l]
    if not by_cid:
        print('\n'.join(rows))
    else:
        groups = collections.OrderedDict()
        for r in rows:
            m = re.search(r'\bcid=(\S+)', r)
            groups.setdefault(m.group(1) if m else '(no-cid)', []).append(r)
        for k, v in groups.items():
            print(f'## cid={k} ({len(v)})')
            print('\n'.join('  ' + x for x in v))
    print(f'<!-- {len(rows)} dòng -->', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('cmd', choices=['list', 'remove', 'grep'])
    ap.add_argument('target')
    ap.add_argument('id', nargs='?')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--by-cid', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'list':
        cmd_list(os.path.abspath(a.target), a.id)
    elif not a.id:
        sys.exit(f'{a.cmd} cần <id>')
    elif a.cmd == 'remove':
        cmd_remove(os.path.abspath(a.target), a.id, a.dry_run)
    else:
        cmd_grep(a.target, a.id, a.by_cid)


if __name__ == '__main__':
    main()
