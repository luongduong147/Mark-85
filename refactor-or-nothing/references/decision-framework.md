# Decision framework

## Contents
1. Cost model
2. Scoring findings
3. Decision rules
4. When rewrite is allowed
5. Incremental strategies
6. Conditions and triggers

## 1. Cost model

For each area (module/subsystem), estimate:

- **Interest (per month)** = changes_per_month x extra_time_per_change + incident_cost + onboarding_drag
  - `changes_per_month`: from git history (commits touching the area, last 6-12 months) plus roadmap.
  - `extra_time_per_change`: how much longer a change takes than in clean code (hours). Ground it: files touched per change, test run time, rework, review back-and-forth.
  - `incident_cost`: bugs, rollbacks, hotfixes traced to this area (commit messages, issue tracker if provided).
  - `onboarding_drag`: time a new dev needs to become productive here.
- **Principal (one-off)** = refactor effort in person-days as a range (low / likely / high), plus the cost of writing the tests you need first.
- **Fix risk**: probability and impact of the refactor breaking behavior. High when tests are absent, the area is on a critical path, or behavior is poorly specified.
- **Payback (months)** = principal_likely / interest_per_month (same unit throughout).

If the user gives no velocity numbers, state your assumptions explicitly (e.g. "assumed 2h extra per change, 12 changes/month") and show how the verdict shifts if they are wrong (halve and double the interest).

## 2. Scoring findings

| Field | Scale |
|---|---|
| Severity | Critical (data loss, security, outage risk) / High (slows or blocks frequent work) / Medium / Low |
| Interest | High (touched weekly, costs hours each time) / Medium / Low / None (stable code) |
| Effort | S (<=2d) / M (3-10d) / L (11-30d) / XL (>30d) |
| Evidence | Verified / Inferred |
| Confidence | High / Medium / Low |

Rank by Interest and Severity high with Effort S or M first. Critical severity is handled as a defect, outside refactor ranking.

## 3. Decision rules (defaults; say when you deviate)

| Situation | Verdict |
|---|---|
| Interest None/Low, area stable, no roadmap work planned | LEAVE |
| Interest Medium, but a safe fix needs tests that don't exist | CONTAIN first (characterization tests, interface boundary), then revisit |
| Payback < 3 months, effort S-M, fix risk Low-Medium | REFACTOR-TARGETED now |
| Payback 3-9 months and planned work touches the area | REFACTOR-TARGETED, folded into that work |
| Payback 3-9 months and no planned work | CONTAIN or LEAVE |
| Payback > 12 months | LEAVE (CONTAIN if risk is the issue) |
| Subsystem with High interest, many findings sharing one root cause (e.g. wrong abstraction), effort L-XL | REFACTOR-PROGRAM, staged, with rollback |
| Not enough data to estimate interest | INSUFFICIENT-DATA plus a collection list |

Tie-breakers: prefer reversible moves; prefer changes that increase verifiability (tests, types, fake boundaries), because they lower the cost of every later decision.

## 4. When REWRITE is allowed

All must hold, each backed by evidence in the report:
1. The core design assumption is wrong and every change fights it (not merely "the code is messy").
2. An incremental path (strangler, branch by abstraction, adapter layer) was examined and is infeasible or costs more, with reasons.
3. Behavior is specified, or can be captured by tests or recordings, so parity is checkable.
4. The component is bounded by a clear interface so old and new can run side by side.
5. Payback is credible even at the high end of the effort range.

Otherwise downgrade to REFACTOR-PROGRAM using a strangler approach.

## 5. Incremental strategies (pick one per REFACTOR verdict)

- **Characterization tests first**: pin current behavior (including recorded LLM and tool traces for AI code) before moving anything.
- **Branch by abstraction**: introduce an interface, route the old implementation through it, build the new one behind it, switch by flag.
- **Strangler**: route a slice of call sites or traffic to the new component and grow it until the old one is empty.
- **Extract and isolate**: split a god module into cohesive units without changing behavior; ship each extraction alone.
- **Shadow / parallel run**: run old and new, compare outputs, switch when parity is shown (good for data-layer and agent-loop changes).

## 6. Conditions and triggers (always include)

For each verdict list what would change it: a feature touching the area, a second incident within 90 days, team growth, a dependency end-of-life date, a provider API deprecation, a measurable rise in cycle time. A verdict without triggers is incomplete.
