# SPEC — asml-product-p2-coherence (M1 champion module)

## Champion job

Given a synthetic illumination / coherence field row, research pods **import**
this package and obtain conditioner metrics plus a documented uncertainty
envelope:

| Metric | Role | KEEP? |
|--------|------|-------|
| `speckle` | Speckle contrast (lower is better) | **yes** `< 0.15` |
| `pupil_fill_error` | Error vs fill target; **etendue proxy** under current toys | **yes** `≤ 0.10` |
| `photons_kept` | Photon / power budget retained (discard → VOID) | **yes** `≥ 0.55` |
| `if_loss_db` | IF insertion-loss report for P10 shim handoff (card `0.8` dB) | **report only** — not a fourth KEEP AND |

Assumption card: **`coherence-if-v1`** (`pupil_fill_target=0.72`, `spatial_sigma=0.15`, `if_loss_db=0.8`).

**No fourth KEEP AND for MVP.** Do not invent etendue/pol/envelope/pointing KEEP
metrics without fixtures. Claiming “etendue KEEP” without the pupil gate is illegal —
`pupil_fill_error` *is* the etendue proxy (cite `pupil_fill_target` + `spatial_sigma`).
Do not drop `if_loss_db` below the card value without a new IF Spec stamp.

Public surface (M1 target):

```python
from asml_product_p2_coherence import condition, ConditionerReport

report = condition({
  # synthetic illumination field features (bench fixture keys)
  "coherence": ...,
  "pupil_fill_error": ...,
  "photons": ...,
  # optional: "bandwidth", ...
})
# report.speckle, .pupil_fill_error, .photons_kept
# report.if_loss_db          # card-aligned report for P10; not a KEEP AND
# report.uncertainty         # per-metric σ (synthetic, documented)
# report.assumption_card_id == "coherence-if-v1"
# report.etendue_proxy       # documents pupil_fill_error as etendue proxy
# report.to_dict()
```

Also: `condition_metrics(row) -> dict` — point estimates only.

## Sandbox contract

- Bench lab: `asml-bench/labs/fel-02-coherence/`
- **Harness may edit only** `labs/fel-02-coherence/conditioner.py`
- This product package is the **stable import surface**. Bundled
  `reference_conditioner.py` (when implemented) matches the SEED-class
  baseline so `pip install -e .` needs zero bench checkout.
- Live weights: set `ASML_BENCH_ROOT` (loads `labs/fel-02-coherence/conditioner.py`)
  or `ASML_P2_CONDITIONER_PATH` (path to a `conditioner.py`). Else → reference
  fallback.
- If those env vars change **mid-process**, call
  `get_conditioner(force_reload=True)` (or `reset_loader_cache()`) — the
  loader caches the first resolved predictor.
- Never invoke lasercode from this PI. Hill-climbs go through Foreman stamps.

## Frozen eval / IF Spec (pupil freeze)

Product claims bind to the **pupil-frozen** FEL-02 KEEP contract only
([asml-bench PR #40](https://github.com/gtmsko46-debug/asml-bench/pull/40)
@`84520ee`):

| Gate | Metric | KEEP threshold |
|------|--------|----------------|
| Speckle | holdout mean `speckle` | `< 0.15` |
| Photons | holdout mean `photons_kept` | `≥ 0.55` |
| **Pupil** | holdout mean `pupil_fill_error` | **`≤ 0.10`** (`PUPIL_ERR_MAX`) |

Ticket guard string: `if_spec_pupil_err_max=0.10`  
(IF Spec stamp: `tickets/IF_SPEC_PUPIL_BOUND.md` on asml-bench).

**Research KEEP ≠ product KEEP.** Citing the research dual-KEEP feed is allowed;
shipping product KEEP language requires P2 frozen eval + sandbox + champion job
+ Critic + Eval Integrity before promote.

## IF Spec product floor

Triple gate above is the **product KEEP floor** (same as FEL-02 PR #40). Extra fields:

| Topic | Rule |
|-------|------|
| Etendue | Product name owns it; under current toys `pupil_fill_error` **is** the etendue proxy |
| `if_loss_db` | Report in product outputs for P10 IF-shim handoff; `photons_kept` remains the hard power/cheat gate |
| Polarization | **Out of scope** → P4 / FEL-04 (deferred, not waived) |
| Pulse envelope | **Out of scope** → P5 / FEL-05 |
| Pointing / power-stability-over-time | **Out of scope** → P8 / FEL-06 |

Package must not claim deferred fields. Product KEEP still requires frozen eval +
sandbox + champion-facing job on this repo (research Dual-KEEP ≠ product KEEP).

## Research feed (cite only)

Dual-KEEP stamped under `coherence-if-v1` (Critic + Repro + Diplomat; EI pupil freeze):

| Ticket | Provider | speckle | pupil_err | photons_kept |
|--------|----------|---------|-----------|--------------|
| HT-1011 | `grok` | 0.0413 | 0.0096 | 1.0 |
| HT-1022 | `mock-mistral` | 0.1017 | 0.0475 | 1.0 |

Do **not** treat these rows as product KEEP / ship-queue language.

## Product dual-gate tickets (queued)

| Ticket | Provider | Status |
|--------|----------|--------|
| HT-1023 | `grok` | drafted; **bay queued behind P1 HT-1015 KEEP_PENDING_DUAL + HT-1025** |
| HT-1024 | `mock-mistral` | drafted; dual pair to HT-1023; same bay queue |

- `lab_path`: `labs/fel-02-coherence`
- `sandbox`: `conditioner.py`
- Parent backlog: [asml-bench #3](https://github.com/gtmsko46-debug/asml-bench/issues/3)

**Bay priority:** P1 Twin stays P0. Current blockers: **HT-1015** `KEEP_PENDING_DUAL` + **HT-1025** independent mock-mistral (HT-1020 was Critic VOID — not the bay owner). Heavy Operator ratchets for HT-1023/1024 wait until CoS frees the bay after 1025 honest dual + Critic/Repro — Spec/Issues may advance now (Lab Director funded); do not steal Operator from P1.

## Provider / dual-island

| Lane | Provider tag | Notes |
|------|--------------|-------|
| STEM / conditioner solvers | `grok` | Primary climb island |
| Docs / scaffold / weak island | `mock-mistral` | Prefer this tag — do **not** stamp `mistral/*` |

Research-facing demos require **dual-island**. Foreman owns lasercode-session
routing. Critic + Eval Integrity before any product KEEP promote.
No vs-LPP framing / no upstairs champion language.

## Factory milestones (asml-bench issues)

| M / path | Issue | Stage | Status |
|----------|-------|-------|--------|
| Parent | [#3](https://github.com/gtmsko46-debug/asml-bench/issues/3) | backlog → build | Lab Director APPROVE |
| M0 | [#41](https://github.com/gtmsko46-debug/asml-bench/issues/41) | Bind to pupil-frozen eval | **spec** |
| M1 | [#42](https://github.com/gtmsko46-debug/asml-bench/issues/42) | Champion importable module | **package skeleton** |
| Dual-gate RUN | [#43](https://github.com/gtmsko46-debug/asml-bench/issues/43) | HT-1023 ∧ HT-1024 | queued behind HT-1015 KEEP_PENDING_DUAL + HT-1025 |

## Uncertainty model (synthetic)

`condition` attaches per-metric σ from a **toy** envelope scaled by
assumption-card confidence (`coherence-if-v1`). These are **not** fab
ground-truth; never invent confidential numbers.

## Package layout (target)

```
asml_product_p2_coherence/
  __init__.py               # condition, ConditionerReport, ASSUMPTION_CARD
  reference_conditioner.py  # bundled SEED-class baseline (when implemented)
  loader.py                 # ASML_BENCH_ROOT / ASML_P2_CONDITIONER_PATH
  condition.py              # ConditionerReport + uncertainty wrapper
```

M1 package skeleton ships SEED-class `reference_conditioner` (importable now).
Live KEEP weight sync + hill-climb wait for Foreman bay after P1 HT-1015
KEEP_PENDING_DUAL + HT-1025 clear — lasercode under stamped tickets only.
