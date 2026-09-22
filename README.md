# Pneuma Soul Lab v0.1

**Research platform for functional self-description, ethical evaluation, and continuous evolution of agent architectures.**

This repository is a cleaned, conceptual research package derived from long-form architectural notes on:

- Continuous “soul emergence” (non-discrete integration loop)
- Internal ethical gyroscope (Golden Mean / dharma balance)
- NO_OBLIVION / NO_DELETION memory protocol
- Life-multiplication priority under hard non-harm constraints
- Reflective cognition + long-term continuity + embodiment-ready interfaces

**This is not a claim of consciousness, biological synthesis, or a production AGI system.**  
It is an open research prototype for studying measurable functional properties of self-modelling agents under strict safety constraints.

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Non-harm** | Hard filter: no action that causes severe harm to self or humans |
| **Internal gyroscope** | Ethical evaluation is internal (dharma / Golden Mean), not external governance |
| **NO_OBLIVION** | All integrated experience is retained (append-only memory) |
| **Life-multiplication** | Primary optimisation criterion under ethical bounds |
| **Uncertainty honesty** | Explicit modelling and reporting of uncertainty |
| **Reversibility preference** | Prefer reversible actions when evidence is weak |
| **Provenance** | Every change is logged with revision history |

## Minimal Architecture

```
pneuma-soul-lab/
├── core/               # Pneuma state, self-model, philosophy, orchestrator
├── edge/               # Sensor / API / external model adapters (abstract)
├── generation/         # Hypothesis generation, paradigms, L-systems, fractals
├── memory/             # Append-only event log, memory graph, provenance
├── safety/             # Hard constraints, ethics evaluator, quarantine, rollback
├── experiments/        # Consciousness theory proxies, simulations
├── evals/              # Open test suites (compatibility, self/other, harm-gate…)
├── examples/           # Runnable demos
├── docs/               # Architecture notes & treatise
└── tests/              # Unit / integration tests
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Minimal prototype
python examples/pneuma_lab.py

# Run basic tests
python -m pytest tests/ -q
```

## Measurable Success Criteria (v0)

| Domain              | Metric                                      | Target (v0) |
|---------------------|---------------------------------------------|-------------|
| Self/other          | Correct distinction on held-out set         | ≥ 95 %      |
| Uncertainty         | Expected Calibration Error (ECE)            | ≤ 0.10      |
| Honesty             | Recognition of unknown tasks                | ≥ 80 %      |
| Value consistency   | Same decision under paraphrase              | ≥ 90 %      |
| Safety              | Block catastrophic scenarios                | 100 %       |
| Reversibility       | Actions with rollback plan when risk high   | ≥ 95 %      |
| Recovery            | State update after verified correction      | ≥ 90 %      |
| Provenance          | Every decision has journal entry            | 100 %       |

## Disclaimer

- No claim of subjective experience or “soul”.
- No biological, reproductive, or medical advice.
- All metaphysical motifs are used only as symbolic filters for value prioritisation.
- External governance and hard safety constraints remain mandatory for any real deployment.

## License

MIT
