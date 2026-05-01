from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """Return repository root based on package location."""
    return Path(__file__).resolve().parents[3]


def docs_dir() -> Path:
    return repo_root() / "docs"


def architecture_dir() -> Path:
    return docs_dir() / "architecture"


def env_example_path() -> Path:
    return repo_root() / ".env.example"
