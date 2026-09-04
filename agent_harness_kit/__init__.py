"""Agent Harness Kit command-line package."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def package_version() -> str:
    source = Path(__file__).resolve()
    portable_candidates = [parent.parent / "VERSION" for parent in source.parents if parent.suffix == ".pyz"]
    for candidate in portable_candidates:
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8").strip()
    try:
        return version("agent-harness-kit-cli")
    except PackageNotFoundError:
        candidates = [source.parents[1] / "VERSION"]
        for candidate in candidates:
            if candidate.is_file():
                return candidate.read_text(encoding="utf-8").strip()
        return "0+portable"


__version__ = package_version()
