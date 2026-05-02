# Phase-Wise Architecture: Restaurant Recommendation System

This document breaks implementation into phases aligned to the workflow in `docs/problemstatement.md`:

`data ingestion -> user input -> integration (filter + prompt prep) -> LLM recommendation -> output display`.

## Phase 0 - Scope and foundations

### Goals
- Define the v1 product shape and engineering boundaries before implementation.

### Outcomes
- **Product slice:** Basic web UI as the primary user input and results surface for milestone 1 (`phase0-scope.md`), with CLI retained for developer diagnostics.
- **Stack:** Confirm language/runtime, dependency manager, and secret handling (`.env`, never committed).
- **Dataset contract:** Confirm Hugging Face dataset fields supported in v1, including column-to-internal mapping.
- **Non-goals:** Explicitly defer user accounts, live Zomato API, maps, and other out-of-scope work.

### Exit criteria
- Written assumptions for stack, v1 UI, and supported preference fields.
- A local command path to run the app end-to-end once downstream phases are in place.

### Implemented artifacts
- `src/milestone1/phase0/` (paths, scope, info/doctor commands)
- `phase0-scope.md`
- `dataset-contract.md`
- `README.md`
- `.env.example`
- CLI: `milestone1 info`, `milestone1 doctor`

## Phase 1 - Data ingestion and canonical model

### Responsibilities
- **Acquisition:** Download/stream `ManikaSaini/zomato-restaurant-recommendation`; cache locally for faster iteration.
- **Normalization:** Clean types (e.g., ratings numeric; cost as enum or numeric band), handle nulls, deduplicate if needed.
- **Canonical schema:** Define internal `Restaurant` model with `name`, `location`, `cuisines`, `cost`, `rating`, plus prompt-useful fields.

### Exit criteria
- One module/package loads data into typed in-memory records (or queryable table).
- Unit tests validate parsing and normalization on sample rows.

### Implemented artifacts
- `src/milestone1/phase1_ingestion/`:
  - `Restaurant`
  - `load_restaurants` / `iter_restaurants`
  - normalization pipeline
  - Hub revision pin
  - schema assertions
- CLI: `milestone1 ingest-smoke --limit N`
- Integration tests: `RUN_HF_INTEGRATION=1 pytest -m integration`

## Phase 2 - User preferences and validation

### Responsibilities
- **Preference model:** Structured fields for `location`, `budget band`, `cuisines`, `minimum rating`, and optional free text.
- **Validation:** Coerce/reject invalid values (unknown location, out-of-range rating), with clear UI/CLI error messages.

### Exit criteria
- Preferences from form/API/CLI deserialize into one object consumed by the filter layer.
- Validation failures are visible and actionable for users.

### Implemented artifacts
- `src/milestone1/phase2_preferences/`:
  - `UserPreferences`
  - `preferences_from_mapping`
  - optional city corpus check (`allowed_city_names`)
  - `allowed_cities_from_restaurants`
- CLI: `milestone1 prefs-parse ...` (JSON on success, field errors on stderr)

## Phase 3 - Integration layer (retrieval + prompt assembly)

### Responsibilities
- **Deterministic filter:** Apply hard constraints first (location, minimum rating, budget, cuisine overlap), then cap candidates for LLM context (e.g., 15-50).
- **Ranking hint (optional):** Pre-sort by rating or composite score for stronger default ordering.
- **Prompt builder:** Build system/user messages (or structured prompt) containing:
  - user preferences
  - candidate set (markdown/JSON)
  - grounding rule: recommend only from list
  - required output format for Phase 4 parser

### Exit criteria
- For `preferences + dataset`, produce stable `candidates[]` and `prompt_payload` without calling LLM.
- Edge-case tests for no matches and too many matches.

### Implemented artifacts
- `src/milestone1/phase3_integration/`:
  - `filter_and_rank`
  - `build_prompt_payload`
  - `build_integration_output`
- CLI: `milestone1 prompt-build`

## Phase 4 - Recommendation engine (LLM)

### Responsibilities
- **Model I/O:** Thin client with `temperature`, `max_tokens`, `timeout`; API key from environment.
- **Grounding:** Prompt enforces candidate-only recommendations; return empty/refusal when no grounded option exists.
- **Structured output:** Request JSON (e.g., `rankings[]` with `restaurant_id`, `rank`, `explanation`) or strict markdown, then parse + validate.
- **Resilience:** Retry transient model errors and fall back to deterministic top-k with template explanations.

### Exit criteria
- End-to-end call returns ranked items with explanations.
- Parser enforces structure; failures degrade gracefully.

### Implemented artifacts
- `src/milestone1/phase4_llm/`:
  - Groq OpenAI-compatible client
  - JSON ranking parser
  - deterministic fallback
  - `recommend_with_groq`
- CLI: `milestone1 recommend`
- Secrets: `GROQ_API_KEY` (see `.env.example`)

## Phase 5 - Output and experience

### Responsibilities
- **Rendering:** Show `name`, `cuisine`, `rating`, `estimated cost`, and AI explanation per recommendation.
- **Empty states:** Distinguish "no restaurants matched filters" from "LLM could not justify picks."
- **Light observability:** Track latency, token usage (if available), and candidate/filter counts; avoid logging PII by default.

### Exit criteria
- One-run demo path from input to readable results.
- Copy and layout satisfy minimum fields in `problemstatement.md`.

### Implemented artifacts
- `src/milestone1/phase5_output/`:
  - markdown/plain renderers
  - empty-state copy
  - stderr telemetry JSON
- CLI: `milestone1 recommend-run`

## Phase 6 - Backend (HTTP API)

### Responsibilities
- **Role:** Thin service owning server-side secrets (`GROQ_API_KEY`), dataset access, and orchestration; browser never calls Groq/Hugging Face directly.
- **Contract:** Stable JSON request/response for recommendations:
  - request aligned with Phase 2 keys
  - response includes ranked items (ids + display fields + explanations)
  - includes source (`llm`, `fallback`, `no_candidates`)
  - includes filter/candidate counts and optional non-sensitive telemetry
- **Endpoints (v1):**
  - `POST /api/v1/recommendations`
  - `GET /health`
  - optional `GET /api/v1/meta` for capped allowed-cities hints
- **Cross-cutting:** Phase 4-aligned timeouts, structured logs, dev-only CORS allowlist, request-size limits for free-text fields.
- **Stack:** Python-first (`FastAPI` or `Flask`) sharing the `milestone1` library.

### Exit criteria
- Frontend completes recommendation flow using API only.
- API outcomes match `milestone1 recommend` / `recommend-run` for same inputs (allowing cache variation).

### Implemented artifacts
- `src/milestone1/phase6_api/`:
  - FastAPI application with async support
  - Pydantic request/response models
  - Service layer with timeout handling
  - CORS middleware with development allowlist
  - Structured logging and telemetry
  - Request size validation
- `run_api.py` - API server entry point
- CLI: `python run_api.py` (starts server on http://localhost:8000)
- API docs: http://localhost:8000/docs

## Phase 7 - Frontend (web UI)

### Responsibilities
- **Role:** Primary user surface (`phase0-scope.md`) with preference form + recommendation list.
- **Data flow:** Browser communicates only with Phase 6 API.
- **UI contract:** Show `name`, `cuisines`, `rating`, `estimated cost`, AI explanation.
- **Empty states:** Keep distinct copy for:
  - no filter matches
  - no grounded model picks
- **UX:** Loading state, inline validation, disabled submit while pending, optional "copy as Markdown."
- **Stack:** Choose one and stay consistent (e.g., React + Vite SPA or HTMX + templates).

### Exit criteria
- README demo path exists: start API + UI, submit preferences, see recommendations (or intentional empty state).

### Implemented artifacts
- `frontend-nextjs/`:
  - Next.js 14 with App Router and TypeScript
  - Tailwind CSS with custom design system
  - Preference form with validation and inline feedback
  - Restaurant recommendation cards with copy-as-Markdown
  - Loading states, error handling, and empty states
  - Responsive design for mobile and desktop
  - API integration with Phase 6 backend
- README with complete demo instructions
- CLI: `npm run dev` (starts frontend on http://localhost:3000)
- Components: PreferenceForm, RestaurantCard, EmptyState, Header, Footer

## Phase 8 - Deployment using Streamlit

### Responsibilities
- **Role:** Single-process Python deployment path replicating CLI/API flow:
  - widgets -> load corpus -> validate -> filter + prompt -> `recommend_with_groq` -> render cards
- **Secrets:** `GROQ_API_KEY` (optional `GROQ_MODEL`) via `st.secrets` or environment variables; no client-side key exposure.
- **Deployment:** Streamlit Community Cloud (free tier) or Docker-based alternatives.
- **Relationship to phases 6-7:** Complementary demo-friendly path; may import `milestone1` directly or call Phase 6 API.
- **UX scope:** `selectbox`, `text_input`, `slider`, `spinner`, optional `expander` for raw JSON/telemetry.
- **Styling:** Streamlit theming with custom CSS for brand consistency (Rosy Hearth colors from Phase 7).
- **Performance:** Caching for restaurant dataset and API responses to improve user experience.

### Exit criteria
- `README` or `docs/streamlit-deploy.md` documents local run and Cloud deploy.
- Reviewer can open hosted URL and complete one recommendation flow or reach an intentional empty state.
- Streamlit app matches Phase 7 UI design and functionality.
- Deployed app handles concurrent users and maintains responsive performance.

### Implemented artifacts
- `src/milestone1/phase8_streamlit/app.py`
- `streamlit_app.py` (repo root Cloud entrypoint)
- `requirements-streamlit.txt` with Streamlit dependencies
- `src/milestone1/phase8_streamlit/streamlit_theme.py` for custom styling
- `docs/streamlit-deploy.md` with deployment instructions
- `streamlit.toml` configuration file
- Dockerfile for containerized deployment

## Phase 9 - Hardening and handoff (optional, recommended)

### Responsibilities
- Add automated tests for filters, prompt shape, JSON parsing, and API contracts (happy/empty/error goldens).
- Expand README with setup, `GROQ_API_KEY`, API + UI runs, CLI fallback commands, and known limitations.
- Document cost/latency levers: candidate caps, model choice, load limits, optional caching strategy.

### Exit criteria
- Reproducible runbook + stable tests for core flows.
- Clear handoff package for reviewers and future contributors.
