# Phase 0 Scope (Milestone 1)

## Product Slice
- Primary surface: basic web UI, which is the source of user input and the main results display for Milestone 1.
- Secondary surface: CLI for diagnostics and developer workflows.

## Scope for Milestone 1
- Dataset-backed recommendations using Hugging Face Zomato dataset.
- User preferences: location, budget, cuisines, minimum rating, optional additional text.
- LLM-generated explanations grounded in filtered candidate restaurants.

## Non-Goals
- User authentication and profiles.
- Live Zomato or third-party restaurant APIs.
- Maps and geospatial browsing.
- Production-scale infrastructure/SLA guarantees.

## Baseline Assumptions
- Python-first backend/library implementation.
- Secrets are provided through environment variables; never committed.
- `milestone1 info` and `milestone1 doctor` are the initial operational checks.
