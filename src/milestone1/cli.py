from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from .phase0.doctor import run_doctor
from .phase0.info import build_info_text
from .phase1_ingestion import (
    HF_DATASET_NAME,
    HF_DATASET_REVISION,
    load_restaurants,
    summarize_restaurants,
)
from .phase2_preferences import (
    PreferencesValidationError,
    allowed_city_names,
    preferences_from_mapping,
)
from .phase3_integration import build_integration_output
from .phase4_llm import recommend_with_groq
from .phase5_output import recommend_run


def _cmd_info() -> int:
    print(build_info_text())
    return 0


def _cmd_doctor() -> int:
    results = run_doctor()
    overall_ok = True
    print("milestone1 doctor")
    for result in results:
        icon = "OK" if result.ok else "FAIL"
        print(f"[{icon}] {result.name}: {result.details}")
        overall_ok = overall_ok and result.ok
    return 0 if overall_ok else 1


def _cmd_ingest_smoke(limit: int, source: str, local_path: str | None) -> int:
    try:
        restaurants = load_restaurants(source=source, local_path=local_path, limit=limit)
    except Exception as exc:
        print(f"ingest-smoke failed: {exc}", file=sys.stderr)
        return 1

    summary = summarize_restaurants(restaurants)
    output = {
        "source": source,
        "dataset_name": HF_DATASET_NAME if source == "hf" else "local",
        "dataset_revision": HF_DATASET_REVISION if source == "hf" else None,
        "limit": limit,
        "summary": summary,
    }
    print(json.dumps(output, indent=2))
    return 0


def _cmd_prefs_parse(args: argparse.Namespace) -> int:
    payload = {
        "location": args.location,
        "budget_band": args.budget_band,
        "cuisines": args.cuisines,
        "minimum_rating": args.minimum_rating,
        "additional_preferences": args.additional_preferences,
    }
    allowed_cities: set[str] | None = None
    if args.validate_city:
        try:
            allowed_cities = allowed_city_names(
                source=args.city_source,
                local_path=args.city_local_path,
                limit=args.city_limit,
            )
        except Exception as exc:
            print(f"prefs-parse city validation setup failed: {exc}", file=sys.stderr)
            return 1

    try:
        preferences = preferences_from_mapping(payload, allowed_city_names=allowed_cities)
    except PreferencesValidationError as exc:
        for error in exc.errors:
            print(f"{error.field}: {error.message}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "location": preferences.location,
                "budget_band": preferences.budget_band,
                "cuisines": preferences.cuisines,
                "minimum_rating": preferences.minimum_rating,
                "additional_preferences": preferences.additional_preferences,
            },
            indent=2,
        )
    )
    return 0


def _cmd_prompt_build(args: argparse.Namespace) -> int:
    pref_payload = {
        "location": args.location,
        "budget_band": args.budget_band,
        "cuisines": args.cuisines,
        "minimum_rating": args.minimum_rating,
        "additional_preferences": args.additional_preferences,
    }
    try:
        preferences = preferences_from_mapping(pref_payload)
        output = build_integration_output(
            preferences,
            source=args.source,
            local_path=args.local_path,
            load_limit=args.load_limit,
            candidate_cap=args.candidate_cap,
        )
    except PreferencesValidationError as exc:
        for error in exc.errors:
            print(f"{error.field}: {error.message}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"prompt-build failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(output, indent=2))
    return 0


def _cmd_recommend(args: argparse.Namespace) -> int:
    pref_payload = {
        "location": args.location,
        "budget_band": args.budget_band,
        "cuisines": args.cuisines,
        "minimum_rating": args.minimum_rating,
        "additional_preferences": args.additional_preferences,
    }
    try:
        preferences = preferences_from_mapping(pref_payload)
        output = recommend_with_groq(
            preferences,
            source=args.source,
            local_path=args.local_path,
            load_limit=args.load_limit,
            candidate_cap=args.candidate_cap,
            top_k=args.top_k,
            timeout_s=args.timeout_s,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    except PreferencesValidationError as exc:
        for error in exc.errors:
            print(f"{error.field}: {error.message}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"recommend failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(output, indent=2))
    return 0


def _cmd_recommend_run(args: argparse.Namespace) -> int:
    pref_payload = {
        "location": args.location,
        "budget_band": args.budget_band,
        "cuisines": args.cuisines,
        "minimum_rating": args.minimum_rating,
        "additional_preferences": args.additional_preferences,
    }
    try:
        preferences = preferences_from_mapping(pref_payload)
        rendered, _ = recommend_run(
            preferences,
            source=args.source,
            local_path=args.local_path,
            load_limit=args.load_limit,
            candidate_cap=args.candidate_cap,
            top_k=args.top_k,
            timeout_s=args.timeout_s,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            output_format=args.output_format,
            emit_stderr_telemetry=True,
        )
    except PreferencesValidationError as exc:
        for error in exc.errors:
            print(f"{error.field}: {error.message}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"recommend-run failed: {exc}", file=sys.stderr)
        return 1

    print(rendered)
    return 0


def main(argv: list[str] | None = None) -> int:
    # Load local .env once for CLI commands (does not override existing env).
    load_dotenv(dotenv_path=Path.cwd() / ".env", override=False)

    parser = argparse.ArgumentParser(prog="milestone1")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("info", help="Print phase 0 project information.")
    subparsers.add_parser("doctor", help="Run environment and project checks.")
    ingest_parser = subparsers.add_parser(
        "ingest-smoke",
        help="Run phase 1 ingestion smoke check.",
    )
    ingest_parser.add_argument("--limit", type=int, default=25, help="Maximum rows to load.")
    ingest_parser.add_argument(
        "--source",
        choices=["hf", "local"],
        default="hf",
        help="Ingestion source (Hugging Face or local file).",
    )
    ingest_parser.add_argument(
        "--local-path",
        default=None,
        help="Path to local CSV/JSON/JSONL source when --source local.",
    )
    prefs_parser = subparsers.add_parser(
        "prefs-parse",
        help="Parse and validate phase 2 user preferences.",
    )
    prefs_parser.add_argument("--location", required=True, help="User location or city.")
    prefs_parser.add_argument(
        "--budget-band",
        required=True,
        help="Budget band: low|medium|high (aliases accepted).",
    )
    prefs_parser.add_argument(
        "--cuisines",
        required=True,
        help="Comma-separated cuisines (e.g. italian,chinese).",
    )
    prefs_parser.add_argument(
        "--minimum-rating",
        required=True,
        help="Minimum rating (0 to 5).",
    )
    prefs_parser.add_argument(
        "--additional-preferences",
        default="",
        help="Optional free-text preferences.",
    )
    prefs_parser.add_argument(
        "--validate-city",
        action="store_true",
        help="Validate location against loaded corpus city names.",
    )
    prefs_parser.add_argument(
        "--city-source",
        choices=["hf", "local"],
        default="hf",
        help="City validation source when --validate-city is set.",
    )
    prefs_parser.add_argument(
        "--city-local-path",
        default=None,
        help="Local source path when --city-source local.",
    )
    prefs_parser.add_argument(
        "--city-limit",
        type=int,
        default=2000,
        help="Row limit for city extraction during validation.",
    )
    prompt_parser = subparsers.add_parser(
        "prompt-build",
        help="Run phase 3 integration (filter + prompt payload).",
    )
    prompt_parser.add_argument("--location", required=True, help="User location.")
    prompt_parser.add_argument("--budget-band", required=True, help="Budget: low|medium|high.")
    prompt_parser.add_argument("--cuisines", required=True, help="Comma-separated cuisines.")
    prompt_parser.add_argument("--minimum-rating", required=True, help="Minimum rating (0..5).")
    prompt_parser.add_argument(
        "--additional-preferences",
        default="",
        help="Optional user free-text preferences.",
    )
    prompt_parser.add_argument(
        "--source",
        choices=["hf", "local"],
        default="local",
        help="Restaurant ingestion source.",
    )
    prompt_parser.add_argument(
        "--local-path",
        default="tests/fixtures/restaurants_sample.json",
        help="Local source path when --source local.",
    )
    prompt_parser.add_argument(
        "--load-limit",
        type=int,
        default=2000,
        help="Maximum restaurants to load before filtering.",
    )
    prompt_parser.add_argument(
        "--candidate-cap",
        type=int,
        default=25,
        help="Maximum candidates included in output/prompt payload.",
    )
    recommend_parser = subparsers.add_parser(
        "recommend",
        help="Run phase 4 recommendation flow with Groq + fallback.",
    )
    recommend_parser.add_argument("--location", required=True, help="User location.")
    recommend_parser.add_argument("--budget-band", required=True, help="Budget: low|medium|high.")
    recommend_parser.add_argument("--cuisines", required=True, help="Comma-separated cuisines.")
    recommend_parser.add_argument("--minimum-rating", required=True, help="Minimum rating (0..5).")
    recommend_parser.add_argument(
        "--additional-preferences",
        default="",
        help="Optional user free-text preferences.",
    )
    recommend_parser.add_argument(
        "--source",
        choices=["hf", "local"],
        default="local",
        help="Restaurant ingestion source.",
    )
    recommend_parser.add_argument(
        "--local-path",
        default="tests/fixtures/restaurants_sample.json",
        help="Local source path when --source local.",
    )
    recommend_parser.add_argument("--load-limit", type=int, default=2000)
    recommend_parser.add_argument("--candidate-cap", type=int, default=25)
    recommend_parser.add_argument("--top-k", type=int, default=5)
    recommend_parser.add_argument("--timeout-s", type=float, default=30.0)
    recommend_parser.add_argument("--temperature", type=float, default=0.2)
    recommend_parser.add_argument("--max-tokens", type=int, default=700)
    recommend_run_parser = subparsers.add_parser(
        "recommend-run",
        help="Run phase 5 user-friendly recommendation output + telemetry.",
    )
    recommend_run_parser.add_argument("--location", required=True, help="User location.")
    recommend_run_parser.add_argument("--budget-band", required=True, help="Budget: low|medium|high.")
    recommend_run_parser.add_argument("--cuisines", required=True, help="Comma-separated cuisines.")
    recommend_run_parser.add_argument("--minimum-rating", required=True, help="Minimum rating (0..5).")
    recommend_run_parser.add_argument("--additional-preferences", default="")
    recommend_run_parser.add_argument("--source", choices=["hf", "local"], default="local")
    recommend_run_parser.add_argument(
        "--local-path",
        default="tests/fixtures/restaurants_sample.json",
        help="Local source path when --source local.",
    )
    recommend_run_parser.add_argument("--load-limit", type=int, default=2000)
    recommend_run_parser.add_argument("--candidate-cap", type=int, default=25)
    recommend_run_parser.add_argument("--top-k", type=int, default=5)
    recommend_run_parser.add_argument("--timeout-s", type=float, default=30.0)
    recommend_run_parser.add_argument("--temperature", type=float, default=0.2)
    recommend_run_parser.add_argument("--max-tokens", type=int, default=700)
    recommend_run_parser.add_argument(
        "--output-format",
        choices=["plain", "markdown"],
        default="plain",
        help="Rendered output format for recommendations.",
    )

    args = parser.parse_args(argv)
    if args.command == "info":
        return _cmd_info()
    if args.command == "doctor":
        return _cmd_doctor()
    if args.command == "ingest-smoke":
        return _cmd_ingest_smoke(
            limit=args.limit,
            source=args.source,
            local_path=args.local_path,
        )
    if args.command == "prefs-parse":
        return _cmd_prefs_parse(args)
    if args.command == "prompt-build":
        return _cmd_prompt_build(args)
    if args.command == "recommend":
        return _cmd_recommend(args)
    if args.command == "recommend-run":
        return _cmd_recommend_run(args)

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
