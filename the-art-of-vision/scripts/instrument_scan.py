#!/usr/bin/env python3
"""instrument_scan.py: trả lời câu hỏi "đã có bộ đếm/đo cho metric này chưa?". Chỉ đọc.

  instrument_scan.py catalog [root]                      liệt kê mọi event tracking, metric (counter/gauge/histogram),
                                                         bảng DB và model mà repo đang có
  instrument_scan.py find [--root R] <metric> -k kw1 kw2 … [<metric> -k …]
                                                         với mỗi metric, xếp HAVE / DERIVABLE / MISSING kèm file:line
  Thêm --json để lấy kết quả máy đọc.

  HAVE      = có event hoặc metric mà tên khớp từ khóa (đếm/đo trực tiếp)
  DERIVABLE = không có bộ đếm riêng nhưng có bảng, model hoặc cột khớp, nên tính lại được bằng truy vấn
  MISSING   = không thấy gì; cần thêm instrumentation (xem references/instrumentation-audit.md)
"""
import argparse, json, os, re, sys, unicodedata
from collections import defaultdict

SKIP = re.compile(r"(^|/)(node_modules|dist|build|\.next|vendor|target|\.git|__pycache__|\.venv|venv|coverage|\.dss|\.chase)(/|$)")
EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".rs", ".go", ".java", ".kt", ".rb", ".php", ".cs",
       ".sql", ".prisma", ".yml", ".yaml", ".vue", ".svelte"}
Q = r"['\"`]([^'\"`]{2,80})['\"`]"
PATTERNS = [
    # (loại, regex; group cuối cùng là tên)
    ("event", re.compile(r"\b(?:analytics|mixpanel|segment|rudder|amplitude|posthog|heap|umami|plausible|ga|gtag|dataLayer|tracker)\s*\.\s*(?:track|capture|logEvent|trackEvent|push|event)\s*\(\s*" + Q)),
    ("event", re.compile(r"\b(?:track|trackEvent|logEvent|captureEvent|sendEvent|emitEvent|recordEvent)\s*\(\s*" + Q)),
    ("event", re.compile(r"gtag\(\s*['\"]event['\"]\s*,\s*" + Q)),
    ("event", re.compile(r"\bevent(?:_name|Name)?\s*[:=]\s*" + Q)),
    ("metric", re.compile(r"\b(?:Counter|Gauge|Histogram|Summary|UpDownCounter)\s*\(\s*" + Q)),
    ("metric", re.compile(r"\bcreate(?:Counter|Histogram|UpDownCounter|ObservableGauge|Gauge)\s*\(\s*" + Q)),
    ("metric", re.compile(r"\b(?:counter|gauge|histogram)!\s*\(\s*" + Q)),
    ("metric", re.compile(r"\bstatsd\s*\.\s*(?:increment|incr|decrement|gauge|timing|histogram|distribution|count)\s*\(\s*" + Q)),
    ("metric", re.compile(r"\b(?:Name|name)\s*:\s*\"([a-z][a-z0-9_]{3,})\"\s*,?\s*(?:Help|help)")),
    ("metric", re.compile(r"new\s+(?:client\.|prom\.)?(?:Counter|Gauge|Histogram|Summary)\s*\(\s*\{\s*name\s*:\s*" + Q)),
    ("table", re.compile(r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"]?(?:\w+\.)?(\w+)", re.I)),
    ("table", re.compile(r"__tablename__\s*=\s*" + Q)),
    ("table", re.compile(r"^\s*model\s+(\w+)\s*\{")),
    ("table", re.compile(r"\b(?:createTable|create_table|pgTable|sqliteTable|mysqlTable|Schema\.create)\s*\(\s*" + Q)),
    ("table", re.compile(r"^\s*class\s+(\w+)\s*\([^)]*(?:Model|Base|Document|SQLModel)\b")),
    ("column", re.compile(r"^\s*(\w+)\s*=\s*(?:Column|mapped_column|models\.\w+Field|fields\.\w+)\(")),
    ("column", re.compile(r"\b(?:ADD\s+COLUMN|ALTER\s+COLUMN)\s+[`\"]?(\w+)", re.I)),
    ("column", re.compile(r"(?:^|[(,])\s*[`\"]?([a-z_]\w*)[`\"]?\s+(?:small|big)?(?:int|integer|serial|numeric|decimal|money|text|varchar|char|timestamptz|timestamp|date|time|boolean|bool|uuid|jsonb|json|real|float|double)\b", re.I)),
]


def fold(s):
    s = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if not SKIP.search(os.path.join(d, x))]
        for f in files:
            if os.path.splitext(f)[1] in EXT:
                yield os.path.join(d, f)


def catalog(root):
    items = []
    for p in walk(root):
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
        except OSError:
            continue
        if len(lines) > 20000:
            continue
        rel = os.path.relpath(p, root)
        for i, line in enumerate(lines, 1):
            for kind, rx in PATTERNS:
                for m in rx.finditer(line):
                    name = m.group(m.lastindex)
                    if kind == "event" and (" " in name.strip() and len(name) > 40):
                        continue
                    items.append({"kind": kind, "name": name, "at": "%s:%d" % (rel, i)})
    seen, out = set(), []
    for it in items:
        key = (it["kind"], it["name"], it["at"])
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


def tokens(s):
    return [t for t in re.split(r"[^a-z0-9]+", fold(re.sub(r"([a-z])([A-Z])", r"\1_\2", s))) if t]


def match(item_name, kws):
    toks = set(tokens(item_name))
    joined = "_".join(tokens(item_name))
    score = 0
    for kw in kws:
        k = "_".join(tokens(kw))
        if not k:
            continue
        if k in joined or k in toks:
            score += 1
    return score


def cmd_catalog(a):
    cat = catalog(a.root)
    if a.json:
        print(json.dumps(cat, ensure_ascii=False, indent=2))
        return
    by = defaultdict(lambda: defaultdict(list))
    for it in cat:
        by[it["kind"]][it["name"]].append(it["at"])
    print("# Instrumentation catalog: %s\n" % os.path.abspath(a.root))
    for kind in ("event", "metric", "table", "column"):
        names = by.get(kind, {})
        print("## %s (%d)" % (kind, len(names)))
        for n in sorted(names)[:200]:
            locs = names[n]
            print("- `%s`  %s%s" % (n, locs[0], " (+%d)" % (len(locs) - 1) if len(locs) > 1 else ""))
        print()


def cmd_find(a):
    # argv: <metric> [-k kw …] <metric> [-k kw …]; một token đứng ngay trước "-k" là tên metric kế tiếp
    specs, i, r = [], 0, a.rest
    while i < len(r):
        name = r[i]; i += 1
        kws = []
        if i < len(r) and r[i] == "-k":
            i += 1
            while i < len(r) and r[i] != "-k" and not (i + 1 < len(r) and r[i + 1] == "-k"):
                kws.append(r[i]); i += 1
        specs.append({"metric": name, "kw": kws or tokens(name)})
    cat = catalog(a.root)
    results = []
    for s in specs:
        direct = sorted([(match(c["name"], s["kw"]), c) for c in cat if c["kind"] in ("event", "metric")],
                        key=lambda x: -x[0])
        derive = sorted([(match(c["name"], s["kw"]), c) for c in cat if c["kind"] in ("table", "column")],
                        key=lambda x: -x[0])
        direct = [c for sc, c in direct if sc > 0][:8]
        derive = [c for sc, c in derive if sc > 0][:8]
        status = "HAVE" if direct else "DERIVABLE" if derive else "MISSING"
        results.append({"metric": s["metric"], "keywords": s["kw"], "status": status,
                        "direct": direct, "derivable_from": derive})
    if a.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    print("| Metric | Trạng thái | Bằng chứng |\n|---|---|---|")
    for r_ in results:
        ev = r_["direct"] or r_["derivable_from"]
        proof = "<br>".join("`%s` (%s) %s" % (c["name"], c["kind"], c["at"]) for c in ev[:4]) or "không thấy (từ khóa: %s)" % ", ".join(r_["keywords"])
        print("| %s | **%s** | %s |" % (r_["metric"], r_["status"], proof))
    print("\nHeuristic theo tên. HAVE vẫn phải mở file kiểm tra: event có bắn đúng lúc, đủ thuộc tính (user_id, thời điểm, giá trị) không.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("catalog"); c.add_argument("root", nargs="?", default="."); c.add_argument("--json", action="store_true")
    f = sub.add_parser("find"); f.add_argument("--root", default="."); f.add_argument("--json", action="store_true")
    f.add_argument("rest", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    {"catalog": cmd_catalog, "find": cmd_find}[a.cmd](a)


if __name__ == "__main__":
    main()
