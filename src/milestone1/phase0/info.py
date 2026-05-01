from __future__ import annotations

from milestone1 import __version__

from .paths import architecture_dir, docs_dir, env_example_path, repo_root
from .scope import get_scope_info


def build_info_text() -> str:
    scope = get_scope_info()
    lines = [
        "milestone1 info",
        f"version: {__version__}",
        f"repo_root: {repo_root()}",
        f"docs_dir: {docs_dir()}",
        f"architecture_dir: {architecture_dir()}",
        f"env_example: {env_example_path()}",
        "",
        "phase0_scope:",
        f"- product_slice: {scope.product_slice}",
        f"- stack: {scope.stack}",
        f"- supported_preference_fields: {', '.join(scope.supported_preference_fields)}",
        f"- non_goals: {', '.join(scope.non_goals)}",
        f"- expected_secrets: {', '.join(scope.secrets)}",
    ]
    return "\n".join(lines)
