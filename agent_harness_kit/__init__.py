"""Agent Harness Kit command-line package."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def package_version() -> str:
    try:
        return version("agent-harness-kit-cli")
    except PackageNotFoundError:
        return (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()


__version__ = package_version()
