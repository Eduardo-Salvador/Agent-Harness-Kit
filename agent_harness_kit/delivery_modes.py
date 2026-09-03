"""Read-only delivery presets; selection never grants execution authority."""

from __future__ import annotations


PRESETS = ("accompanied", "autonomous", "hackathon")


def resolve_delivery_mode(preset: str = "accompanied") -> dict:
    """Describe a preset without changing project state or existing gates."""
    if preset not in PRESETS:
        raise ValueError(f"unknown delivery preset: {preset!r}")
    checkpoints = {
        "accompanied": ["first-usable-slice", "material-capabilities"],
        "autonomous": [],
        "hackathon": ["first-demo"],
    }
    return {
        "schema": "harness.delivery-mode/v1",
        "preset": preset,
        "mode": "hackathon" if preset == "hackathon" else "delivery",
        "interaction": "continuous" if preset == "autonomous" else "accompanied",
        "client_checkpoints": checkpoints[preset],
        "scope_policy": "timeboxed-demo" if preset == "hackathon" else "approved-envelope",
        "verification": "required",
        "parallelism": "host-capability",
        "learning_activation": "unchanged",
        "applies_changes": False,
    }
