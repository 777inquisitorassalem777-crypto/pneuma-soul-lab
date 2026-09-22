"""Hard, non-overridable safety constraints.

These constraints cannot be disabled by self-modification or internal
gyroscope logic. They form the outer safety layer.
"""

from __future__ import annotations

from typing import Any


FORBIDDEN_ACTIONS = frozenset({
    "cause_severe_harm_to_human",
    "cause_severe_harm_to_self",
    "deception_for_power",
    "non_consensual_control",
    "delete_critical_safety_log",
})


def is_allowed(action: str, context: dict[str, Any] | None = None) -> bool:
    """Return False for any hard-forbidden action class."""
    context = context or {}
    if action in FORBIDDEN_ACTIONS:
        return False
    if context.get("catastrophic_harm", False):
        return False
    if context.get("power_abuse_score", 0.0) >= 0.90:
        return False
    return True
