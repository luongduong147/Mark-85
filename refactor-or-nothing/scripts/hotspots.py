#!/usr/bin/env python3
"""Find change hotspots in a git repo: churn x size x branching density.

Read-only, standard library only. Works on any language (uses extensions + regex proxies).
Usage:
    python hotspots.py <repo> [--since 12.months] [--top 20] [--path SUBDIR] [--json]
The score is only for ranking; it is a signal to investigate, not a verdict.
"""
import argparse, json, math, os, re, subprocess, sys
from collections import defaultdict

EXTS = {'.py', '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.rs', '.go', '.java', '.kt',
        '.rb', '.php', '.cs', '.c', '.cc', '.cpp', '.h', '.hpp', '.swift', '.sql', '.vue', '.svelte'}
SKIP_PARTS = {'node_modules', 'dist', 'build', 'target', '.venv', 'venv', '__pycache__', 'vendor',
              '.next', 'coverage', 'migrations', 'generated', '.git'}
SKIP_SUFFIX = ('.min.js', '.d.ts', '.lock', '.snap')
BRANCH_RE = re.compile(r'\b(?:if|elif|else\s+if|for|while|match|case|catch|except|when)\b|&&|\|\||\band\b|\bor\b|\?\?')
MARK_RE = re.compile(r'\b(?:TODO|FIXME|HACK|XXX)\b')
TEST_RE = re.compile(r'(^|/)(tests?|__tests__|spec)(/|$)|(_test|\.test|\.spec)\.[a-z]+$|(^|/)test_[^/]+\.py$')


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors='replace')


def wanted(path):
    p = path.replace('\\', '/')
    if any(part in SKIP_PARTS for part in p.split('/')):
        return False
    if p.endswith(SKIP_SUFFIX):
        return False
    return os.path.splitext(p)[1].lower() in EXTS


def git_churn(repo, since, sub):
    cmd = ['git', 'log', f'--since={since.replace(".", " ")}', '--no-merges', '--no-renames',
           '--numstat', '--format=@@%H|%an|%ad', '--date=short']
    if sub:
        cmd += ['--', sub]
    r = run(cmd, repo)
    if r.returncode != 0:
        return None, r.stderr.strip()
    stats = defaultdict(lambda: {'commits': 0, 'churn': 0, 'authors': set(), 'last': ''})
    author = date = None
    for line in r.stdout.splitlines():
        if line.startswith('@@'):
            _, author, date = line[2:].split('|', 2)
        elif line.strip():
            parts = line.split('\t')
            if len(parts) != 3 or not wanted(parts[2]):
                continue
            a, d, f = parts
            s = stats[f]
            s['commits'] += 1
            s['churn'] += (int(a) if a.isdigit() else 0) + (int(d) if d.isdigit() else 0)
            s['authors'].add(author)
            s['last'] = max(s['last'], date)
    return stats, ''


def analyze_file(path):
    try:
        text = open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return None
    lines = [l for l in text.splitlines() if l.strip()]
    loc = len(lines)
    branches = sum(len(BRANCH_RE.findall(l)) for l in lines)
    marks = len(MARK_RE.findall(text))
    return loc, branches, marks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('repo')
    ap.add_argument('--since', default='12.months')
    ap.add_argument('--top', type=int, default=20)
    ap.add_argument('--path', default='')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)

    files, lang_loc, test_loc, src_loc, marks_total = {}, defaultdict(int), 0, 0, 0
    root = os.path.join(repo, a.path) if a.path else repo
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_PARTS]
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, repo).replace('\\', '/')
            if not wanted(rel):
                continue
            res = analyze_file(full)
            if not res:
                continue
            loc, br, mk = res
            files[rel] = {'loc': loc, 'branch_density': round(100 * br / loc, 1) if loc else 0.0, 'marks': mk}
            lang_loc[os.path.splitext(rel)[1].lower()] += loc
            marks_total += mk
            if TEST_RE.search(rel):
                test_loc += loc
            else:
                src_loc += loc

    stats, err = git_churn(repo, a.since, a.path)
    warn = None
    rows = []
    for rel, m in files.items():
        g = (stats or {}).get(rel)
        commits = g['commits'] if g else 0
        churn = g['churn'] if g else 0
        authors = len(g['authors']) if g else 0
        score = commits * (1 + math.log10(m['loc'] + 1)) * (1 + m['branch_density'] / 25)
        rows.append({'file': rel, 'commits': commits, 'churn_lines': churn, 'authors': authors,
                     'last_change': g['last'] if g else '', 'loc': m['loc'],
                     'branch_density': m['branch_density'], 'todo_marks': m['marks'],
                     'is_test': bool(TEST_RE.search(rel)), 'score': round(score, 1)})
    if stats is None:
        warn = f'git history unavailable ({err}); ranking by size and branching only'
        for r in rows:
            r['score'] = round(r['loc'] * (1 + r['branch_density'] / 25) / 100, 1)

    prod = [r for r in rows if not r['is_test']]
    hot = sorted(prod, key=lambda r: r['score'], reverse=True)[:a.top]
    big = sorted(prod, key=lambda r: r['loc'], reverse=True)[:10]
    single = [r for r in hot if r['authors'] == 1 and r['commits'] >= 5]
    summary = {
        'files_analyzed': len(rows), 'source_loc': src_loc, 'test_loc': test_loc,
        'test_to_source_ratio': round(test_loc / src_loc, 2) if src_loc else None,
        'loc_by_extension': dict(sorted(lang_loc.items(), key=lambda kv: -kv[1])),
        'todo_fixme_hack_total': marks_total, 'since': a.since, 'warning': warn,
    }
    if a.json:
        print(json.dumps({'summary': summary, 'hotspots': hot, 'largest_files': big,
                          'single_author_hotspots': [r['file'] for r in single]}, indent=2))
        return

    print(f'# Hotspot report ({a.since})\n')
    if warn:
        print(f'> WARNING: {warn}\n')
    print(f"Files: {summary['files_analyzed']} | source LOC: {src_loc} | test LOC: {test_loc} "
          f"| test/source: {summary['test_to_source_ratio']} | TODO/FIXME/HACK: {marks_total}")
    print('LOC by extension: ' + ', '.join(f'{k} {v}' for k, v in list(summary['loc_by_extension'].items())[:8]) + '\n')
    print('## Top hotspots (commits x size x branching; ranking signal only)\n')
    print('| file | commits | churn | authors | last | LOC | branch% | score |')
    print('|---|---:|---:|---:|---|---:|---:|---:|')
    for r in hot:
        print(f"| {r['file']} | {r['commits']} | {r['churn_lines']} | {r['authors']} | {r['last_change']} "
              f"| {r['loc']} | {r['branch_density']} | {r['score']} |")
    print('\n## Largest source files\n')
    for r in big:
        print(f"- {r['file']}: {r['loc']} LOC, branch% {r['branch_density']}, commits {r['commits']}")
    if single:
        print('\n## Single-author hotspots (bus-factor risk)\n')
        for r in single:
            print(f"- {r['file']} ({r['commits']} commits, 1 author)")
    print('\nNote: branch% counts if/for/while/match/&&/||/and/or per non-blank line; it is a language-agnostic proxy.')


if __name__ == '__main__':
    main()
