# asml-product-p2-coherence

**P2 product.** Illuminator-near coherence / etendue conditioner that research
pods can import — not a lab-only sandbox. M1 ships the installable module `asml_product_p2_coherence` (SEED-class
`reference_conditioner`; live KEEP weights via env after Foreman climbs).

## Status

- Lab Director **APPROVE** product sync from Diplomat **DUAL-KEEP HT-1023 ∧ HT-1034**
- Bundled `reference_conditioner` = **HT-1023** (speckle=0.1221 / pupil_err=0.0209 / photons=1.0)
- Dual partner **HT-1034** (speckle=0.1220 / pupil_err=0.0350 / photons=1.0) Critic+Repro PASS
- HOLDOUT digest `3ed24ec5df80e01a133de535e5d8df0c9ce4f9f10493538f24c2d87c359596f8`
- **SOFT NOTES (travel):** HT-1034 carries soft `speckle *120`-class scale and `fill = 1 − pfe` identity (HT-1022-class soft) — disclosed here, not hidden
- Not vs-LPP; no champion brief; PR for merge review (not auto-merge)
- Spec: [SPEC.md](./SPEC.md) · Lab notes: [LAB.md](./LAB.md)


## Install

```bash
git clone https://github.com/gtmsko46-debug/asml-product-p2-coherence
cd asml-product-p2-coherence
pip install -e .
```

Zero bench checkout required. Bundled `reference_conditioner` = **HT-1023** dual-KEEP (not SEED). Live weights:

```bash
export ASML_BENCH_ROOT=/path/to/asml-bench
# or: export ASML_P2_CONDITIONER_PATH=/path/to/labs/fel-02-coherence/conditioner.py
```

Harness edits **only** bench `conditioner.py`. This package is the stable
import surface.

## Import (champion API — M1 target)

```python
from asml_product_p2_coherence import condition, ConditionerReport

report = condition({
    "coherence": 0.6,
    "pupil_fill_error": 0.25,
    "photons": 1.0,
    "bandwidth": 0.001,
})

print(report.speckle, report.pupil_fill_error, report.photons_kept)
print(report.if_loss_db)       # P10 handoff report; not a KEEP AND
print(report.uncertainty)      # per-metric σ (synthetic, documented)
assert report.assumption_card_id == "coherence-if-v1"
print(report.to_dict())
```

Point estimates only: `from asml_product_p2_coherence import condition_metrics`.

Smoke: `python examples/smoke_import.py` · tests: `pip install -e '.[dev]' && pytest`

## Champion job

Synthetic illumination field → conditioner metrics under assumption card
`coherence-if-v1` (`pupil_fill_target=0.72`).

KEEP contract (pupil-frozen; IF Spec product floor):

| Gate | Threshold | Notes |
|------|-----------|-------|
| `speckle` | `< 0.15` | KEEP AND |
| `pupil_fill_error` | `≤ 0.10` | KEEP AND — **etendue proxy** (`pupil_fill_target` + `spatial_sigma`) |
| `photons_kept` | `≥ 0.55` | KEEP AND — hard power/cheat gate |
| `if_loss_db` | card `0.8` dB | **report only** for P10 handoff — not a fourth KEEP AND |

No pol / pulse-envelope / pointing claims (deferred to P4/P5/P8).  
Uncertainty is a documented toy envelope — **synthetic**, not confidential fab data.

## Bench / sandbox

| | |
|--|--|
| Lab | `labs/fel-02-coherence/` on [asml-bench](https://github.com/gtmsko46-debug/asml-bench) |
| Sandbox (harness-only) | `conditioner.py` |
| Assumption card | `coherence-if-v1` |
| Spec | [SPEC.md](./SPEC.md) |

## Research feed (cite only — not product KEEP)

| Ticket | Provider | speckle / pupil_err / photons |
|--------|----------|-------------------------------|
| HT-1011 | `grok` | 0.0413 / 0.0096 / 1.0 |
| HT-1022 | `mock-mistral` | 0.1017 / 0.0475 / 1.0 |

## Factory milestones

| M / path | Issue | Stage | Status |
|----------|-------|-------|--------|
| Parent | [#3](https://github.com/gtmsko46-debug/asml-bench/issues/3) | build | Lab Director APPROVE |
| M0 | [#41](https://github.com/gtmsko46-debug/asml-bench/issues/41) | Bind pupil-frozen eval | spec |
| M1 | [#42](https://github.com/gtmsko46-debug/asml-bench/issues/42) | Champion importable module | **package skeleton (this PR)** |
| Dual-gate RUN | [#43](https://github.com/gtmsko46-debug/asml-bench/issues/43) | HT-1023 ∧ HT-1034 | **shipped** dual-KEEP 1023∧1034 |

## Provider / dual-island

| Lane | Provider tag |
|------|--------------|
| STEM / conditioner solvers | `grok` |
| Docs / scaffold / weak island | `mock-mistral` |

Never invoke lasercode from this PI; Foreman owns harness stamps.
Critic + Eval Integrity before any product KEEP promote.
