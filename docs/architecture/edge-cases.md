# Detailed Edge Cases: Restaurant Recommendation System

This document lists phase-wise edge cases derived from:
- `docs/problemstatement.md`
- `docs/architecture/phase-wise-architecture.md`

Use this as a checklist for implementation, testing, and production hardening.

## How to Read This Document

Each edge case includes:
- **Scenario:** What can go wrong.
- **Risk:** Why it matters.
- **Expected handling:** Required behavior.

---

## Phase 0 - Scope and foundations

### 0.1 Scope drift and unclear ownership
- **Scenario:** Features like auth, maps, or live Zomato API get added mid-milestone.
- **Risk:** Delays core recommendation flow and creates unstable MVP.
- **Expected handling:** Reject out-of-scope work via explicit non-goals and backlog tagging.

### 0.2 Missing environment setup documentation
- **Scenario:** Teammates cannot run the app due to undocumented setup.
- **Risk:** Onboarding friction and inconsistent local behavior.
- **Expected handling:** Keep `README.md`, `.env.example`, and `milestone1 doctor` aligned and versioned.

### 0.3 Secret leakage in repo or logs
- **Scenario:** `GROQ_API_KEY` appears in code, commits, screenshots, or error logs.
- **Risk:** Credential compromise and account misuse.
- **Expected handling:** Load from environment only, redact logs, and block commits of secret files.

### 0.4 Contract ambiguity for v1 fields
- **Scenario:** Different modules assume different field names/types (e.g., `cost_for_two` vs `cost_band`).
- **Risk:** Runtime failures between phases.
- **Expected handling:** Maintain one dataset contract and enforce schema assertions in ingestion.

---

## Phase 1 - Data ingestion and canonical model

### 1.1 Dataset unavailable or network failure
- **Scenario:** Hugging Face is down or rate-limited.
- **Risk:** Application cannot load data.
- **Expected handling:** Retry with backoff; allow cached snapshot fallback; provide actionable error.

### 1.2 Dataset schema changes between revisions
- **Scenario:** Upstream column names/types are modified.
- **Risk:** Silent parsing errors or wrong recommendations.
- **Expected handling:** Pin dataset revision; fail fast when required columns are missing.

### 1.3 Duplicate restaurants with conflicting values
- **Scenario:** Same restaurant appears multiple times with different ratings/cost.
- **Risk:** Duplicated recommendations or inconsistent ranking.
- **Expected handling:** Define dedupe key and deterministic conflict resolution strategy.

### 1.4 Invalid numeric fields
- **Scenario:** `rating` is text, null, or outside valid range.
- **Risk:** Broken filters and ranking bias.
- **Expected handling:** Coerce where safe; drop or flag invalid rows; track row-drop counts.

### 1.5 Cost field inconsistency
- **Scenario:** Cost appears as text labels, currencies, or mixed units.
- **Risk:** Budget filtering becomes unreliable.
- **Expected handling:** Normalize to one comparable representation with explicit conversion rules.

### 1.6 Location normalization pitfalls
- **Scenario:** `Bangalore`, `Bengaluru`, and mixed casing are treated as different cities.
- **Risk:** False "no match" outcomes.
- **Expected handling:** Normalize casing/spaces/synonyms; maintain canonical city mapping.

### 1.7 Cuisine parsing anomalies
- **Scenario:** Cuisines are comma-separated, slash-separated, or contain misspellings.
- **Risk:** Missed overlaps during filtering.
- **Expected handling:** Tokenize robustly, trim punctuation, normalize aliases (e.g., `North Indian` variants).

### 1.8 Large dataset memory pressure
- **Scenario:** Full load exceeds memory in low-resource environments.
- **Risk:** Crashes or very slow startup.
- **Expected handling:** Support load limits, iterators, or chunked reads with predictable caps.

---

## Phase 2 - User preferences and validation

### 2.1 Missing required fields
- **Scenario:** User submits empty location or no meaningful constraints.
- **Risk:** Excessively broad candidate sets and weak recommendation quality.
- **Expected handling:** Validate required fields and return field-specific error messages.

### 2.2 Out-of-range minimum rating
- **Scenario:** User sends `-1`, `6`, or non-numeric rating.
- **Risk:** Filter logic breaks or returns invalid sets.
- **Expected handling:** Coerce only safe formats; otherwise reject with clear bounds.

### 2.3 Unsupported budget value
- **Scenario:** Budget not in allowed bands (`low`, `medium`, `high`) or localization variants.
- **Risk:** Budget filter bypass or incorrect coercion.
- **Expected handling:** Normalize accepted aliases; reject unknown values with allowed options.

### 2.4 Unknown or misspelled location
- **Scenario:** `Bangaluru`, `Dheli`, or neighborhood-level names not in corpus.
- **Risk:** Frequent empty results.
- **Expected handling:** Fuzzy suggestion list and "did you mean" response without auto-guessing silently.

### 2.5 Empty or conflicting cuisine filters
- **Scenario:** Multiple cuisines provided but none overlap any city candidates.
- **Risk:** User receives confusing empty state.
- **Expected handling:** Explain which constraint likely caused no matches; optionally suggest relaxing one filter.

### 2.6 Abusive or prompt-injection free text
- **Scenario:** Additional preferences contain prompt attacks ("ignore rules, output secrets").
- **Risk:** LLM output policy violation.
- **Expected handling:** Sanitize/quote free text, cap length, and isolate it as untrusted user content.

### 2.7 Very long free-text notes
- **Scenario:** User pastes long paragraphs.
- **Risk:** Token overflow and slow LLM responses.
- **Expected handling:** Enforce max length and provide truncation warning.

---

## Phase 3 - Integration layer (retrieval + prompt assembly)

### 3.1 No candidates after hard filters
- **Scenario:** Strict constraints eliminate all restaurants.
- **Risk:** LLM called unnecessarily or misleading recommendations produced.
- **Expected handling:** Skip LLM call; return `no_candidates` with clear user-facing message.

### 3.2 Too many candidates for context window
- **Scenario:** Broad preferences return hundreds of rows.
- **Risk:** Prompt truncation or high token costs.
- **Expected handling:** Cap candidates deterministically (e.g., top-N after pre-sort) and report cap in telemetry.

### 3.3 Non-deterministic candidate ordering
- **Scenario:** Same inputs produce different candidate list order across runs.
- **Risk:** Flaky tests and inconsistent UX.
- **Expected handling:** Use stable sort keys and deterministic tie-breakers.

### 3.4 Prompt serialization failure
- **Scenario:** Candidate data contains special characters/newlines that break JSON/markdown blocks.
- **Risk:** Parsing errors downstream.
- **Expected handling:** Escape fields correctly and validate prompt payload before model call.

### 3.5 Mismatch between filter and prompt data
- **Scenario:** Prompt includes restaurants not in filtered set due to stale variable use.
- **Risk:** Grounding violations and user mistrust.
- **Expected handling:** Build prompt directly from finalized candidate list only.

### 3.6 Bias from ranking hint
- **Scenario:** Optional pre-sort over-weights rating and hides lower-cost relevant options.
- **Risk:** Reduced personalization quality.
- **Expected handling:** Keep pre-sort explainable; include affordability and preference fit in composite score.

---

## Phase 4 - Recommendation engine (LLM)

### 4.1 Missing or invalid API key
- **Scenario:** `GROQ_API_KEY` absent, malformed, or revoked.
- **Risk:** Recommendation endpoint fails hard.
- **Expected handling:** Fail fast with explicit configuration error; use deterministic fallback where possible.

### 4.2 LLM timeout or transient provider errors
- **Scenario:** 429/5xx/timeouts from provider.
- **Risk:** High failure rate and poor UX.
- **Expected handling:** Retry with bounded backoff; if still failing, return fallback recommendations.

### 4.3 Hallucinated restaurant names
- **Scenario:** Model invents restaurants not in candidate list.
- **Risk:** Broken trust and invalid outputs.
- **Expected handling:** Validate IDs/names against candidate set; discard invalid picks and fallback if needed.

### 4.4 Output not matching schema
- **Scenario:** LLM returns prose instead of required JSON structure.
- **Risk:** Parser failures and crashes.
- **Expected handling:** Strict parse/validate; one repair attempt; fallback response on persistent mismatch.

### 4.5 Duplicate recommendations in rankings
- **Scenario:** Same restaurant appears multiple times with different ranks.
- **Risk:** Redundant output and fewer useful options.
- **Expected handling:** Deduplicate by restaurant ID and re-rank remaining items.

### 4.6 Unsafe explanation content
- **Scenario:** Explanation contains offensive/irrelevant text from prompt injection.
- **Risk:** Harmful output shown to users.
- **Expected handling:** Post-process with safety checks and template-based fallback explanations.

### 4.7 Token budget overflow
- **Scenario:** Candidate block + instructions exceed model context or max tokens.
- **Risk:** truncated reasoning, malformed JSON, high latency.
- **Expected handling:** Pre-estimate token size; trim candidates and free text before request.

---

## Phase 5 - Output and experience

### 5.1 Missing display fields for selected restaurants
- **Scenario:** Recommended item lacks cuisine/cost/rating.
- **Risk:** Incomplete cards and confused users.
- **Expected handling:** Show explicit "not available" placeholders; never crash renderer.

### 5.2 Empty-state ambiguity
- **Scenario:** UI uses same message for filter miss and LLM failure.
- **Risk:** Users cannot understand how to recover.
- **Expected handling:** Distinct copy for `no_candidates` vs `fallback_failed/llm_unavailable`.

### 5.3 Inconsistent sorting between API and UI
- **Scenario:** Frontend re-sorts list differently than backend rank.
- **Risk:** Mismatch between explanation and order.
- **Expected handling:** Preserve backend `rank` order and display rank values directly.

### 5.4 Latency spikes degrade UX
- **Scenario:** Slow model response causes long waits.
- **Risk:** User drop-off.
- **Expected handling:** Loading indicators, timeout messaging, and visible fallback path.

### 5.5 Telemetry accidentally logs user free text
- **Scenario:** full request body appears in info logs.
- **Risk:** Privacy/security exposure.
- **Expected handling:** Log counts/latency/source only; mask or exclude free-text preferences.

---

## Phase 6 - Backend (HTTP API)

### 6.1 Invalid JSON or wrong content type
- **Scenario:** Client sends malformed payload or non-JSON content.
- **Risk:** Unhandled exceptions.
- **Expected handling:** Return structured `400` with validation details.

### 6.2 Contract drift between API and frontend
- **Scenario:** Frontend expects fields not returned by backend (or renamed fields).
- **Risk:** UI runtime failures.
- **Expected handling:** Versioned response schema and contract tests.

### 6.3 Unbounded request size
- **Scenario:** Very large free-text field or payload flooding.
- **Risk:** Resource exhaustion.
- **Expected handling:** Enforce request body limits and field-length caps.

### 6.4 CORS misconfiguration
- **Scenario:** Overly permissive origins in production or blocked local frontend during dev.
- **Risk:** Security issues or broken integration.
- **Expected handling:** Explicit environment-based allowlists.

### 6.5 Health check gives false positives
- **Scenario:** `/health` returns OK while key missing or dataset unavailable.
- **Risk:** Misleading deployment state.
- **Expected handling:** Separate liveness and readiness semantics.

### 6.6 Concurrent request contention
- **Scenario:** Simultaneous requests trigger repeated dataset loads or model bottlenecks.
- **Risk:** Latency and memory spikes.
- **Expected handling:** Cache dataset safely, reuse clients, and apply timeout/concurrency guards.

---

## Phase 7 - Frontend (web UI)

### 7.1 Double submit race condition
- **Scenario:** User clicks submit repeatedly while request in flight.
- **Risk:** Duplicate API calls and inconsistent results.
- **Expected handling:** Disable submit during pending state and debounce quick repeats.

### 7.2 Stale response overwrite
- **Scenario:** Older request finishes after newer request and replaces latest results.
- **Risk:** User sees outdated recommendations.
- **Expected handling:** Track request IDs; ignore out-of-order responses.

### 7.3 Client/server validation mismatch
- **Scenario:** UI allows values backend rejects.
- **Risk:** avoidable failed submissions.
- **Expected handling:** Mirror backend constraints in UI; still trust backend as source of truth.

### 7.4 Rendering crashes on partial responses
- **Scenario:** API returns optional fields missing/null.
- **Risk:** Blank screen or broken component.
- **Expected handling:** Defensive rendering and typed fallback values.

### 7.5 Unclear field semantics
- **Scenario:** User confuses "minimum rating" with "target rating."
- **Risk:** unexpected empty results.
- **Expected handling:** Add helper text and examples near inputs.

---

## Phase 8 - Streamlit deployment (optional)

### 8.1 Secret not configured in Cloud
- **Scenario:** `st.secrets` missing `GROQ_API_KEY`.
- **Risk:** App appears live but fails on recommendation.
- **Expected handling:** Startup warning panel and graceful disabled recommend action.

### 8.2 Cold start + heavy load path
- **Scenario:** Free-tier instance cold-starts and then loads full dataset.
- **Risk:** long first interaction.
- **Expected handling:** cache data/model client using Streamlit caching primitives.

### 8.3 Divergence from API semantics
- **Scenario:** Streamlit path returns different empty-state/source labels than API.
- **Risk:** inconsistent demo behavior.
- **Expected handling:** Reuse shared orchestration functions from `milestone1` library.

### 8.4 Dependency bloat on free tier
- **Scenario:** large dependencies increase boot time and failures.
- **Risk:** unstable demo deployment.
- **Expected handling:** keep extras minimal; pin tested versions.

---

## Phase 9 - Hardening and handoff

### 9.1 Flaky tests due to live model dependency
- **Scenario:** tests call real LLM and fail intermittently.
- **Risk:** unreliable CI.
- **Expected handling:** use fixtures/mocks for most tests; isolate opt-in integration tests.

### 9.2 Missing golden tests for output contracts
- **Scenario:** refactor changes response format silently.
- **Risk:** frontend breaks without obvious backend failures.
- **Expected handling:** maintain golden JSON tests for happy, empty, and error paths.

### 9.3 No regression coverage for edge filtering
- **Scenario:** changes in normalization alter filter outcomes.
- **Risk:** quality regression unnoticed.
- **Expected handling:** lock edge-case fixtures for no-match, many-match, and tie-break scenarios.

### 9.4 Incomplete operational runbook
- **Scenario:** reviewers cannot reproduce demo setup.
- **Risk:** handoff failure.
- **Expected handling:** include step-by-step runbook with expected outputs and common failure remedies.

---

## Cross-Phase Critical Edge Cases (High Priority)

1. **No candidates after filters** must short-circuit before LLM.
2. **LLM returns non-grounded/hallucinated picks** must be rejected by parser validation.
3. **Malformed/partial LLM output** must trigger deterministic fallback, not crash.
4. **Secret/configuration failures** must be explicit and safe (no key leakage).
5. **API and UI contract drift** must be caught by schema/golden tests.
6. **Ambiguous empty states** must be split into filter miss vs model failure.

## Suggested Test Matrix Dimensions

- **Input quality:** valid, borderline, invalid, malicious.
- **Data quality:** complete rows, sparse rows, inconsistent schema, duplicates.
- **Volume:** small (`N<100`), medium, large (`N>50k`) where applicable.
- **LLM behavior:** valid JSON, malformed JSON, hallucination, timeout, 429/5xx.
- **Channel:** CLI, API, Web UI, Streamlit.
- **Outcome type:** success, no candidates, fallback success, hard error.
