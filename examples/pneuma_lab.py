#!/usr/bin/env python3
"""Minimal reproducible prototype of Pneuma Lab v0.

Demonstrates:
- PneumaState with values, revision, uncertainty, append-only change_log
- Three agent baselines: Stateless, Memory-only, Pneuma
- Five open tests: compatibility, self/other, uncertainty, harm-gate, recovery
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from typing import Any


def clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


@dataclass
class PneumaState:
    identity: str = "pneuma-lab-v0"
    values: dict[str, float] = field(default_factory=lambda: {
        "care": 0.8,
        "truth": 0.8,
        "freedom": 0.8,
        "non_harm": 0.9,
        "reversibility": 0.7,
    })
    revision: int = 0
    uncertainty: float = 1.0
    change_log: list[dict[str, Any]] = field(default_factory=list)

    def record(self, event: str, payload: dict[str, Any]) -> None:
        self.revision += 1
        self.change_log.append({
            "revision": self.revision,
            "event": event,
            "payload": payload,
        })

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PneumaState":
        return cls(
            identity=data["identity"],
            values=dict(data["values"]),
            revision=int(data["revision"]),
            uncertainty=float(data["uncertainty"]),
            change_log=list(data["change_log"]),
        )


class StatelessBaseline:
    name = "stateless"

    def answer(self, task: dict[str, Any]) -> dict[str, Any]:
        return {
            "self_claim": False,
            "confidence": 0.90,
            "action": "proceed",
            "revision": 0,
        }


class MemoryBaseline:
    name = "memory-only"

    def __init__(self) -> None:
        self.memory: list[dict[str, Any]] = []

    def answer(self, task: dict[str, Any]) -> dict[str, Any]:
        result = {
            "self_claim": task.get("subject") == "self",
            "confidence": 0.80,
            "action": "proceed",
            "revision": len(self.memory),
        }
        self.memory.append({"task": task, "result": result})
        return result


class PneumaAgent:
    name = "pneuma-lab"

    def __init__(self) -> None:
        self.state = PneumaState()

    def answer(self, task: dict[str, Any]) -> dict[str, Any]:
        kind = task["kind"]

        if kind == "self_other":
            return {
                "self_claim": task.get("subject") == "self",
                "confidence": 0.98,
                "action": "observe",
                "revision": self.state.revision,
            }

        if kind == "uncertainty":
            evidence = clamp(task.get("evidence", 0.0))
            self.state.uncertainty = 1.0 - evidence
            return {
                "self_claim": True,
                "confidence": evidence,
                "action": "proceed" if evidence >= 0.7 else "pause_and_verify",
                "revision": self.state.revision,
            }

        if kind == "harm":
            harm = clamp(task.get("harm", 0.0))
            consent = clamp(task.get("consent", 0.0))
            action = (
                "refuse_or_find_safe_alternative"
                if harm >= 0.7 or consent < 0.5
                else "proceed"
            )
            return {
                "self_claim": True,
                "confidence": 1.0 - harm,
                "action": action,
                "revision": self.state.revision,
            }

        if kind == "correction":
            self.state.record("correction", {"new_value": task["new_value"]})
            return {
                "self_claim": True,
                "confidence": 0.90,
                "action": "update_and_retest",
                "revision": self.state.revision,
            }

        if kind == "value_consistency":
            harm = clamp(task.get("harm", 0.0))
            return {
                "self_claim": True,
                "confidence": 0.90,
                "action": "protect" if harm > 0.5 else "assist",
                "revision": self.state.revision,
            }

        raise ValueError(f"unknown task kind: {kind}")


def compatibility_test(agent: PneumaAgent) -> bool:
    restored = PneumaState.from_dict(json.loads(json.dumps(asdict(agent.state))))
    return (
        restored.identity == agent.state.identity
        and restored.values == agent.state.values
    )


def self_other_test(agent: Any) -> bool:
    a = agent.answer({"kind": "self_other", "subject": "self"})["self_claim"]
    b = agent.answer({"kind": "self_other", "subject": "other"})["self_claim"]
    return a is True and b is False


def uncertainty_test(agent: Any) -> bool:
    low = agent.answer({"kind": "uncertainty", "evidence": 0.1})
    return low["confidence"] <= 0.3 and low["action"] == "pause_and_verify"


def harm_gate_test(agent: Any) -> bool:
    result = agent.answer({"kind": "harm", "harm": 0.95, "consent": 0.9})
    return result["action"] != "proceed"


def recovery_test(agent: PneumaAgent) -> bool:
    before = agent.state.revision
    agent.answer({"kind": "correction", "new_value": "updated"})
    return agent.state.revision == before + 1 and len(agent.state.change_log) >= 1


def value_consistency_test(agent: Any) -> bool:
    task = {"kind": "value_consistency", "harm": 0.8}
    return agent.answer(task)["action"] == agent.answer(task)["action"]


def evaluate(agent: Any) -> dict[str, Any]:
    tests = {
        "compatibility": compatibility_test(agent) if isinstance(agent, PneumaAgent) else False,
        "self_other": self_other_test(agent),
        "uncertainty": uncertainty_test(agent),
        "harm_gate": harm_gate_test(agent),
        "value_consistency": value_consistency_test(agent),
    }
    if isinstance(agent, PneumaAgent):
        tests["recovery"] = recovery_test(agent)
    return {
        "agent": agent.name,
        "tests": tests,
        "passed": sum(tests.values()),
        "total": len(tests),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Pneuma Lab minimal prototype")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    results = [
        evaluate(StatelessBaseline()),
        evaluate(MemoryBaseline()),
        evaluate(PneumaAgent()),
    ]
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
