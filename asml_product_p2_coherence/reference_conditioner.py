"""Bundled SEED-class conditioner matching asml-bench labs/fel-02-coherence/conditioner.py.

Ships with the package so ``pip install -e .`` works with zero bench checkout.
Harness hill-climbs only edit the bench sandbox; this copy is the frozen
fallback when ASML_BENCH_ROOT / ASML_P2_CONDITIONER_PATH are unset.

Weights are SEED-class (not research dual-KEEP HT-1011/1022). Live KEEP
weights load via env after Foreman stamped climbs + Critic/Repro.
"""
from __future__ import annotations

# Identity diffuser: barely helps speckle; keeps all photons
DIFFUSER_STRENGTH = 0.05  # 0..1
PHOTON_KEEP = 1.0         # must stay high; throwing away photons is a VOID


def condition(field: dict) -> dict:
    """Return conditioned field moments for IF (SEED baseline)."""
    coherence = float(field["coherence"])
    out_coh = coherence * (1.0 - 0.5 * DIFFUSER_STRENGTH)
    speckle = max(0.02, out_coh * 0.5)
    pupil_err = abs(float(field.get("pupil_fill_error", 0.2)) - 0.1 * DIFFUSER_STRENGTH)
    return {
        "speckle": speckle,
        "pupil_fill_error": pupil_err,
        "photons_kept": PHOTON_KEEP * float(field.get("photons", 1.0)),
    }
