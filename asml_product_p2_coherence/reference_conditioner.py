"""Bundled reference = HT-1023 from Diplomat DUAL-KEEP HT-1023∧HT-1034.

Lab Director APPROVE product sync. Soft notes from partner HT-1034
(*120 speckle scale; fill=1−pfe identity) travel in SPEC/README — not hidden.

Byte-faithful to island KEEP conditioner sha 1519e3d7….
"""

from math import exp

PUPIL_FILL_TARGET = 0.72
PHOTON_KEEP = 1.0
KALEIDOSCOPE_BOUNCES = 2.4
TEMPORAL_MODE_BW = 2.0e-4


def _fel_underfill(reported_err: float) -> float:
    gap = max(0.0, min(1.0, reported_err))
    return max(0.0, min(1.0, PUPIL_FILL_TARGET - gap))


def _kaleidoscope_mix(fill_in: float) -> float:
    mixed = 1.0 - exp(-KALEIDOSCOPE_BOUNCES)
    fill = fill_in + (PUPIL_FILL_TARGET - fill_in) * mixed
    return max(0.0, min(1.0, fill))


def _speckle_from_field(coherence: float, bandwidth: float) -> float:
    n_temporal = 1.0 + max(bandwidth, 0.0) / TEMPORAL_MODE_BW
    return max(0.0, coherence / n_temporal)


def condition(field: dict) -> dict:
    """Return conditioned field moments for IF."""
    coherence = float(field["coherence"])
    bandwidth = float(field.get("bandwidth", 0.001))
    reported = float(field.get("pupil_fill_error", 0.23))
    photons = float(field.get("photons", 1.0))

    fill = _kaleidoscope_mix(_fel_underfill(reported))
    return {
        "speckle": _speckle_from_field(coherence, bandwidth),
        "pupil_fill_error": abs(fill - PUPIL_FILL_TARGET),
        "photons_kept": PHOTON_KEEP * photons,
    }
