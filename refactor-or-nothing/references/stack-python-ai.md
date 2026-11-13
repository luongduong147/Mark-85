# Python and custom in-house AI stack

Use when the repo has Python and hand-built LLM infrastructure: provider wrappers, context management, agent loop, tools, registry, memory, evals.

## Contents
1. How to approach custom AI infrastructure
2. LLM wrapper / provider layer
3. Context management
4. Agent loop
5. Tools and registry
6. Observability, cost, evals
7. General Python checks

## 1. Approach

Custom here is often deliberate. Evaluate each component by (a) is the boundary clean enough that swapping a model/provider or the whole component is cheap, (b) is it testable without a real model, (c) does it fail safely. Flag "reinventing a stable library" only when maintenance cost is evidenced, and name what adopting would cost (lock-in, lost customization).

Fast churn in this layer is expected. Judge whether churn is **contained behind a stable interface**.

## 2. LLM wrapper / provider layer
- Provider types leaking into callers (callers import SDK response objects, branch on provider name).
- One normalized message/content-block/tool-call/usage model, or several ad hoc dicts?
- Retries, backoff with jitter, timeouts, rate-limit handling, cancellation, streaming error mid-stream; idempotency of retries.
- Handling of partial responses, refusals, stop reasons, truncated output, malformed tool-call JSON.
- Token counting and cost tracking done in one place; model names/pricing in config, not scattered literals.
- Sync/async duplication; blocking calls inside async code; unbounded concurrency.
- A fake/replay model implementation exists for tests (very high value; its absence is a top verifiability finding).

## 3. Context management
- Single owner of the message history and its invariants (tool-call/tool-result pairing, role ordering). Violations cause provider 400s that are expensive to debug.
- Truncation/compaction strategy is explicit, tested, and never splits a tool-call from its result or drops the system prompt.
- Token budgets computed per model; handling of very large tool outputs (cap, summarize, store by reference).
- Prompt assembly: templates versioned and testable, not string concatenation across files; caching-friendly ordering (stable prefix first) if prompt caching is used.
- Memory/state persistence: schema versioning for stored conversations; behavior when old formats load.
- Secrets or PII ending up in prompts or logs.

## 4. Agent loop
- Termination: max steps/tokens/time, explicit stop conditions, behavior on repeated identical tool calls (loop detection).
- Cancellation and timeouts propagate through tool execution; partial state is recoverable.
- Error policy: tool errors returned to the model vs raised; retries bounded; poisoned context after errors.
- Parallel tool calls: ordering, result pairing, shared-state races.
- State machine clarity: loop logic split from policy (approval, budgets, guardrails) or one 500-line function with flags?
- Human-in-the-loop/approval hooks; permission boundaries for dangerous tools.
- Determinism for tests: seedable, record/replay of full traces, golden transcripts.

## 5. Tools and registry
- Registration mechanism: import-time side effects, global mutable registries, name collisions, ordering dependence. Prefer explicit registration passed to the agent.
- Schema source of truth: one definition generates the model-facing JSON schema and validates inputs (pydantic or equivalent); no hand-synced duplicates.
- Argument validation and clear error messages back to the model; output size caps and typed results.
- Tool side effects: idempotency, timeouts, sandboxing, least privilege, audit log.
- Per-tool tests that run without network; contract tests for schema stability.
- Dynamic tool discovery/versioning if tools are added at runtime.

## 6. Observability, cost, evals
- Structured tracing of each model call and tool call (inputs, outputs, latency, tokens, cost, correlation IDs) with redaction.
- Evals or regression suites for prompts/agents; are they run in CI; are failures actionable?
- Budget and rate guards per user/session; kill switch.
- Prompt and model changes are traceable (version in logs).

## 7. General Python checks
- Typing: coverage, `Any` density, mypy/pyright strictness; pydantic models at boundaries.
- Packaging: `pyproject.toml`, pinned lock (uv/poetry/pip-tools), Python version policy, dev/prod dependency split.
- Async: blocking I/O in event loop, `asyncio.run` nesting, orphaned tasks, missing `await`, no cancellation handling, mixing threads and loops.
- Circular imports, `utils.py`/`helpers.py` junk drawers, module-level singletons and global state, import-time work.
- Exception handling: bare `except`, swallowed errors, error types as strings.
- Config: env vars read in many places; no single settings object; secrets in code.
- Dead code (`vulture`), duplicated logic, long functions (`radon`, `ruff` rules), mutable default args.
