# Milestone 1 - AI Restaurant Recommendation System

This repository contains a phase-wise implementation of an AI-powered restaurant recommendation system inspired by Zomato.

## Architecture Overview

The system is now structured with a proper backend API and frontend web UI:

- **Phase 6 Backend**: FastAPI-based HTTP API server
- **Phase 7 Frontend**: React + TypeScript web application
- **Phases 0-5**: Core recommendation pipeline (CLI-based)

## Quick Start with Web UI

### 1) Backend Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install with API and LLM dependencies
pip install -e ".[api,llm,ingestion,dev]"

# Configure environment
copy .env.example .env
# Edit .env to add GROQ_API_KEY

# Start the API server
python run_api.py
```

The API will be available at `http://localhost:8000`

### 2) Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3) Test the System

1. Open `http://localhost:5173` in your browser
2. Fill in your preferences (location, budget, cuisines, rating)
3. Click "Get Recommendations" to see AI-powered suggestions

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/meta` - Available cities, cuisines, and options
- `POST /api/v1/recommendations` - Generate recommendations

## CLI Usage (Development)

The original CLI interface is still available for development and testing:

```bash
milestone1 info
milestone1 doctor
```

## Phase 1 Ingestion

Phase 1 package:
- `src/milestone1/phase1_ingestion/`
- Provides `Restaurant`, `iter_restaurants`, `load_restaurants`, normalization, schema assertions, and Hugging Face revision pin.

Install ingestion extras (for Hugging Face source):

```bash
py -m pip install -e ".[ingestion,dev]"
```

Smoke test ingestion:

```bash
milestone1 ingest-smoke --limit 25
milestone1 ingest-smoke --source local --local-path sample.json --limit 10
```

Run tests:

```bash
pytest -q
RUN_HF_INTEGRATION=1 pytest -m integration
```

## Phase 2 Preferences

Phase 2 package:
- `src/milestone1/phase2_preferences/`
- Provides `UserPreferences`, `preferences_from_mapping`, `allowed_cities_from_restaurants`, and `allowed_city_names`.

Parse preferences from CLI:

```bash
milestone1 prefs-parse --location Delhi --budget-band medium --cuisines "Italian,Chinese" --minimum-rating 4.0
```

Validate city name against corpus:

```bash
milestone1 prefs-parse --location Delhi --budget-band medium --cuisines "Italian,Chinese" --minimum-rating 4.0 --validate-city --city-source local --city-local-path tests/fixtures/restaurants_sample.json
```

On success, command prints normalized JSON.  
On validation failure, command prints field errors to stderr and returns non-zero.

## Phase 3 Integration

Phase 3 package:
- `src/milestone1/phase3_integration/`
- Provides:
  - `filter_and_rank` (hard constraints + deterministic ranking)
  - `build_prompt_payload`
  - `build_integration_output`

Build candidates and prompt payload from CLI:

```bash
milestone1 prompt-build --location Delhi --budget-band medium --cuisines "Italian,Chinese" --minimum-rating 4.0 --source local --local-path tests/fixtures/restaurants_sample.json --candidate-cap 10
```

Output contains stable:
- `candidates[]`
- `prompt_payload`

without calling an LLM.

## Phase 4 Recommendation (Groq)

Phase 4 package:
- `src/milestone1/phase4_llm/`
- Provides:
  - Groq OpenAI-compatible client
  - JSON ranking parser + grounding checks
  - deterministic fallback
  - `recommend_with_groq`

Run end-to-end recommendation:

```bash
milestone1 recommend --location Delhi --budget-band high --cuisines "Chinese,Italian" --minimum-rating 4.0 --source local --local-path tests/fixtures/restaurants_sample.json
```

Required env:
- `GROQ_API_KEY`
- Optional: `GROQ_MODEL`

Behavior:
- Uses Groq when available.
- Retries transient failures.
- Falls back to deterministic top-k recommendations if LLM output is invalid or API call fails.

## Phase 5 Output and Experience

Phase 5 package:
- `src/milestone1/phase5_output/`
- Provides:
  - markdown/plain recommendation rendering
  - distinct empty-state copy
  - stderr telemetry JSON (latency + counts)
  - `recommend_run` orchestration

Run readable end-to-end output:

```bash
milestone1 recommend-run --location Bellandur --budget-band high --cuisines "North Indian,Chinese" --minimum-rating 4.0 --source hf --top-k 5 --output-format plain
```

For markdown output:

```bash
milestone1 recommend-run --location Bellandur --budget-band high --cuisines "North Indian,Chinese" --minimum-rating 4.0 --source hf --top-k 5 --output-format markdown
```

## Phase 6 Backend (HTTP API)

Phase 6 package:
- `src/milestone1/phase6_api/`
- Provides:
  - FastAPI application with CORS support
  - `POST /api/v1/recommendations` endpoint
  - `GET /health` and `GET /api/v1/meta` endpoints
  - Structured request/response models
  - Error handling and telemetry

Start API server:

```bash
python run_api.py
```

API documentation available at `http://localhost:8000/docs`

## Phase 7 Frontend (Web UI)

Phase 7 package:
- `frontend/` directory
- React + TypeScript + Tailwind CSS
- Provides:
  - Preference form with validation
  - Real-time recommendation display
  - Loading states and error handling
  - Responsive design
  - API integration with backend

Start frontend development server:

```bash
cd frontend
npm install
npm run dev
```

## Key Documents

- `docs/problemstatement.md`
- `docs/architecture/phase-wise-architecture.md`
- `docs/architecture/edge-cases.md`
- `phase0-scope.md`
- `dataset-contract.md`
