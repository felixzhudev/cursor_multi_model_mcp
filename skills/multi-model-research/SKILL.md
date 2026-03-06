---
name: multi-model-research
description: Multi-model research workflow for Cursor Agent mode. Queries OpenAI (GPT), Google (Gemini), and Anthropic (Claude) via the multi-model-llm MCP. Compare, reconcile, and synthesize answers from 2–4 models. Agent mode only.
user-invocable: true
---

This skill runs the multi-model research workflow. It works with the **multi-model-llm** MCP from this repo. Phase 2 lets the user choose one, two, or all three MCP models (openai, anthropic, google), so 2–4 models total including the model already used in Cursor. Enable the multi-model-llm MCP in Cursor before using this skill.

---

## Phase 1 — Problem Framing (Before Any Model Comparison)

1. Define:
   - Objective
   - Constraints (time, budget, risk tolerance, context)
   - Evaluation criteria (what "best" means)

2. Identify:
   - Unknowns
   - Assumptions
   - Risk areas

Do not proceed without explicit framing.

---

## Phase 2 — Parallel Multi-Model Reasoning

**Model choice:** The user specifies which MCP model(s) to use: **openai**, **google**, **anthropic** — one, two, or all three. If the user is in Auto mode or uses a different model in Cursor, suggest a strong reasoning model for this workflow.

**Steps:**

1. Get the user's choice: one, two, or all three of `openai`, `google`, `anthropic`. If not specified, ask.
2. Build one clear prompt (and optional system_prompt) from the framed objective and context from Phase 1.
3. **Produce your own structured answer** (Cursor) to that prompt. For each model output:
   - Provide a structured answer or plan
   - State assumptions clearly
   - Identify trade-offs
   - Highlight risks or blind spots
   - Note areas of uncertainty
4. **Call the multi-model-llm MCP** tool **query_llm_models**(prompt, models, system_prompt) with `models` = the user's choice (e.g. `["anthropic"]`, `["openai", "google"]`, or `["openai", "google", "anthropic"]`).
5. Keep each model's output clearly separated and labeled (e.g. "Cursor", "OpenAI (GPT)", "Google (Gemini)", "Anthropic (Claude)").

---

## Phase 3 — Structured Comparison

### A. Convergence Mapping

List:
- Core agreements
- Repeated recommendations
- Shared risk assessments

### B. Divergence Mapping

List:
- Conflicting strategies
- Differing assumptions
- Risk tolerance differences
- Resource allocation differences

---

## Phase 4 — Reconciliation Logic

Use explicit decision criteria:
- Robustness under uncertainty
- Alignment with constraints
- Scalability
- Empirical support
- Risk-adjusted outcome

Then choose one from the following:

### Option A — Synthesize
Combine strongest parts into one solution.

### Option B — Rank
Rank full alternatives with justification.

### Option C — Conditional Recommendation
Recommend different solutions based on scenario triggers.

Reconciliation must be justified — not intuitive.

---

## Phase 5 — Evidence Escalation (If Disagreement or High Stakes)

Trigger if:
- Models disagree in important ways
- Claims depend on uncertain facts
- Domain needs current best practice
- Stakes are financial, legal, or operational

Actions:
- Do targeted web search
- Prefer peer-reviewed research, official docs, regulatory sources, reputable institutions
- Avoid blogs unless they link to primary sources
- Cross-verify critical claims

State clearly:
- What evidence changed
- What was corrected or removed

---

## Phase 6 — Full Internal Audit

Check for:
- Logical contradictions
- Dropped constraints
- Hidden assumptions
- Inconsistent terminology
- Unsupported claims
- Overgeneralization
- Scope drift

Fix and re-audit until coherent.

---

## Phase 7 — Reference Verification

If references are used:
- Verify each link works
- Confirm source authority and recency where needed
- Remove stale or unverifiable references

If you made corrections, state them.

---

## Phase 8 — Final Coherence Pass (Hard Stop)

Before delivery:
- Does the solution answer the objective?
- Is it decision-ready?
- Are trade-offs clear?
- Is risk stated clearly?
- Is reasoning traceable?

Only deliver after passing this gate.

---

## Operational Safeguards

**Cost and latency:** Do not loop indefinitely. Max two reconciliation iterations. Max one evidence escalation unless new contradictions appear.

**Failure handling:** If models stay irreconcilable, evidence is inconclusive, or data is insufficient: present structured uncertainty, give bounded recommendations, and state limits of confidence.

**Output:** Final output must not expose internal chain-of-thought. Present only synthesized reasoning. Avoid raw multi-model transcripts. Keep it structured and decision-oriented.

---

## Success Criteria Checklist

- [ ] Problem framing completed
- [ ] 2, 3, or 4 distinct models considered (Cursor + one, two, or all three MCP: openai, google, anthropic)
- [ ] Convergences and divergences mapped
- [ ] Reconciliation justified
- [ ] Evidence escalation applied when needed
- [ ] Full logical audit completed
- [ ] References verified or removed
- [ ] Final output coherent and decision-ready
