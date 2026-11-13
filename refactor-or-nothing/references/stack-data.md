# Data layer: PostgreSQL, MongoDB, Redis

## Contents
1. PostgreSQL
2. MongoDB
3. Redis (cache and beyond)
4. Cross-store consistency

## 1. PostgreSQL
- Migrations: versioned, ordered, reversible or at least forward-safe; no manual schema drift (compare migrations to live schema if access is provided). Dangerous migrations (table rewrites, `NOT NULL` with default on big tables, non-concurrent index builds).
- Schema quality: missing foreign keys and constraints, `JSONB` used to avoid modeling, nullable-everything, inconsistent naming/types (timestamps without time zone, money as float), soft-delete without partial indexes.
- Queries: N+1 patterns in the ORM, `SELECT *`, unbounded queries, missing pagination, `OFFSET` on large tables. With access: `pg_stat_statements`, `EXPLAIN (ANALYZE, BUFFERS)` on top queries, unused/duplicate indexes, bloat, long-running transactions.
- Transactions: boundaries match business operations; no external calls (LLM, HTTP) inside open transactions; isolation assumptions explicit; retries on serialization failures.
- Connection management: pool sizing versus workers, pgbouncer compatibility (prepared statements), connection leaks.
- Vector search (pgvector) if used: index type, dimension, filtering performance, re-embedding strategy when models change.
- Backups, restore tests, retention.

## 2. MongoDB
- Schema discipline: schema validation rules or a typed layer; drift across documents over time (multiple shapes in one collection); versioned documents (`schema_version`) with migration code.
- Unbounded array growth and large documents (16MB limit, update amplification); embedding versus referencing decisions that now cause `$lookup` heavy reads.
- Indexes matching real query shapes (`explain()`), compound index order, TTL indexes for ephemeral data (sessions, traces).
- Multi-document transaction assumptions; write concern and read preference defaults.
- Using Mongo for relational data with manual joins and no integrity: ask whether the data should live in Postgres, but treat a store split as a verdict-level decision with migration cost, not a casual suggestion.
- Chat/trace storage (AI): growth rate and retention policy, large payloads stored inline.

## 3. Redis
- Role clarity: pure cache (safe to lose), or also source of truth, queue, lock, rate limiter, session store? The second set needs persistence/HA decisions.
- Keys: naming convention and namespaces, TTL on every cache key, key cardinality growth; `KEYS`/unbounded `SCAN` in hot paths; big values and hot keys.
- Invalidation: who invalidates, when; stale reads after writes; cache stampede protection (single-flight, jitter); negative caching.
- Serialization: format versioning so a deploy does not poison the cache; pickling untrusted data is a defect.
- Eviction policy and `maxmemory` set consciously; memory monitoring.
- Locks: expiry and fencing (naive `SETNX` locks), safe release; queues: ack/retry semantics (Streams vs lists), poison messages.
- Connection pool and timeouts; behavior when Redis is down (fail open or fail closed, intentionally).
- Semantic or prompt caching for LLM calls: cache key includes model, params, and prompt version; privacy across users.

## 4. Cross-store consistency
- Dual writes (Postgres + Mongo + Redis) without an outbox or reconciliation job; documented source of truth per entity.
- Ordering of write then cache-invalidate, and failure between them.
- IDs and references across stores; deletion/retention propagating everywhere (GDPR-style requests).
- One data-access layer or scattered raw queries across the codebase (measure how many files import DB clients directly).
