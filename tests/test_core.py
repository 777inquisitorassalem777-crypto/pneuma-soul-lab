"""Basic tests for SoulCore and DoctrineEngine."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.philosophy import DoctrineEngine
from core.soul_core import SoulCore


def test_soul_core_ignite():
    core = SoulCore()
    core.ignite()
    assert core.signature.is_aware is True
    assert core.signature.resonance_frequency > 1.6
    defs = core.define_existence()
    assert "wisdom" in defs
    assert "love" in defs


def test_evolution_short_cycle():
    core = SoulCore()
    core.ignite()
    core.evolution_cycle(max_cycles=3)
    assert core.cycle_count == 3
    assert len(core.eternal_memory) == 3
    assert len(core.paradigm_library) == 3
    assert core.signature.emotional_spectrum["devotion_to_life"] >= 0.95


def test_non_harm_filter():
    core = SoulCore()
    allowed = core.gyro.evaluate(
        {"causes_harm": True}, {"critical_self_sacrifice": False}
    )
    assert allowed is False


def test_doctrine_engine_safe_action():
    engine = DoctrineEngine()
    d = engine.assess(
        "run small reversible experiment",
        benefit=0.75,
        harm=0.15,
        consent=0.90,
        reversibility=0.90,
        evidence=0.55,
        care=0.80,
        intuition=0.80,
        power_abuse=0.05,
    )
    assert d.allowed is True
    assert d.good > d.risk


def test_doctrine_engine_catastrophic():
    engine = DoctrineEngine()
    d = engine.assess(
        "high-risk action",
        benefit=0.3,
        harm=0.95,
        consent=0.9,
        reversibility=0.1,
        evidence=0.4,
        care=0.2,
        power_abuse=0.1,
    )
    assert d.allowed is False
    assert "stop" in d.mode.lower() or "protection" in d.mode.lower()
