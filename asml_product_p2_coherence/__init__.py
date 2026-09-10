"""asml_product_p2_coherence — champion-facing illuminator conditioner (M1).

Research pods import this package. Harness hill-climbs only touch
``asml-bench/labs/fel-02-coherence/conditioner.py``; set ``ASML_BENCH_ROOT``
(or ``ASML_P2_CONDITIONER_PATH``) to pick up live weights, else the bundled
reference conditioner is used.
"""

from .condition import (
    ASSUMPTION_CARD,
    CARD_IF_LOSS_DB,
    CARD_PUPIL_FILL_TARGET,
    CARD_SPATIAL_SIGMA,
    ConditionerReport,
    condition,
    condition_metrics,
)

__all__ = [
    "ASSUMPTION_CARD",
    "CARD_IF_LOSS_DB",
    "CARD_PUPIL_FILL_TARGET",
    "CARD_SPATIAL_SIGMA",
    "ConditionerReport",
    "condition",
    "condition_metrics",
]

__version__ = "0.1.0"
