"""Champion-facing condition API: metrics + synthetic uncertainty.

Uncertainty is a **toy / documented** model. Numbers are synthetic; they are
not confidential fab data.

IF Spec product floor (triple KEEP only):
  speckle < 0.15
  pupil_fill_error ≤ 0.10  (etendue proxy under current toys)
  photons_kept ≥ 0.55

``if_loss_db`` is report-only for P10 IF-shim handoff — not a fourth KEEP AND.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .loader import get_conditioner

ASSUMPTION_CARD = "coherence-if-v1"
CARD_PUPIL_FILL_TARGET = 0.72
CARD_SPATIAL_SIGMA = 0.15
CARD_IF_LOSS_DB = 0.8

# Synthetic uncertainty model (documented, not fab-grounded).
_CARD_CONFIDENCE = 0.65  # coherence-if-v1 med confidence (synthetic)
_REL_SIGMA = {
    "speckle": 0.06,
    "pupil_fill_error": 0.05,
    "photons_kept": 0.02,
    "if_loss_db": 0.05,
}
_FLOOR_SIGMA = {
    "speckle": 0.002,
    "pupil_fill_error": 0.002,
    "photons_kept": 0.005,
    "if_loss_db": 0.02,
}

_REQUIRED_KEYS = ("coherence",)


@dataclass
class ConditionerReport:
    """Product report returned by :func:`condition`."""

    speckle: float
    pupil_fill_error: float
    photons_kept: float
    if_loss_db: float
    uncertainty: dict[str, float]
    assumption_card_id: str = ASSUMPTION_CARD
    etendue_proxy: str = (
        "pupil_fill_error (cite pupil_fill_target=0.72 + spatial_sigma=0.15)"
    )
    conditioner_source: str = "reference"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _uncertainty_for(metrics: Mapping[str, float]) -> dict[str, float]:
    """Toy σ: max(floor, |value| * rel * (1.25 - confidence)). Synthetic."""
    scale = 1.25 - _CARD_CONFIDENCE
    out: dict[str, float] = {}
    for key, value in metrics.items():
        rel = _REL_SIGMA.get(key, 0.05)
        floor = _FLOOR_SIGMA.get(key, 1e-3)
        out[key] = float(max(floor, abs(float(value)) * rel * scale))
    return out


def condition_metrics(row: Mapping[str, Any]) -> dict[str, float]:
    """Point estimates only (no uncertainty envelope)."""
    for key in _REQUIRED_KEYS:
        if key not in row:
            raise KeyError(f"missing required field: {key}")
    payload = dict(row)
    _source, fn = get_conditioner()
    raw = fn(payload)
    return {
        "speckle": float(raw["speckle"]),
        "pupil_fill_error": float(raw["pupil_fill_error"]),
        "photons_kept": float(raw["photons_kept"]),
        "if_loss_db": float(CARD_IF_LOSS_DB),
    }


def condition(row: Mapping[str, Any]) -> ConditionerReport:
    """Run the conditioner and attach synthetic per-metric uncertainty."""
    for key in _REQUIRED_KEYS:
        if key not in row:
            raise KeyError(f"missing required field: {key}")
    payload = dict(row)
    source, fn = get_conditioner()
    raw = fn(payload)
    metrics = {
        "speckle": float(raw["speckle"]),
        "pupil_fill_error": float(raw["pupil_fill_error"]),
        "photons_kept": float(raw["photons_kept"]),
        "if_loss_db": float(CARD_IF_LOSS_DB),
    }
    return ConditionerReport(
        speckle=metrics["speckle"],
        pupil_fill_error=metrics["pupil_fill_error"],
        photons_kept=metrics["photons_kept"],
        if_loss_db=metrics["if_loss_db"],
        uncertainty=_uncertainty_for(metrics),
        assumption_card_id=ASSUMPTION_CARD,
        conditioner_source=source,
    )
