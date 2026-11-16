#!/usr/bin/env python3
"""slop_scan.py — quét heuristic tìm "slop" trong code. Chỉ đọc, chỉ gợi ý; model phải đọc lại từng cờ.

  slop_scan.py [--diff BASE] [--window 5] [--only code|fe|text] [--json] [paths...]

  Phạm vi:
    --diff BASE   chỉ xét dòng được thêm so với BASE (mặc định: merge-base với main, gồm cả working tree)
    paths...      xét toàn bộ các file/thư mục này
    (không có gì) tương đương --diff main

  Nhóm cờ:
    code  dup-block (khối lặp trong phạm vi hoặc lặp với code sẵn có), narrating-comment, broad-except,
          type-escape, debug-leftover, wrapper-name, commented-out-code
    fe    ai-gradient, glass, ai-radius-shadow, gradient-text, emoji-ui, default-font, hardcoded-color,
          stock-copy, magic-zindex
    text  ai-vocab, chatbot-phrase, filler (trong comment, docstring, chuỗi UI, file .md)
"""
import argparse, json, os, re, subprocess, sys
from collections import defaultdict

CODE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".rs", ".go", ".java", ".kt", ".rb", ".php",
            ".cs", ".c", ".cc", ".cpp", ".h", ".hpp", ".swift", ".vue", ".svelte", ".sh"}
FE_EXT = {".jsx", ".tsx", ".vue", ".svelte", ".html", ".css", ".scss", ".sass", ".less", ".astro"}
TEXT_EXT = {".md", ".mdx", ".rst", ".txt"}
SKIP_DIR = re.compile(r"(^|/)(node_modules|dist|build|\.next|vendor|target|\.git|__pycache__|\.venv|venv|coverage)/")


def git(*args, check=True):
    r = subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        sys.exit("git %s thất bại: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


# ---------- rules ----------
COMMENT = r"(?:#|//|/\*|\*|<!--|\{/\*)\s*"
R = lambda p, f=re.I: re.compile(p, f)
CODE_RULES = [
    ("narrating-comment", R(COMMENT + r"(this (function|method|class|component) (is used to|will|does)|helper (function|method) (to|for|that)|"
                             r"initiali[sz]e (the )?\w+$|increment \w+|loop (through|over)|iterate (through|over)|check if |return(s)? the |"
                             r"set (the )?\w+ to |create (a )?new |import (the )?|call (the )?\w+ function|"
                             r"hàm này|khởi tạo|kiểm tra xem|lặp qua|duyệt qua|trả về |gọi hàm)")),
    ("broad-except", R(r"except\s*(Exception|BaseException)?\s*(as \w+)?\s*:\s*$|catch\s*\(\s*(e|err|error|_)?\s*(:\s*any)?\s*\)\s*\{\s*(\}|console\.(log|error))|\.catch\(\s*\(\)\s*=>|unwrap_or_default\(\)", 0)),
    ("type-escape", R(r"\bas any\b|:\s*any\b|@ts-ignore|@ts-nocheck|# type:\s*ignore|eslint-disable(?!-next-line \S+ -- )|\bunsafe\s*\{|#\[allow\(", 0)),
    ("debug-leftover", R(r"^\s*(console\.(log|debug)\(|print\(\s*(f?[\"'](debug|here|>>>|---|xxx|test)|[a-z_]\w*\s*\))|println!\(\"debug|dbg!\(|debugger;|fmt\.Println\(\"DEBUG)", re.I)),
    ("wrapper-name", R(r"\b(class|struct|interface|type)\s+\w*(Manager|Helper|Wrapper|Util|Utils|Handler|Processor|Factory|Provider)(Base|Impl)?\b", 0)),
    ("commented-out-code", R(r"^\s*(#|//)\s*(return |if \(|for \(|const |let |var |def |import |from \w+ import|await |\w+\(.*\);?$)", 0)),
]
FE_RULES = [
    ("ai-gradient", R(r"bg-gradient-to-\w+[^\"'`]*from-(purple|violet|indigo|fuchsia|pink|blue)-|linear-gradient\([^)]*(#(8b5cf6|7c3aed|6366f1|a855f7|ec4899|3b82f6)|purple|violet|indigo)")),
    ("glass", R(r"backdrop-blur|backdrop-filter:\s*blur|bg-white/(5|10|20)\b|rgba\(255,\s*255,\s*255,\s*0\.(0?5|1|2)\)")),
    ("ai-radius-shadow", R(r"rounded-(2xl|3xl)[^\"'`]*shadow-(xl|2xl)|shadow-(xl|2xl)[^\"'`]*rounded-(2xl|3xl)|hover:scale-1(05|10)|hover:-translate-y-")),
    ("gradient-text", R(r"bg-clip-text[^\"'`]*text-transparent|text-transparent[^\"'`]*bg-clip-text|-webkit-background-clip:\s*text")),
    ("emoji-ui", re.compile("[\U0001F300-\U0001FAFF✨⚡✅❌⭐\U0001F680]")),
    ("default-font", R(r"font-family:\s*['\"]?(Inter|Poppins)\b|fontFamily:\s*\{?[^}]*['\"](Inter|Poppins)['\"]")),
    ("hardcoded-color", R(r"(?<![\w-])#[0-9a-f]{6}\b|\b(bg|text|border)-\[#[0-9a-f]{3,6}\]")),
    ("stock-copy", R(r"(supercharge|unleash|elevate|revolutioni[sz]e|seamless(ly)?|effortless(ly)?|next[- ]level|game[- ]chang|"
                     r"all-in-one|cutting[- ]edge|lorem ipsum|get started (today|now|for free)|built for the future|"
                     r"trải nghiệm (liền mạch|tuyệt vời)|nâng tầm|bứt phá|đột phá)")),
    ("magic-zindex", R(r"z-index:\s*\d{3,}|\bz-\[\d{3,}\]")),
]
AI_VOCAB = (r"additionally|crucial|delve|enduring|enhance|fostering|garner|interplay|intricate|pivotal|showcase|tapestry|"
            r"testament|underscore|vibrant|leverage|utili[sz]e|facilitate|robust|seamless|comprehensive|streamline|"
            r"empower|holistic|paradigm|synergy|nuanced")
TEXT_RULES = [
    ("ai-vocab", R(r"\b(%s)\w*\b" % AI_VOCAB)),
    ("chatbot-phrase", R(r"(i hope this helps|let me know if|great question|you'?re absolutely right|certainly!|of course!|"
                         r"happy to help|feel free to|hy vọng (điều này|nó) giúp|rất vui được)")),
    ("filler", R(r"\b(in order to|due to the fact that|it is important to note|it'?s worth noting|at the end of the day|"
                 r"needless to say|cần lưu ý rằng|điều quan trọng là)\b")),
]
COMMENT_OR_STR = re.compile(r"(#|//|/\*|\*|<!--).*$|\"[^\"]{12,}\"|'[^']{12,}'|`[^`]{12,}`|>[^<>{}]{12,}<")


def nontrivial(s):
    s = re.sub(r"\s+", " ", re.sub(r"(#|//).*$", "", s)).strip()
    return s if len(s) >= 10 and not re.fullmatch(r"[\s{}()\[\];,:]*|(else|try|finally|pass|break|continue|return)[:;]?", s) else ""


# ---------- scope ----------
def scope_from_diff(base):
    """-> {path: set(dòng được thêm)} gồm cả thay đổi chưa commit và file untracked."""
    mb = git("merge-base", base, "HEAD", check=False).strip() or base
    added, path, ln = defaultdict(set), None, 0
    for raw in git("diff", "-U0", "-M", mb).splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            ln = int(m.group(1)) if m else 0
        elif raw.startswith("+") and path:
            added[path].add(ln)
            ln += 1
    for p in git("ls-files", "--others", "--exclude-standard").splitlines():
        try:
            n = sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
        except OSError:
            continue
        added[p] = set(range(1, n + 1))
    return mb, added


def scope_from_paths(paths):
    out = {}
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if not SKIP_DIR.search(os.path.join(root, d) + "/")]
                for f in files:
                    out[os.path.join(root, f)] = None
        elif os.path.isfile(p):
            out[p] = None
    return out


def read_lines(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as fh:
            return fh.read().splitlines()
    except OSError:
        return []


# ---------- scan ----------
def scan(scope, only, window):
    findings = []
    add = lambda group, rule, p, ln, text: findings.append(
        {"group": group, "rule": rule, "at": "%s:%d" % (p, ln), "line": text.strip()[:160]})
    win_index = defaultdict(list)
    for p, lines_in_scope in scope.items():
        ext = os.path.splitext(p)[1].lower()
        if SKIP_DIR.search(p) or p.endswith((".min.js", ".lock")) or ext not in CODE_EXT | FE_EXT | TEXT_EXT:
            continue
        lines = read_lines(p)
        in_scope = (lambda i: True) if lines_in_scope is None else (lambda i: i in lines_in_scope)
        for i, t in enumerate(lines, 1):
            if not in_scope(i):
                continue
            if only in (None, "code") and ext in CODE_EXT:
                for rule, rx in CODE_RULES:
                    if rx.search(t):
                        add("code", rule, p, i, t)
            if only in (None, "fe") and ext in FE_EXT:
                for rule, rx in FE_RULES:
                    if rule == "hardcoded-color" and ext not in {".jsx", ".tsx", ".vue", ".svelte", ".html"}:
                        continue  # trong file CSS, mã màu thường là chỗ định nghĩa token
                    if rx.search(t):
                        add("fe", rule, p, i, t)
            if only in (None, "text"):
                target = t if ext in TEXT_EXT else " ".join(m.group(0) for m in COMMENT_OR_STR.finditer(t))
                for rule, rx in TEXT_RULES:
                    if target and rx.search(target):
                        add("text", rule, p, i, t)
        if only in (None, "code") and ext in CODE_EXT | FE_EXT:
            nt = [(i, nontrivial(t)) for i, t in enumerate(lines, 1)]
            nt = [(i, s) for i, s in nt if s]
            for k in range(len(nt) - window + 1):
                chunk = nt[k:k + window]
                key = "\n".join(s for _, s in chunk)
                win_index[key].append((p, chunk[0][0], chunk[-1][0], any(in_scope(i) for i, _ in chunk)))
    # Khối lặp: cửa sổ xuất hiện >= 2 nơi và ít nhất một nơi nằm trong phạm vi; gộp các cửa sổ chồng nhau.
    pairs = defaultdict(list)  # (file trong phạm vi, file kia) -> [(a, b, a2, b2)]
    for locs in win_index.values():
        if len(locs) < 2:
            continue
        for x in locs:
            if not x[3]:
                continue
            for y in locs:
                if y[:2] != x[:2] and not (y[3] and (y[0], y[1]) < (x[0], x[1])):
                    pairs[(x[0], y[0])].append((x[1], x[2], y[1], y[2]))
    for (pa, pb), spans in pairs.items():
        spans.sort()
        merged = [list(spans[0])]
        for a, b, a2, b2 in spans[1:]:
            m = merged[-1]
            if a <= m[1] + 1:
                m[1], m[2], m[3] = max(m[1], b), min(m[2], a2), max(m[3], b2)
            else:
                merged.append([a, b, a2, b2])
        for a, b, a2, b2 in merged:
            findings.append({"group": "code", "rule": "dup-block", "at": "%s:%d-%d" % (pa, a, b),
                             "line": "lặp với %s:%d-%d" % (pb, a2, b2)})
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--diff", metavar="BASE")
    ap.add_argument("--window", type=int, default=5)
    ap.add_argument("--only", choices=["code", "fe", "text"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.paths and not a.diff:
        scope, label = scope_from_paths(a.paths), "paths: " + " ".join(a.paths)
    else:
        mb, scope = scope_from_diff(a.diff or "main")
        label = "diff từ %s (merge-base %s)" % (a.diff or "main", mb[:8])
        # Diff mode: thêm các file code cùng loại (toàn bộ, ngoài phạm vi) để bắt lặp với code sẵn có.
        exts = {os.path.splitext(p)[1] for p in scope}
        for p in git("ls-files").splitlines():
            if p not in scope and os.path.splitext(p)[1] in exts & (CODE_EXT | FE_EXT):
                scope[p] = set()
    f = scan(scope, a.only, a.window)
    if a.json:
        print(json.dumps({"scope": label, "findings": f}, ensure_ascii=False, indent=2))
        return
    print("# slop_scan — %s — %d cờ\n" % (label, len(f)))
    by = defaultdict(list)
    for x in f:
        by[(x["group"], x["rule"])].append(x)
    for (g, r), xs in sorted(by.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
        print("## %s/%s (%d)" % (g, r, len(xs)))
        for x in xs[:25]:
            print("- %s  %s" % (x["at"], x["line"]))
        if len(xs) > 25:
            print("- … còn %d" % (len(xs) - 25))
        print()


if __name__ == "__main__":
    main()
