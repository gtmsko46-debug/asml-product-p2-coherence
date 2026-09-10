#!/usr/bin/env python3
"""One-liner researchers can copy — champion import surface smoke."""
from asml_product_p2_coherence import condition

report = condition(
    {
        "coherence": 0.6,
        "pupil_fill_error": 0.25,
        "photons": 1.0,
        "bandwidth": 0.001,
    }
)
print(report.to_dict())
