---
name: refactor-or-nothing
description: Review a codebase (or a module/PR set), measure its technical debt with evidence, and deliver a decision report on whether to refactor, contain, leave alone, or rewrite — with cost/benefit, options, and conditions. Use this skill whenever the user asks to review code quality, audit a repo, assess technical debt, decide "should we refactor / rewrite / leave it", estimate refactor ROI, check codebase health before a big feature, or says things like "đánh giá code", "nợ kỹ thuật", "có nên refactor không", "nên viết lại không", "review kiến trúc", "code này có ổn không" — even if they never say "technical debt". Tuned for Python, JS/TS/TSX, Rust; Vite+React+Tailwind; Fastify/FastAPI/Axum; Postgres, MongoDB, Redis; and custom in-house AI stacks (LLM wrappers, context management, agent loops, tool registries).
user-invocable: true
disable-model-invocation: false
whenToUse: "Người dùng muốn đánh giá code / đo nợ kỹ thuật / quyết định có nên refactor, rewrite, contain hay để nguyên — kèm bằng chứng, chi phí/lợi ích và điều kiện đổi verdict. Gõ /refactor-or-nothing hoặc nói 'đánh giá code', 'có nên refactor không', 'nợ kỹ thuật', 'review kiến trúc', 'nên viết lại không'…"
---

# Refactor or Nothing

Goal: produce a **decision**, not a list of complaints. The reader is someone who must decide where to spend engineering time. Every finding exists to support (or undermine) one of these verdicts:

| Verdict | Meaning |
|---|---|
| **LEAVE** | Debt is real but cheap or in code that rarely changes. Do nothing. |
| **CONTAIN** | Put a boundary, tests, or docs around it so it stops spreading. No restructuring. |
| **REFACTOR-TARGETED** | Fix specific hotspots incrementally, alongside planned work. |
| **REFACTOR-PROGRAM** | Dedicated, time-boxed, multi-step effort on a subsystem with milestones and rollback. |
| **REWRITE** | Replace a component wholesale. Only when incremental paths are shown to be infeasible (see `references/decision-framework.md`). |
| **INSUFFICIENT-DATA** | Say so, and list exactly what to collect. An honest "don't know yet" beats a confident guess. |

One report can give different verdicts per area (e.g. LEAVE for the React UI, REFACTOR-TARGETED for the agent loop).

## Core principles

- **Debt is only debt if it costs interest.** Ugly code nobody touches is not a priority. Weigh every finding by how often the area changes, how much it slows those changes, and how badly it can fail. Ask for or infer the upcoming roadmap; it is the strongest signal.
- **Evidence over taste.** Each finding cites `file:line` and says whether it is **Verified** (you read it / a tool reported it) or **Inferred** (pattern suggests it). Never present inferred claims as facts. Do not pad: a short report with five solid findings beats forty weak ones.
- **Separate defects from debt.** A security hole or data-loss bug is urgent regardless of refactor decisions. Report those in their own section, not buried in debt scoring.
- **No rewrite bias, no refactor bias.** Rewrites are usually more expensive and riskier than they look; refactors can also be gold-plating. Let the cost model decide. Treat deliberate, documented trade-offs (e.g. a custom agent framework chosen on purpose) as decisions to evaluate by their maintenance cost, not as mistakes.
- **Chesterton's fence.** Before calling something wasteful, find out why it exists (git blame/log, comments, tests). Include a "looks bad but is fine" list; it builds trust and prevents wasted work.
- **Estimates are ranges.** Give effort as person-day ranges with stated assumptions. If the user can supply velocity, incident, or onboarding data, use it and say so.

## Workflow

### 1. Scope and context (ask at most 3 questions, then proceed)
Ask only what you cannot infer: (a) scope (whole repo, a subsystem, a PR set), (b) what is planned for the next 3-6 months, (c) known pain (slow features, recurring bugs, onboarding, incidents) and team size. If the user does not answer, state your assumptions at the top of the report and continue.

If you have no repo access (e.g. chat without files), ask for: directory tree, output of `scripts/hotspots.py`, and the few files they suspect are worst. Lower the confidence rating accordingly.

### 2. Reconnaissance (cheap, broad)
- Map the repo: languages, entry points, module boundaries, dependency manifests, test layout, CI config, deploy files. Read `README`, `CLAUDE.md`/`AGENTS.md`, ADRs, and recent commit messages.
- Run `python scripts/hotspots.py <repo> --since 12.months` to find where change concentrates (churn × size × branching density). See `references/evidence-commands.md` for per-stack tooling (linters, type-checkers, dead-code, dependency audits) and run what is available and safe. These are read-only; never modify the repo or install into it.
- Detect which stack references apply and read **only those**:
  - Python/AI custom stack (LLM wrapper, context, agent loop, tools, registry) → `references/stack-python-ai.md`
  - React/Vite/Tailwind/TS, Fastify, FastAPI, Axum/Rust → `references/stack-web-backend.md`
  - Postgres, MongoDB, Redis → `references/stack-data.md`

### 3. Deep read where it matters
Do not read everything. Read the top hotspots, the architectural seams (module boundaries, public interfaces), and the code on the critical path (auth, payments, data writes, the agent loop). For each, look at dimensions in the list below. Sample rather than exhaust; say what you sampled.

Dimensions:
1. **Architecture and boundaries**: layering, circular dependencies, god modules, leaky abstractions, where a change ripples.
2. **Code-level maintainability**: size and branching of hot files, duplication, naming, dead code, misleading abstractions.
3. **Verifiability**: tests where change happens, test speed and flakiness, ability to run offline (fake LLM, fake DB), CI gates, type coverage.
4. **Dependencies and build**: outdated or abandoned packages, pinning, lockfiles, vulnerable versions, build reproducibility.
5. **Data layer**: schema and migration discipline, query patterns, indexes, consistency, cache invalidation.
6. **Operability**: logging, tracing, metrics, config and secrets handling, deploy and rollback, cost visibility (for AI: token and latency tracking).
7. **Knowledge**: docs, bus factor (single-author hotspots), onboarding friction.
8. **Defects found along the way**: security, data loss, correctness. Separate section.

### 4. Quantify
For each significant finding (aim for 5-15), fill the fields in `references/report-template.md` (severity, interest, effort, evidence level). Then apply the cost model in `references/decision-framework.md`: monthly interest vs one-off principal, payback period, risk of the fix itself.

### 5. Decide
Choose a verdict per area using the decision rules. State the **conditions that would change the verdict** (e.g. "if the payments module is touched more than twice next quarter, upgrade LEAVE to REFACTOR-TARGETED"). Give a confidence level (High / Medium / Low) and the reason.

### 6. Write the report
Use `references/report-template.md`. Rules:
- Verdict and top-3 reasons go first; a reader who stops after one screen should know what to do.
- Write in the user's language. Default to Vietnamese if the user writes Vietnamese; keep code identifiers, paths and commands in their original form.
- Deliver as a Markdown file (`REFACTOR_DECISION_REPORT.md`) in the outputs location when file tools are available, and summarize the verdict in chat. If the user wants Word or PDF, convert using the docx or pdf skills.
- Include a phased plan only for REFACTOR-* verdicts: steps small enough to ship independently, each with a success metric and a rollback.
- End with "Open questions / what I could not verify".

## Calibration reminders
- Fast-moving AI code churns for good reasons (provider APIs change monthly). High churn in a wrapper layer is a sign it is a useful seam, not automatically a hotspot to rewrite. Judge whether the churn is *contained* behind a stable interface.
- A custom framework is justified when it encodes domain-specific behavior that libraries do not. Flag it only when maintenance cost is evidenced (bugs, slow onboarding, reinventing a stable library feature) and say what adopting a library would cost, including lock-in.
- Do not recommend sweeping style changes (formatters, renames) as "refactors"; they are cheap hygiene. Mention once under quick wins.
- Never run destructive commands, never push, never auto-fix, unless the user explicitly asks for that as a separate task.
