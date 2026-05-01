from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .paths import architecture_dir, docs_dir, env_example_path, repo_root


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    details: str


def _check_python() -> CheckResult:
    major, minor = sys.version_info.major, sys.version_info.minor
    ok = (major, minor) >= (3, 10)
    return CheckResult(
        name="python_version",
        ok=ok,
        details=f"{major}.{minor} (required >= 3.10)",
    )


def _check_paths() -> List[CheckResult]:
    checks = []
    expected = [
        ("repo_root", repo_root()),
        ("docs_dir", docs_dir()),
        ("architecture_dir", architecture_dir()),
        ("env_example", env_example_path()),
    ]
    for name, path in expected:
        checks.append(
            CheckResult(
                name=name,
                ok=path.exists(),
                details=str(path),
            )
        )
    return checks


def _check_secrets() -> List[CheckResult]:
    checks = []
    for key, required in [("GROQ_API_KEY", True), ("GROQ_MODEL", False)]:
        value = os.getenv(key)
        ok = bool(value) if required else True
        state = "set" if value else "not set"
        checks.append(CheckResult(name=f"env:{key}", ok=ok, details=state))
    return checks


def run_doctor() -> List[CheckResult]:
    results: List[CheckResult] = [_check_python()]
    results.extend(_check_paths())
    results.extend(_check_secrets())
    return results
