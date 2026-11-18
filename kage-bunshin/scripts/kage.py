#!/usr/bin/env python3
"""kage.py — quản lý một bầy phân thân: mỗi phân thân một worktree, chạy song song, gom báo cáo, dọn sạch.

    kage.py up     --n 5 [--run ID] [--base HEAD] [--repo .]     tạo N worktree (hoặc N thư mục nếu không phải repo git)
    kage.py shard  --n 5 [paths...] [--ext .py,.ts]               chia file thành N phần cân theo số dòng -> JSON
    kage.py run    --run ID --tasks tasks.jsonl [--model haiku]   chạy headless `claude -p` trong từng worktree
    kage.py status --run ID                                       worktree nào bẩn, có commit, đã có báo cáo
    kage.py collect --run ID                                      gom báo cáo + khối JSON của từng phân thân
    kage.py down   --run ID [--purge]                             dọn: giết tiến trình, cất patch, gỡ worktree + nhánh
    kage.py gc     [--yes]                                        tìm worktree mồ côi của các lần chạy cũ và dọn

Mọi thứ nằm ngoài repo, ở ${KAGE_HOME:-~/.cache/kage}/<repo>-<hash>/<run>/, nên không làm bẩn git status.
"""
import argparse, concurrent.futures as cf, datetime as dt, hashlib, json, os, re, shlex, shutil
import signal, subprocess as sp, sys, time
from pathlib import Path

KAGE_HOME = Path(os.environ.get("KAGE_HOME", Path.home() / ".cache" / "kage"))
BRANCH_PREFIX = "kage/"
DEFAULT_TOOLS = "Read,Grep,Glob,LS,Bash,Edit,Write,WebSearch,WebFetch"


def sh(cmd, cwd=None, check=True):
    r = sp.run(cmd, cwd=cwd, stdout=sp.PIPE, stderr=sp.PIPE, encoding="utf-8", errors="replace")
    if check and r.returncode:
        sys.exit(f"lỗi: {' '.join(map(str, cmd))}\n{r.stderr.strip()}")
    return r.stdout.strip()


def repo_root(path):
    r = sp.run(["git", "rev-parse", "--show-toplevel"], cwd=path, stdout=sp.PIPE, stderr=sp.DEVNULL, encoding="utf-8")
    return Path(r.stdout.strip()) if r.returncode == 0 else None


def home_for(base):
    base = Path(base).resolve()
    tag = hashlib.sha1(str(base).encode()).hexdigest()[:8]
    return KAGE_HOME / f"{base.name}-{tag}"


def run_dir(args):
    root = repo_root(args.repo) or Path(args.repo).resolve()
    if not args.run:
        runs = sorted(home_for(root).glob("*/manifest.json"), key=lambda p: p.stat().st_mtime)
        if not runs:
            sys.exit("chưa có lần chạy nào; dùng `kage.py up` trước")
        return runs[-1].parent
    return home_for(root) / args.run


def load(rd):
    mf = rd / "manifest.json"
    if not mf.exists():
        sys.exit(f"không thấy {mf}")
    return json.loads(mf.read_text())


def save(rd, m):
    (rd / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- up
def cmd_up(a):
    root = repo_root(a.repo)
    base_dir = root or Path(a.repo).resolve()
    run = a.run or dt.datetime.now().strftime("%m%d-%H%M%S")
    rd = home_for(base_dir) / run
    if (rd / "manifest.json").exists():
        sys.exit(f"run {run} đã tồn tại ở {rd}")
    (rd / "reports").mkdir(parents=True)
    m = {"run": run, "root": str(base_dir), "mode": "git" if root else "dir", "created": time.time(), "clones": []}
    base_sha = sh(["git", "rev-parse", a.base], cwd=root) if root else None
    m["base"] = base_sha
    for i in range(1, a.n + 1):
        wt = rd / f"clone-{i:02d}"
        c = {"i": i, "path": str(wt), "port": a.port + i, "pid": None}
        if root:
            br = f"{BRANCH_PREFIX}{run}/{i:02d}"
            sh(["git", "worktree", "add", "-q", "-b", br, str(wt), base_sha], cwd=root)
            c["branch"] = br
        else:
            wt.mkdir()
        (wt / ".kage-profile").mkdir(exist_ok=True)   # hồ sơ trình duyệt riêng cho Playwright/Chrome
        if root:  # giấu thư mục profile khỏi git status của worktree
            gd = Path(sh(["git", "rev-parse", "--git-dir"], cwd=wt))
            gd = gd if gd.is_absolute() else wt / gd
            (gd / "info").mkdir(exist_ok=True)
            with open(gd / "info" / "exclude", "a") as f:
                f.write("\n.kage-profile/\nKAGE_REPORT.md\n")
        m["clones"].append(c)
    save(rd, m)
    print(json.dumps({"run": run, "dir": str(rd), "mode": m["mode"],
                      "clones": [{k: c[k] for k in ("i", "path", "port", "branch") if k in c} for c in m["clones"]]},
                     ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- shard
CODE_EXT = ".py,.js,.jsx,.ts,.tsx,.rs,.go,.java,.kt,.rb,.php,.cs,.c,.cc,.cpp,.h,.hpp,.swift,.scala,.sql,.vue,.svelte"


def cmd_shard(a):
    root = repo_root(a.repo)
    exts = tuple(e.strip() for e in a.ext.split(",") if e.strip())
    if root and not a.paths:
        files = [root / f for f in sh(["git", "ls-files"], cwd=root).splitlines()]
    else:
        files = []
        for p in (a.paths or ["."]):
            p = Path(p)
            files += [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file() and ".git" not in f.parts]
    files = [f for f in files if f.suffix in exts and f.exists()]
    sized = []
    for f in files:
        try:
            sized.append((sum(1 for _ in open(f, "rb")), f))
        except OSError:
            pass
    # gom theo thư mục để mỗi phân thân đọc một vùng liền mạch, rồi tham lam: nhóm lớn nhất vào phần nhẹ nhất
    groups = {}
    for n, f in sized:
        groups.setdefault(str(f.parent), []).append((n, f))
    buckets = [{"lines": 0, "files": []} for _ in range(a.n)]
    for _, items in sorted(groups.items(), key=lambda kv: -sum(n for n, _ in kv[1])):
        total = sum(n for n, _ in items)
        if total > max(1, sum(n for n, _ in sized) // a.n):   # thư mục quá to thì xé lẻ
            for n, f in sorted(items, key=lambda x: -x[0]):
                b = min(buckets, key=lambda b: b["lines"]); b["lines"] += n; b["files"].append(str(f))
        else:
            b = min(buckets, key=lambda b: b["lines"]); b["lines"] += total; b["files"] += [str(f) for _, f in items]
    base = root or Path.cwd()
    for b in buckets:
        b["files"] = sorted(os.path.relpath(f, base) for f in b["files"])
    print(json.dumps(buckets, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- run
def _one(c, task, a, rd):
    out = rd / "reports" / f"clone-{c['i']:02d}.md"
    prompt = task["prompt"]
    model = task.get("model", a.model)
    tools = task.get("tools", a.tools)
    cmd = shlex.split(a.cmd.format(model=model)) + ["--allowedTools", tools]
    env = dict(os.environ, KAGE_RUN=rd.name, KAGE_CLONE=str(c["i"]), KAGE_PORT=str(c["port"]),
               KAGE_PROFILE=str(Path(c["path"]) / ".kage-profile"), KAGE_OUT=str(out))
    t0 = time.time()
    with open(out, "w") as fo:
        p = sp.Popen(cmd, cwd=c["path"], stdin=sp.PIPE, stdout=fo, stderr=sp.STDOUT, text=True, env=env,
                     start_new_session=True)
        c["pid"] = p.pid
        try:
            p.communicate(prompt, timeout=task.get("timeout", a.timeout))
            status = "done" if p.returncode == 0 else f"exit {p.returncode}"
        except sp.TimeoutExpired:
            os.killpg(p.pid, signal.SIGTERM); p.wait()
            status = "timeout"
    c["pid"] = None
    return c["i"], status, round(time.time() - t0, 1)


def cmd_run(a):
    rd = run_dir(a)
    m = load(rd)
    tasks = [json.loads(l) for l in open(a.tasks) if l.strip()]
    clones = m["clones"]
    if len(tasks) > len(clones):
        sys.exit(f"{len(tasks)} task nhưng chỉ có {len(clones)} phân thân")
    pairs = list(zip(clones, tasks))
    for c, t in pairs:
        (rd / "reports" / f"clone-{c['i']:02d}.task.json").write_text(json.dumps(t, ensure_ascii=False, indent=2))
    with cf.ThreadPoolExecutor(max_workers=a.parallel or len(pairs)) as ex:
        futs = [ex.submit(_one, c, t, a, rd) for c, t in pairs]
        time.sleep(0.5); save(rd, m)   # ghi pid để `down` giết được nếu bị ngắt giữa chừng
        for f in cf.as_completed(futs):
            i, st, sec = f.result()
            print(f"clone-{i:02d}: {st} ({sec}s)")
    save(rd, m)


# ---------------------------------------------------------------- status / collect
def clone_state(m, c):
    s = {"i": c["i"], "path": c["path"], "exists": Path(c["path"]).exists()}
    if m["mode"] == "git" and s["exists"]:
        s["dirty"] = bool(sh(["git", "status", "--porcelain"], cwd=c["path"], check=False))
        s["commits"] = int(sh(["git", "rev-list", "--count", f"{m['base']}..{c['branch']}"], cwd=m["root"], check=False) or 0)
    return s


def cmd_status(a):
    rd = run_dir(a); m = load(rd)
    for c in m["clones"]:
        s = clone_state(m, c)
        rep = rd / "reports" / f"clone-{c['i']:02d}.md"
        own = Path(c["path"]) / "KAGE_REPORT.md"
        print(f"clone-{c['i']:02d}  exists={s['exists']}  dirty={s.get('dirty', '-')}  commits={s.get('commits', '-')}"
              f"  report={'yes' if (rep.exists() and rep.stat().st_size) or own.exists() else 'no'}  {c['path']}")


JSON_BLOCK = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)


def cmd_collect(a):
    rd = run_dir(a); m = load(rd)
    merged, seen, rows = [], set(), []
    for c in m["clones"]:
        texts = []
        for p in (rd / "reports" / f"clone-{c['i']:02d}.md", Path(c["path"]) / "KAGE_REPORT.md"):
            if p.exists():
                texts.append(p.read_text(errors="replace"))
        text = "\n".join(texts)
        if (Path(c["path"]) / "KAGE_REPORT.md").exists():   # cất lại trước khi worktree bị gỡ
            shutil.copy(Path(c["path"]) / "KAGE_REPORT.md", rd / "reports" / f"clone-{c['i']:02d}.own.md")
        blocks = JSON_BLOCK.findall(text)
        data = {}
        if blocks:
            try:
                data = json.loads(blocks[-1])
            except json.JSONDecodeError:
                data = {"status": "bad-json"}
        st = clone_state(m, c)
        rows.append({"i": c["i"], "status": data.get("status", "no-json" if text else "no-report"),
                     "findings": len(data.get("findings", [])), "commits": st.get("commits", 0), "dirty": st.get("dirty", False)})
        for f in data.get("findings", []):
            key = (f.get("key") or f.get("title") or json.dumps(f, sort_keys=True)).strip().lower()
            if key in seen:
                for g in merged:
                    if g["_key"] == key:
                        g["clones"].append(c["i"])
                continue
            seen.add(key)
            merged.append(dict(f, _key=key, clones=[c["i"]]))
    for g in merged:
        g.pop("_key")
    out = {"run": m["run"], "clones": rows, "findings": merged}
    (rd / "summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"| clone | status | findings | commits | dirty |\n|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['i']:02d} | {r['status']} | {r['findings']} | {r['commits']} | {r['dirty']} |")
    print(f"\n{len(merged)} phát hiện sau khi gộp trùng -> {rd / 'summary.json'}")


# ---------------------------------------------------------------- down / gc
def kill(pid):
    try:
        os.killpg(pid, signal.SIGTERM); time.sleep(1); os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def teardown(root, path, branch, base, salvage):
    """Cất mọi thay đổi chưa gom thành patch, rồi gỡ worktree và nhánh. Trả về mô tả những gì đã cất."""
    kept = []
    salvage.mkdir(parents=True, exist_ok=True)
    name = Path(path).name
    if Path(path).exists() and root:
        if sh(["git", "status", "--porcelain"], cwd=path, check=False):
            sh(["git", "add", "-A"], cwd=path, check=False)
            diff = sh(["git", "diff", "--cached", "--binary"], cwd=path, check=False)
            if diff:
                (salvage / f"{name}.uncommitted.patch").write_text(diff + "\n"); kept.append("uncommitted")
        sh(["git", "worktree", "remove", "--force", path], cwd=root, check=False)
    if Path(path).exists():
        shutil.rmtree(path, ignore_errors=True)
    if root and branch and sh(["git", "rev-parse", "--verify", "-q", branch], cwd=root, check=False):
        if base and sh(["git", "rev-list", "--count", f"{base}..{branch}"], cwd=root, check=False) not in ("", "0"):
            patch = sh(["git", "format-patch", "--stdout", f"{base}..{branch}"], cwd=root, check=False)
            (salvage / f"{name}.commits.patch").write_text(patch + "\n"); kept.append("commits")
        sh(["git", "branch", "-D", branch], cwd=root, check=False)
    return kept


def cmd_down(a):
    rd = run_dir(a); m = load(rd)
    root = m["root"] if m["mode"] == "git" else None
    for c in m["clones"]:
        if c.get("pid"):
            kill(c["pid"])
        kept = teardown(root, c["path"], c.get("branch"), m.get("base"), rd / "salvage")
        print(f"clone-{c['i']:02d}: đã gỡ" + (f" (cất {', '.join(kept)} vào salvage/)" if kept else ""))
    if root:
        sh(["git", "worktree", "prune"], cwd=root, check=False)
    if a.purge:
        shutil.rmtree(rd, ignore_errors=True); print(f"đã xóa {rd}")
    else:
        m["closed"] = time.time(); save(rd, m)
        print(f"báo cáo và patch còn ở {rd} (thêm --purge để xóa hẳn)")
    left = [l for l in sh(["git", "worktree", "list"], cwd=root, check=False).splitlines() if str(rd) in l] if root else []
    if left:
        sys.exit("còn worktree chưa gỡ được:\n" + "\n".join(left))


def cmd_gc(a):
    root = repo_root(a.repo)
    if not root:
        sys.exit("gc chỉ dùng trong repo git")
    pats = [str(KAGE_HOME)] + [p for p in a.also.split(",") if p]
    raw = sh(["git", "worktree", "list", "--porcelain"], cwd=root)
    found = []
    for blk in raw.split("\n\n"):
        f = dict(l.split(" ", 1) for l in blk.splitlines() if " " in l)
        path, br = f.get("worktree", ""), f.get("branch", "").replace("refs/heads/", "")
        if path == str(root):
            continue
        if any(p in path for p in pats) or br.startswith(BRANCH_PREFIX):
            found.append((path, br))
    orphan_br = [b for b in sh(["git", "for-each-ref", "--format=%(refname:short)", f"refs/heads/{BRANCH_PREFIX}"], cwd=root).splitlines()
                 if b not in {br for _, br in found}]
    if not found and not orphan_br:
        print("sạch: không có worktree hay nhánh phân thân nào sót lại"); return
    for p, b in found:
        print(f"worktree  {p}  [{b}]")
    for b in orphan_br:
        print(f"nhánh mồ côi  {b}")
    if not a.yes:
        print("\nchạy lại với --yes để dọn (thay đổi chưa gom được cất vào salvage/)"); return
    base = sh(["git", "rev-parse", "HEAD"], cwd=root)
    salvage = home_for(root) / "gc-salvage"
    for p, b in found:
        print(p, "->", teardown(root, p, b, base, salvage) or "đã gỡ")
    for b in orphan_br:
        print(b, "->", teardown(root, "/nonexistent", b, base, salvage) or "đã xóa")
    sh(["git", "worktree", "prune"], cwd=root, check=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def p(name, fn):
        s = sub.add_parser(name); s.set_defaults(fn=fn); s.add_argument("--repo", default="."); return s

    s = p("up", cmd_up); s.add_argument("--n", type=int, required=True); s.add_argument("--run")
    s.add_argument("--base", default="HEAD"); s.add_argument("--port", type=int, default=4100)
    s = p("shard", cmd_shard); s.add_argument("--n", type=int, required=True); s.add_argument("paths", nargs="*")
    s.add_argument("--ext", default=CODE_EXT)
    s = p("run", cmd_run); s.add_argument("--run"); s.add_argument("--tasks", required=True)
    s.add_argument("--model", default="haiku"); s.add_argument("--tools", default=DEFAULT_TOOLS)
    s.add_argument("--timeout", type=int, default=900); s.add_argument("--parallel", type=int)
    s.add_argument("--cmd", default="claude -p --model {model}", help="lệnh headless, prompt đi qua stdin")
    for name, fn in (("status", cmd_status), ("collect", cmd_collect)):
        s = p(name, fn); s.add_argument("--run")
    s = p("down", cmd_down); s.add_argument("--run"); s.add_argument("--purge", action="store_true")
    s = p("gc", cmd_gc); s.add_argument("--yes", action="store_true")
    s.add_argument("--also", default="", help="mẫu đường dẫn khác cũng coi là phân thân, vd .claude/worktrees (chỉ khi chắc không phiên nào đang dùng)")
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
