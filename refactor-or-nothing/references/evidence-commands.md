# Evidence gathering: read-only commands

Run what exists and is safe. Never install into the user's repo; use `uvx`/`pipx run`/`npx --yes` or a temp environment, or skip and say so. Record each command and its output summary in the report's "Evidence" appendix.

## Always
```bash
python scripts/hotspots.py <repo> --since 12.months          # churn x size x branching, TODO counts, test ratio
git -C <repo> shortlog -sn --since=12.months                  # contributors / bus factor
git -C <repo> log --since=12.months -i -E --grep='fix|hotfix|revert' --oneline | head -50   # defect-ish history
```

## Python
```bash
ruff check . --statistics
radon cc -s -n C <src>            # complexity C or worse
radon mi -s <src> | head          # maintainability index
vulture <src> --min-confidence 80 # dead code
mypy <src> / pyright              # type errors, Any usage
pip-audit                          # vulnerable deps
pytest -q --durations=15           # slow tests; add --cov for coverage if configured
```

## TypeScript / React
```bash
npx tsc --noEmit
npx eslint . --max-warnings=0
npx knip                            # unused files, exports, deps
npx madge --circular --extensions ts,tsx src   # circular imports
npm audit --omit=dev / pnpm audit
npx vite build && (bundle analyzer if configured)
rg -n "\bany\b|@ts-ignore|@ts-expect-error|as unknown as" src | wc -l
```

## Rust
```bash
cargo clippy --all-targets -- -W clippy::unwrap_used -W clippy::expect_used   # read-only lint
cargo udeps / cargo machete          # unused deps
cargo audit; cargo deny check
cargo geiger                         # unsafe usage
cargo build --timings                # compile-time cost
rg -n "unwrap\(\)|expect\(" --glob '!*test*' src | wc -l
```

## Data
- Postgres (only with user-provided read access): `pg_stat_statements` top by total time; `EXPLAIN (ANALYZE, BUFFERS)` on those; index usage views. Without access, review migrations and ORM queries.
- Mongo: `db.collection.getIndexes()`, `explain("executionStats")`, collection stats.
- Redis: `INFO memory`, `INFO keyspace`, `MEMORY USAGE`, `SCAN`-based sampling (never `KEYS *` on production).

## Cross-language quick signals (rg)
```bash
rg -n "TODO|FIXME|HACK|XXX" | wc -l
rg -n -i "global |singleton|_instance" --type py
rg -n "catch\s*\(.*\)\s*\{\s*\}|except\s*:|except Exception:\s*pass"
rg -l "import redis|pymongo|asyncpg|psycopg|sqlalchemy" | wc -l    # DB access spread
```
Treat all counts as signals to investigate, never as findings by themselves.
