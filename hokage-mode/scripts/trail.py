#!/usr/bin/env python3
"""trail.py — sổ nhiệm vụ của hokage-mode: chụp hiện trạng lúc nhận việc, ghi từng bước, tiếp tục sau khi đứt mạch, và dọn sạch dấu vết.

    trail.py start  --mode shinobi|sage|bruiser --goal "..." [--done "<điều kiện xong>"]
    trail.py note   <plan|step|hyp|check|decision|checkpoint|blocked> "<nội dung>" [--test ".."] [--result ".."] [--verdict ..]
    trail.py show   [--last 20]          in sổ dạng bảng
    trail.py resume                      in mục tiêu, điều kiện xong, checkpoint cuối và các bước gần nhất (dùng sau compact / phiên mới)
    trail.py sweep  [--keep GLOB ...] [--yes] [--purge]
                                         so với lúc start: file/thư mục mới không phải doc, worktree mới, nhánh mới,
                                         tiến trình mới đang nghe cổng. Không có --yes thì chỉ liệt kê.
                                         File bị dọn được chuyển vào thùng rác ngoài repo (tự xóa sau 7 ngày, --purge xóa ngay).
    trail.py end                         đóng sổ

Sổ nằm ở ${HOKAGE_HOME:-~/.cache/hokage}/<repo>-<hash>/<id>/, ngoài repo.
"""
import argparse, fnmatch, hashlib, json, os, re, shutil, signal, subprocess as sp, sys, time
from pathlib import Path

HOME = Path(os.environ.get("HOKAGE_HOME", Path.home() / ".cache" / "hokage"))
DOCS = ["*.md", "*.mdx", "*.rst", "*.adoc", "docs/*", "doc/*", "docs", "doc"]
KINDS = ["plan", "step", "hyp", "check", "decision", "checkpoint", "blocked"]


def sh(cmd, cwd=None):
    r = sp.run(cmd, cwd=cwd, stdout=sp.PIPE, stderr=sp.DEVNULL, encoding="utf-8", errors="replace")
    return r.stdout.strip() if r.returncode == 0 else ""


def root_of(cwd="."):
    r = sh(["git", "rev-parse", "--show-toplevel"], cwd)
    return Path(r) if r else Path(cwd).resolve()


def store(root):
    return HOME / f"{root.name}-{hashlib.sha1(str(root).encode()).hexdigest()[:8]}"


def current(root):
    p = store(root) / "current"
    if not p.exists():
        sys.exit("chưa có sổ nào đang mở; chạy `trail.py start` trước")
    d = store(root) / p.read_text().strip()
    return d, json.loads((d / "trail.json").read_text())


# ---------------------------------------------------------------- snapshot
def snap_files(root, git):
    if git:  # --directory gom thư mục chưa track thành một dòng; không --exclude-standard để thấy cả file bị ignore (build, cache)
        return sorted(set(sh(["git", "ls-files", "--others", "--directory"], root).splitlines()))
    out = []
    for p in root.iterdir():
        out.append(p.name + ("/" if p.is_dir() else ""))
        if p.is_dir() and not p.name.startswith("."):
            try:
                out += [f"{p.name}/{q.name}" + ("/" if q.is_dir() else "") for q in p.iterdir()]
            except OSError:
                pass
    return sorted(out)


def snap_ports():
    out = sh(["ss", "-ltnpH"])
    res = []
    for line in out.splitlines():
        m = re.search(r":(\d+)\s", line.split()[3] + " ") if len(line.split()) > 3 else None
        for name, pid in re.findall(r'\("([^"]+)",pid=(\d+)', line):
            res.append({"port": int(m.group(1)) if m else 0, "pid": int(pid), "name": name})
    return res


def snapshot(root):
    git = (root / ".git").exists()
    s = {"git": git, "files": snap_files(root, git), "ports": snap_ports()}
    if git:
        s["head"] = sh(["git", "rev-parse", "HEAD"], root)
        s["branches"] = sh(["git", "for-each-ref", "--format=%(refname:short)", "refs/heads"], root).splitlines()
        s["worktrees"] = [l[9:] for l in sh(["git", "worktree", "list", "--porcelain"], root).splitlines() if l.startswith("worktree ")]
    return s


# ---------------------------------------------------------------- commands
def cmd_start(a):
    root = root_of()
    tid = time.strftime("%m%d-%H%M%S")
    d = store(root) / tid
    d.mkdir(parents=True)
    t = {"id": tid, "root": str(root), "mode": a.mode, "goal": a.goal, "done": a.done, "started": time.time(),
         "baseline": snapshot(root)}
    (d / "trail.json").write_text(json.dumps(t, ensure_ascii=False, indent=1))
    (d / "ledger.tsv").write_text("time\tkind\ttext\ttest\tresult\tverdict\n")
    (store(root) / "current").write_text(tid)
    print(f"sổ {tid} [{a.mode}] mở ở {d}")


def cmd_note(a):
    d, _ = current(root_of())
    clean = lambda s: (s or "").replace("\t", " ").replace("\n", " ")
    with open(d / "ledger.tsv", "a") as f:
        f.write("\t".join([time.strftime("%H:%M:%S"), a.kind, clean(a.text), clean(a.test), clean(a.result), clean(a.verdict)]) + "\n")


def rows(d):
    lines = (d / "ledger.tsv").read_text().splitlines()[1:]
    return [dict(zip(["time", "kind", "text", "test", "result", "verdict"], l.split("\t"))) for l in lines if l]


def table(rs):
    out = ["| giờ | loại | nội dung | kiểm bằng | kết quả | kết luận |", "|---|---|---|---|---|---|"]
    out += [f"| {r['time']} | {r['kind']} | {r['text']} | {r.get('test', '')} | {r.get('result', '')} | {r.get('verdict', '')} |" for r in rs]
    return "\n".join(out)


def cmd_show(a):
    d, t = current(root_of())
    print(f"**{t['mode']}** · {t['goal']}" + (f" · xong khi: {t['done']}" if t.get("done") else ""))
    print(table(rows(d)[-a.last:]))


def cmd_resume(a):
    d, t = current(root_of())
    rs = rows(d)
    cps = [r for r in rs if r["kind"] == "checkpoint"]
    text = "\n".join([
        f"# Tiếp tục nhiệm vụ {t['id']} [{t['mode']}]",
        f"- Mục tiêu: {t['goal']}",
        f"- Xong khi: {t.get('done') or '(chưa ghi)'}",
        f"- Checkpoint cuối: {cps[-1]['text'] if cps else '(chưa có)'}",
        f"- Bị chặn: " + ("; ".join(r["text"] for r in rs if r["kind"] == "blocked") or "không"),
        "", "## 10 dòng cuối", table(rs[-10:]),
    ])
    (d / "resume.md").write_text(text + "\n")
    print(text)


def matches(path, pats):
    p = path.rstrip("/")
    return any(fnmatch.fnmatch(p, g) or fnmatch.fnmatch(Path(p).name, g) for g in pats)


def purge_old(base, days=7):
    for x in base.glob("*"):
        if x.is_dir() and time.time() - x.stat().st_mtime > days * 86400:
            shutil.rmtree(x, ignore_errors=True)


def cmd_sweep(a):
    root = root_of()
    d, t = current(root)
    b, now = t["baseline"], snapshot(root)
    keep = DOCS + (a.keep or [])
    trash = store(root) / "trash" / t["id"]
    # file/thư mục mới: chỉ thứ không có lúc start; thư mục chưa track có từ trước thì không đụng vào bên trong
    old = set(b["files"])
    new_files = [f for f in now["files"] if f not in old and not any(f.startswith(o) for o in old if o.endswith("/"))]
    junk = [f for f in new_files if not matches(f, keep)]
    kept = [f for f in new_files if matches(f, keep)]
    new_wt = [w for w in now.get("worktrees", []) if w not in b.get("worktrees", [])]
    cur_br = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], root) if b["git"] else ""
    new_br = [x for x in now.get("branches", []) if x not in b.get("branches", []) and x != cur_br]
    old_pids = {p["pid"] for p in b["ports"]}
    new_ports = [p for p in now["ports"] if p["pid"] not in old_pids]
    dirty = sh(["git", "status", "--porcelain", "--untracked-files=no"], root) if b["git"] else ""

    print(f"## Dọn dấu vết nhiệm vụ {t['id']} [{t['mode']}]")
    for title, items in (("file/thư mục rác", junk), ("worktree mới", new_wt), ("nhánh mới", new_br),
                         ("tiến trình mới đang nghe cổng", [f"{p['name']} pid={p['pid']} :{p['port']}" for p in new_ports])):
        print(f"- {title}: " + (", ".join(items) if items else "không"))
    if kept:
        print(f"- giữ lại (doc / --keep): {', '.join(kept)}")
    if dirty:
        print(f"- CẢNH BÁO: file đã track còn thay đổi chưa commit, không đụng tới:\n  " + dirty.replace("\n", "\n  "))
    if not a.yes:
        print("\n(chỉ liệt kê; thêm --yes để dọn. File được chuyển vào thùng rác, không xóa ngay)")
        return
    trash.mkdir(parents=True, exist_ok=True)
    for p in new_ports:
        try:
            os.kill(p["pid"], signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
    for w in new_wt:
        name = Path(w).name
        diff = sh(["git", "-C", w, "diff", "HEAD", "--binary"])
        if diff:
            (trash / f"worktree-{name}.patch").write_text(diff + "\n")
        sp.run(["git", "worktree", "remove", "--force", w], cwd=root, stderr=sp.DEVNULL)
    for br in new_br:
        unmerged = sh(["git", "rev-list", "--count", f"HEAD..{br}"], root)
        if unmerged not in ("", "0"):
            (trash / f"branch-{br.replace('/', '_')}.patch").write_text(
                sh(["git", "format-patch", "--stdout", f"{b['head']}..{br}"], root) + "\n")
        sp.run(["git", "branch", "-D", br], cwd=root, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    for f in junk:
        src = root / f.rstrip("/")
        if src.exists() or src.is_symlink():
            dst = trash / "files" / f.rstrip("/")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
    if b["git"]:
        sp.run(["git", "worktree", "prune"], cwd=root)
    purge_old(store(root) / "trash")
    if a.purge:
        shutil.rmtree(trash, ignore_errors=True)
        print("đã dọn và xóa hẳn")
    else:
        print(f"đã dọn; thứ bị dọn nằm ở {trash} (tự xóa sau 7 ngày)")


def cmd_end(a):
    root = root_of()
    d, t = current(root)
    t["ended"] = time.time()
    (d / "trail.json").write_text(json.dumps(t, ensure_ascii=False, indent=1))
    (store(root) / "current").unlink()
    print(f"đóng sổ {t['id']} sau {round((t['ended'] - t['started']) / 60, 1)} phút; sổ còn ở {d}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.set_defaults(fn=cmd_start)
    s.add_argument("--mode", required=True, choices=["shinobi", "sage", "bruiser", "hokage"])
    s.add_argument("--goal", required=True); s.add_argument("--done", default="")
    s = sub.add_parser("note"); s.set_defaults(fn=cmd_note)
    s.add_argument("kind", choices=KINDS); s.add_argument("text")
    for o in ("--test", "--result", "--verdict"):
        s.add_argument(o, default="")
    s = sub.add_parser("show"); s.set_defaults(fn=cmd_show); s.add_argument("--last", type=int, default=20)
    sub.add_parser("resume").set_defaults(fn=cmd_resume)
    s = sub.add_parser("sweep"); s.set_defaults(fn=cmd_sweep)
    s.add_argument("--keep", action="append"); s.add_argument("--yes", action="store_true"); s.add_argument("--purge", action="store_true")
    sub.add_parser("end").set_defaults(fn=cmd_end)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
