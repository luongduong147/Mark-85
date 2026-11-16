#!/usr/bin/env python3
"""dss.py — dữ liệu tất định cho skill dont-ship-shit. Chỉ đọc repo, không push, không comment.

  dss.py fetch [target] [--base BRANCH] [--remote origin] [--platform github|gitlab] [--out .dss]
      target: số PR/MR (123, #123, !123), URL PR GitHub / MR GitLab, tên nhánh, hoặc bỏ trống (= HEAD hiện tại).
      Tải ref của PR/MR về refs/dss/<id>, tính merge-base, ghi .dss/<id>/diff.patch + summary.json, in summary.
  dss.py dupes <base> <head> [--min-lines 4] [--threshold 0.6] [--me EMAIL] [--top 3]
      Đối chiếu từng khối code được thêm với code đã có ở <base> (khớp nguyên văn + khớp cấu trúc
      sau khi chuẩn hóa tên biến/literal). Khối trùng do chính --me viết sẽ được đánh dấu mine=true.
  dss.py lint <base> <head>
      Cờ trên dòng được thêm/xóa: test bị skip/only, file test bị xóa, assert bị bỏ, dấu hiệu case-fix
      (so sánh với chuỗi/số cứng, nuốt exception, TODO/HACK).
"""
import argparse, json, os, re, subprocess, sys
from collections import defaultdict

CODE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".rs", ".go", ".java", ".kt", ".rb",
            ".php", ".cs", ".c", ".cc", ".cpp", ".h", ".hpp", ".swift", ".scala", ".vue", ".svelte", ".sql", ".sh"}
TEST_RE = re.compile(r"(^|/)(tests?|__tests__|spec|e2e)/|(_test|\.test|\.spec|_spec)\.[a-z]+$|(^|/)test_[^/]+\.py$")
DOC_RE = re.compile(r"\.(md|rst|txt|adoc)$|(^|/)docs?/")
CONF_RE = re.compile(r"\.(ya?ml|toml|json|ini|cfg|lock|env\.example)$|(^|/)(Dockerfile|Makefile)$")


def git(*args, check=True):
    r = subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        sys.exit("git %s thất bại: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def tool(*cmd):
    try:
        r = subprocess.run(list(cmd), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def kind_of(path):
    if TEST_RE.search(path):
        return "test"
    if DOC_RE.search(path):
        return "doc"
    if CONF_RE.search(path):
        return "config"
    return "src" if os.path.splitext(path)[1] in CODE_EXT else "other"


# ---------- fetch ----------
def parse_target(target, remote_url, forced):
    """-> (platform, number|None, branch|None)"""
    platform = forced or ("github" if "github" in remote_url else "gitlab" if "gitlab" in remote_url else None)
    if not target:
        return platform, None, None
    m = re.search(r"github\.com/.+/pull/(\d+)", target)
    if m:
        return "github", int(m.group(1)), None
    m = re.search(r"/-/merge_requests/(\d+)", target)
    if m:
        return "gitlab", int(m.group(1)), None
    m = re.fullmatch(r"[#!]?(\d+)", target)
    if m:
        if target.startswith("!"):
            platform = "gitlab"
        return platform, int(m.group(1)), None
    return platform, None, target


def default_branch(remote):
    ref = git("symbolic-ref", "-q", "refs/remotes/%s/HEAD" % remote, check=False).strip()
    if ref:
        return ref.split("/", 3)[-1]
    for b in ("main", "master", "develop"):
        if git("rev-parse", "-q", "--verify", "refs/remotes/%s/%s" % (remote, b), check=False).strip():
            return b
    return "main"


def cmd_fetch(a):
    remote_url = git("remote", "get-url", a.remote, check=False).strip()
    platform, num, branch = parse_target(a.target, remote_url, a.platform)
    meta = {}
    if num is not None:
        if platform not in ("github", "gitlab"):
            sys.exit("Không đoán được nền tảng từ remote '%s'. Thêm --platform github|gitlab." % remote_url)
        rid = ("pr-%d" if platform == "github" else "mr-%d") % num
        src = ("pull/%d/head" if platform == "github" else "merge-requests/%d/head") % num
        git("fetch", "-q", a.remote, "+%s:refs/dss/%s" % (src, rid))
        head_ref = "refs/dss/" + rid
        # Metadata nếu CLI có sẵn và đã đăng nhập; thiếu thì thôi.
        if platform == "github":
            raw = tool("gh", "pr", "view", str(num), "--json", "title,body,baseRefName,author,url,labels")
            if raw:
                j = json.loads(raw)
                meta = {"title": j.get("title"), "body": j.get("body"), "base": j.get("baseRefName"),
                        "author": (j.get("author") or {}).get("login"), "url": j.get("url")}
        else:
            raw = tool("glab", "mr", "view", str(num), "-F", "json")
            if raw:
                j = json.loads(raw)
                meta = {"title": j.get("title"), "body": j.get("description"), "base": j.get("target_branch"),
                        "author": (j.get("author") or {}).get("username"), "url": j.get("web_url")}
    else:
        head_ref = branch or "HEAD"
        rid = re.sub(r"[^A-Za-z0-9._-]+", "-", branch or git("rev-parse", "--abbrev-ref", "HEAD").strip())
    base_branch = a.base or meta.get("base") or default_branch(a.remote)
    base_ref = "refs/remotes/%s/%s" % (a.remote, base_branch)
    if not git("rev-parse", "-q", "--verify", base_ref, check=False).strip():
        base_ref = base_branch
    head = git("rev-parse", head_ref).strip()
    mb = git("merge-base", base_ref, head).strip()

    files = []
    for line in git("diff", "--numstat", "-M", mb, head).splitlines():
        add, rem, path = line.split("\t", 2)
        path = path.split(" => ")[-1].rstrip("}")
        files.append({"path": path, "added": int(add) if add != "-" else 0,
                      "removed": int(rem) if rem != "-" else 0, "kind": kind_of(path)})
    status = {}
    for line in git("diff", "--name-status", mb, head).splitlines():
        parts = line.split("\t")
        status[parts[-1]] = parts[0][0]
    for f in files:
        f["status"] = status.get(f["path"], "M")

    kinds = defaultdict(int)
    for f in files:
        kinds[f["kind"]] += f["added"] + f["removed"]
    out_dir = os.path.join(a.out, rid)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "diff.patch"), "w") as fh:
        fh.write(git("diff", "-M", mb, head))
    summary = {
        "id": rid, "platform": platform, "remote": remote_url and re.sub(r"//[^@/]+@", "//", remote_url),
        "base_branch": base_branch, "merge_base": mb, "head": head, "meta": meta,
        "commits": git("log", "--format=%h %an <%ae> %s", "%s..%s" % (mb, head)).splitlines(),
        "files": files, "churn_by_kind": dict(kinds),
        "src_without_new_test": any(f["kind"] == "src" and f["added"] for f in files)
                                and not any(f["kind"] == "test" and f["added"] for f in files),
        "lint": lint(mb, head),
        "test_cmd_guess": guess_test_cmd(),
        "out_dir": out_dir,
    }
    with open(os.path.join(out_dir, "summary.json"), "w") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def guess_test_cmd():
    top = git("rev-parse", "--show-toplevel").strip()
    has = lambda p: os.path.exists(os.path.join(top, p))
    cmds = []
    if has("package.json"):
        try:
            scripts = json.load(open(os.path.join(top, "package.json"))).get("scripts", {})
            cmds += ["npm run %s" % k for k in ("test", "test:unit", "test:e2e") if k in scripts]
        except ValueError:
            pass
    if has("pyproject.toml") or has("pytest.ini") or has("setup.cfg") or has("tests"):
        cmds.append("pytest -q")
    if has("Cargo.toml"):
        cmds.append("cargo test")
    if has("go.mod"):
        cmds.append("go test ./...")
    if has("Makefile") and re.search(r"^test:", open(os.path.join(top, "Makefile")).read(), re.M):
        cmds.append("make test")
    return cmds


# ---------- diff parsing ----------
def added_hunks(base, head, exts=None):
    """-> list of {path, start, lines:[(lineno, text)]} cho các khối dòng thêm liên tiếp."""
    hunks, path, ln, cur = [], None, 0, None
    for raw in git("diff", "-U0", "-M", base, head).splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
            continue
        if raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            ln = int(m.group(1)) if m else 0
            cur = None
            continue
        if path is None or (exts and os.path.splitext(path)[1] not in exts):
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            if cur is None:
                cur = {"path": path, "start": ln, "lines": []}
                hunks.append(cur)
            cur["lines"].append((ln, raw[1:]))
            ln += 1
        elif raw.startswith("-"):
            cur = None
    return hunks


def removed_lines(base, head):
    out, path = [], None
    for raw in git("diff", "-U0", "-M", base, head).splitlines():
        if raw.startswith("--- "):
            path = raw[6:] if raw.startswith("--- a/") else None
        elif raw.startswith("-") and not raw.startswith("---") and path:
            out.append((path, raw[1:]))
    return out


# ---------- dupes ----------
COMMENT_RE = re.compile(r"(#|//).*$")
IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
STR_RE = re.compile(r"(\"(?:\\.|[^\"])*\"|'(?:\\.|[^'])*'|`(?:\\.|[^`])*`)")
NUM_RE = re.compile(r"\b\d+(\.\d+)?\b")
KEYWORDS = set("""if else elif for while return def function const let var class import from export async await
try except catch finally raise throw new fn pub impl struct enum match case switch break continue in of not and or
is None null true false True False self this let mut use mod type interface extends implements static public private
protected with as yield lambda go func package defer select chan map range""".split())


def norm_exact(s):
    s = COMMENT_RE.sub("", s).strip()
    return re.sub(r"\s+", " ", s)


def norm_shape(s):
    s = STR_RE.sub("S", norm_exact(s))
    s = NUM_RE.sub("N", s)
    return IDENT_RE.sub(lambda m: m.group(0) if m.group(0) in KEYWORDS else "v", s)


def trivial(n):
    return len(n) < 8 or re.fullmatch(r"[\s{}()\[\];,:]*(else|end|try|finally|pass|return|\}\s*else\s*\{)?[\s{}()\[\];,:]*", n) is not None


def cmd_dupes(a):
    hunks = [h for h in added_hunks(a.base, a.head, CODE_EXT)]
    exts = {os.path.splitext(h["path"])[1] for h in hunks}
    idx_exact, idx_shape = defaultdict(set), defaultdict(set)
    paths = [p for p in git("ls-tree", "-r", "--name-only", a.base).splitlines()
             if os.path.splitext(p)[1] in exts and "node_modules/" not in p and not p.endswith(".min.js")]
    for p in paths:
        try:
            text = git("show", "%s:%s" % (a.base, p), check=False)
        except UnicodeDecodeError:
            continue
        if len(text) > 400_000:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            e = norm_exact(line)
            if trivial(e):
                continue
            idx_exact[e].add((p, i))
            idx_shape[norm_shape(line)].add((p, i))
    me = a.me or git("config", "user.email", check=False).strip()
    results = []
    for h in hunks:
        lines = [(ln, t) for ln, t in h["lines"] if not trivial(norm_exact(t))]
        if len(lines) < a.min_lines:
            continue
        for mode, idx, norm in (("exact", idx_exact, norm_exact), ("shape", idx_shape, norm_shape)):
            per_file = defaultdict(list)
            for _, t in lines:
                for p, i in idx.get(norm(t), ()):
                    per_file[p].append(i)
            ranked = []
            for p, hits in per_file.items():
                # đếm số dòng của khối có mặt trong file, gom vùng quanh trung vị để blame
                matched = sum(1 for _, t in lines if any(q == p for q, _ in idx.get(norm(t), ())))
                score = matched / len(lines)
                if score >= a.threshold:
                    hits.sort()
                    mid = hits[len(hits) // 2]
                    region = [x for x in hits if abs(x - mid) <= len(lines) * 3]
                    ranked.append((score, p, min(region), max(region)))
            ranked.sort(reverse=True)
            if ranked:
                break  # có khớp nguyên văn thì không cần báo khớp cấu trúc
        if not ranked:
            continue
        matches = []
        for score, p, lo, hi in ranked[: a.top]:
            authors = set(re.findall(r"^author-mail <(.+?)>", git("blame", "--porcelain", "-L", "%d,%d" % (lo, hi), a.base, "--", p, check=False), re.M))
            matches.append({"file": "%s:%d-%d" % (p, lo, hi), "score": round(score, 2),
                            "authors": sorted(authors), "mine": bool(me) and me in authors})
        results.append({"added": "%s:%d-%d" % (h["path"], h["start"], h["lines"][-1][0]),
                        "lines": len(lines), "mode": mode, "matches": matches})
    # Tên được định nghĩa mới nhưng đã tồn tại ở base
    names = []
    def_re = re.compile(r"^\s*(?:export\s+)?(?:pub\s+)?(?:async\s+)?(?:def|function|fn|func|class|struct|interface|type)\s+([A-Za-z_]\w{3,})|^\s*(?:export\s+)?const\s+([A-Za-z_]\w{3,})\s*=\s*(?:async\s*)?\(")
    for h in hunks:
        for ln, t in h["lines"]:
            m = def_re.match(t)
            if not m:
                continue
            name = m.group(1) or m.group(2)
            hits = [x for x in git("grep", "-n", "-w", "-E", r"(def|function|fn|func|class|struct|interface|type|const)\s+%s" % re.escape(name), a.base, check=False).splitlines()]
            if hits:
                names.append({"name": name, "added": "%s:%d" % (h["path"], ln), "existing": [x.split(":", 1)[1] for x in hits[:5]]})
    print(json.dumps({"me": me, "blocks": results, "same_name_defs": names}, ensure_ascii=False, indent=2))


# ---------- lint ----------
LINT_ADDED = [
    ("test-skip", re.compile(r"\.(skip|todo)\(|\bx(it|describe|test)\(|@pytest\.mark\.(skip|xfail)|@unittest\.skip|#\[ignore\]|\bt\.Skip\(")),
    ("test-only", re.compile(r"\.(only)\(|\bf(it|describe)\(")),
    ("swallow-error", re.compile(r"except(\s+\w+(\s+as\s+\w+)?)?\s*:\s*(pass|\.\.\.)\s*$|catch\s*(\(\s*\w*\s*\))?\s*\{\s*\}|\.catch\(\s*\(\s*\w*\s*\)\s*=>\s*\{?\s*\}?\s*\)|let\s+_\s*=")),
    ("case-fix-literal", re.compile(r"\bif\b.*(==|===|!=|!==|\bis\b|\bin\b)\s*[\"'][^\"']{3,}[\"']|\bif\b.*[\"'][^\"']{3,}[\"']\s*(==|===|in)\b")),
    ("case-fix-magic-id", re.compile(r"\bif\b.*(==|===|!=|!==)\s*\d{3,}\b")),
    ("todo-hack", re.compile(r"\b(TODO|FIXME|HACK|XXX|WORKAROUND|tạm thời|tam thoi)\b", re.I)),
    ("suppress", re.compile(r"eslint-disable|@ts-ignore|@ts-expect-error|type:\s*ignore|noqa|#\[allow\(|nolint")),
    ("sleep-retry", re.compile(r"\b(time\.sleep|setTimeout|thread::sleep|asyncio\.sleep)\(")),
]
ASSERT_RE = re.compile(r"\b(assert\w*|expect\(|should\.|assert_eq!|assert!|require\.)")


def lint(base, head):
    flags = []
    for h in added_hunks(base, head):
        is_test = kind_of(h["path"]) == "test"
        prev = ""
        for ln, t in h["lines"]:
            if re.match(r"\s*(except\b[^:]*|catch\b.*)[:{]\s*$", prev) and re.fullmatch(r"\s*(pass|\.\.\.|\}|return( None| null)?;?)\s*", t):
                flags.append({"flag": "swallow-error", "at": "%s:%d" % (h["path"], ln - 1), "line": (prev.strip() + " " + t.strip())[:160]})
            prev = t
            for name, rx in LINT_ADDED:
                if name in ("test-skip", "test-only") and not is_test:
                    continue
                if name == "case-fix-literal" and is_test:
                    continue
                if rx.search(t):
                    flags.append({"flag": name, "at": "%s:%d" % (h["path"], ln), "line": t.strip()[:160]})
    removed_asserts = defaultdict(int)
    for p, t in removed_lines(base, head):
        if kind_of(p) == "test" and ASSERT_RE.search(t):
            removed_asserts[p] += 1
    added_asserts = defaultdict(int)
    for h in added_hunks(base, head):
        if kind_of(h["path"]) == "test":
            added_asserts[h["path"]] += sum(1 for _, t in h["lines"] if ASSERT_RE.search(t))
    for p, n in removed_asserts.items():
        if n > added_asserts.get(p, 0):
            flags.append({"flag": "asserts-removed", "at": p, "line": "-%d / +%d assert" % (n, added_asserts.get(p, 0))})
    for line in git("diff", "--name-status", "--diff-filter=D", base, head).splitlines():
        p = line.split("\t")[-1]
        if kind_of(p) == "test":
            flags.append({"flag": "test-file-deleted", "at": p, "line": ""})
    return flags


def cmd_lint(a):
    print(json.dumps(lint(a.base, a.head), ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("target", nargs="?", default="")
    f.add_argument("--base")
    f.add_argument("--remote", default="origin")
    f.add_argument("--platform", choices=["github", "gitlab"])
    f.add_argument("--out", default=".dss")
    d = sub.add_parser("dupes")
    d.add_argument("base"); d.add_argument("head")
    d.add_argument("--min-lines", type=int, default=4)
    d.add_argument("--threshold", type=float, default=0.6)
    d.add_argument("--me")
    d.add_argument("--top", type=int, default=3)
    l = sub.add_parser("lint")
    l.add_argument("base"); l.add_argument("head")
    a = ap.parse_args()
    {"fetch": cmd_fetch, "dupes": cmd_dupes, "lint": cmd_lint}[a.cmd](a)


if __name__ == "__main__":
    main()
