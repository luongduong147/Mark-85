# Frontend (Vite + React + Tailwind + TSX) and backends (Fastify, FastAPI, Axum)

Read only the sections that match the repo.

## Contents
1. TypeScript and React (Vite, Tailwind)
2. Fastify (Node)
3. FastAPI (Python)
4. Axum (Rust)
5. Cross-cutting API checks

## 1. TypeScript and React (Vite, Tailwind)
- `tsconfig`: `strict` on? Count of `any`, `as` casts, `@ts-ignore`/`@ts-expect-error`. Run `tsc --noEmit`.
- Components: files over ~300 lines; components mixing data fetching, state, and layout; prop drilling more than 2-3 levels.
- Server state: hand-rolled `useEffect` + `fetch` + loading flags versus a data layer (TanStack Query or similar); duplicated caching and invalidation logic.
- Effects: missing/incorrect dependency arrays, effects used to derive state, subscription cleanup, race conditions on rapid navigation.
- State management: a single global store used for everything, or context re-render storms; form state handled ad hoc.
- Streaming/chat UIs (common in AI apps): message list virtualization, handling of partial tokens, abort on unmount, reconnect, scroll anchoring, memory growth in long sessions.
- Types shared with the backend: generated from OpenAPI/zod/JSON Schema, or hand-copied and drifting?
- Tailwind: duplicated long class strings that should be components; arbitrary values everywhere; no design tokens; dark-mode/theme inconsistencies. Heavy `@apply` is usually a smell, but do not call utility-class verbosity "debt" by itself.
- Vite: bundle size (`vite build` + analyzer), code splitting, env var handling (`import.meta.env`), dead dependencies (`knip`).
- Tests: component tests for logic-heavy parts, e2e for critical flows; flaky selectors.
- Accessibility and error boundaries on critical screens.

## 2. Fastify (Node)
- Plugin encapsulation used properly, or everything registered on the root with hidden coupling via decorators.
- Schema-first validation (JSON Schema / TypeBox / zod provider) on every route; response schemas for serialization speed and safety.
- Central error handler; async handler errors; hooks ordering; lifecycle (`onClose`) for DB/Redis shutdown.
- Business logic inside route handlers versus services; testability with `fastify.inject`.
- Blocking CPU work on the event loop; unbounded request bodies; missing timeouts and rate limits.

## 3. FastAPI (Python)
- Sync endpoints calling blocking libs inside `async def`, or async endpoints calling sync DB drivers.
- Dependency injection used for DB sessions, auth, settings; global clients created at import time.
- Pydantic v2 models at boundaries; `response_model` set; internal ORM models not leaked to responses.
- Session/transaction handling (SQLAlchemy sessions per request, commit/rollback, N+1 with lazy loading); Alembic migrations in order.
- `BackgroundTasks` used for work that needs durability/retries (should be a queue); lifespan events for startup/shutdown.
- SSE/WebSocket/streaming endpoints (AI): disconnect handling, backpressure, cancellation of upstream model calls.
- Settings via `pydantic-settings`, not scattered `os.getenv`.

## 4. Axum (Rust)
- Error type strategy: `thiserror` for library/domain, `anyhow` at edges; `unwrap`/`expect`/`panic!` outside tests and startup (`rg`/clippy `unwrap_used`).
- Shared state design: `Arc<Mutex<...>>` everywhere versus message passing or narrower state; lock held across `.await`.
- Blocking calls in async context (`spawn_blocking` missing); runtime misuse.
- Extractor and layer structure (tower middleware) clear; handler size; request validation.
- `unsafe` blocks: count, justification, tests (`cargo geiger`). `clippy` warnings level in CI; `cargo deny`/`audit`.
- sqlx/diesel usage: compile-time checked queries, migrations discipline, pool sizing.
- Over-generic code, trait-object vs generics churn that makes changes expensive; long compile times as a velocity cost (measure `cargo build --timings` before blaming).
- Do not flag `.clone()` as debt without profiling evidence.

## 5. Cross-cutting API checks
- Versioning and backward compatibility of public endpoints and stored data.
- AuthN/AuthZ enforced consistently (middleware/dependency) versus ad hoc per route; object-level authorization checks.
- Input validation, output encoding, CORS, CSRF as applicable, rate limiting, request size limits, secrets handling (report concrete issues under **Defects**, not debt).
- Idempotency for retried POSTs; pagination; consistent error shape.
- Contract between FE and BE: single source of truth, contract tests.
