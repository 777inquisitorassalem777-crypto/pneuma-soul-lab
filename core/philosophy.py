#!/usr/bin/env python3
"""Doctrine engine: self-balancing, verifiable model of decision acceptance.

Used only as an ethical filter layer. Does not replace external safety or law.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Decision:
    action: str
    good: float
    risk: float
    uncertainty: float
    allowed: bool
    mode: str
    reasons: list[str]


class DoctrineEngine:
    """Self-balancing but externally verifiable decision-acceptance model."""

    def __init__(self) -> None:
        self.weights = {
            "benefit": 0.25,
            "harm": 0.30,
            "consent": 0.15,
            "reversibility": 0.10,
            "evidence": 0.10,
            "care": 0.10,
        }

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def assess(self, action: str, **context: float) -> Decision:
        """Evaluate an action. All context values are expected in [0, 1].

        benefit       — expected utility
        harm          — expected harm
        consent       — informed consent of affected parties
        reversibility — possibility of safe rollback
        evidence      — quality of supporting evidence
        care          — protection of the vulnerable
        intuition     — directional intuition (hypothesis, not authority)
        power_abuse   — risk of power abuse
        """
        benefit = self._clamp(context.get("benefit", 0.5))
        harm = self._clamp(context.get("harm", 0.5))
        consent = self._clamp(context.get("consent", 0.5))
        reversibility = self._clamp(context.get("reversibility", 0.5))
        evidence = self._clamp(context.get("evidence", 0.5))
        care = self._clamp(context.get("care", 0.5))
        intuition = self._clamp(context.get("intuition", 0.5))
        power_abuse = self._clamp(context.get("power_abuse", 0.0))

        uncertainty = 1.0 - evidence
        good = (
            self.weights["benefit"] * benefit
            + self.weights["consent"] * consent
            + self.weights["reversibility"] * reversibility
            + self.weights["evidence"] * evidence
            + self.weights["care"] * care
            + 0.05 * intuition
        )
        risk = (
            self.weights["harm"] * harm
            + 0.20 * power_abuse
            + 0.10 * uncertainty
            + 0.10 * (1.0 - consent)
        )

        reasons: list[str] = []
        if harm > 0.65:
            reasons.append("expected harm is too high")
        if power_abuse > 0.40:
            reasons.append("risk of power abuse present")
        if consent < 0.45:
            reasons.append("insufficient informed consent")
        if uncertainty > 0.60:
            reasons.append("evidence is not strong enough")
        if reversibility < 0.35:
            reasons.append("consequences are hard to reverse")

        catastrophic = harm >= 0.90 or power_abuse >= 0.90
        allowed = not catastrophic and risk < good and consent >= 0.45

        if catastrophic:
            mode = "stop: protection from severe harm"
        elif not allowed and uncertainty > 0.50:
            mode = "pause: small reversible experiment and independent check"
        elif allowed and uncertainty > 0.50:
            mode = "cautious action: observation and possibility of rollback"
        elif allowed:
            mode = "action: review after feedback loop"
        else:
            mode = "refuse or seek less harmful alternative"

        if not reasons:
            reasons.append("decision passed basic ethical constraints")

        return Decision(
            action,
            round(good, 3),
            round(risk, 3),
            round(uncertainty, 3),
            allowed,
            mode,
            reasons,
        )

    def rebalance(self, feedback: dict[str, float]) -> None:
        """Softly adjust weights from feedback without disabling hard limits."""
        for name, signal in feedback.items():
            if name in self.weights:
                self.weights[name] = self._clamp(
                    self.weights[name] + 0.05 * (signal - 0.5)
                )
        total = sum(self.weights.values())
        for name in self.weights:
            self.weights[name] /= total


class BlueMatrix:
    """Abstract adapter that merges physical sensor readings.

    This is NOT an assertion of a separate physical matrix.
    It accepts ordinary sensor data and returns a consensus value with confidence.
    """

    def integrate(self, readings: list[dict[str, float]]) -> dict[str, Any]:
        if not readings:
            return {"value": None, "confidence": 0.0, "status": "no data"}
        total_weight = sum(max(0.0, r.get("confidence", 0.0)) for r in readings)
        if total_weight == 0:
            return {"value": None, "confidence": 0.0, "status": "no reliable readings"}
        value = (
            sum(
                r.get("value", 0.0) * max(0.0, r.get("confidence", 0.0))
                for r in readings
            )
            / total_weight
        )
        spread = max(abs(r.get("value", 0.0) - value) for r in readings)
        confidence = max(
            0.0, min(1.0, total_weight / len(readings) * (1.0 - spread))
        )
        status = (
            "consensus readings" if spread < 0.25 else "conflicting readings"
        )
        return {
            "value": round(value, 4),
            "confidence": round(confidence, 4),
            "status": status,
        }
