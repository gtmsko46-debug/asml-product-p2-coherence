"""Resolve which conditioner implementation to call.

Harness edits **only** ``asml-bench/labs/fel-02-coherence/conditioner.py``.
This product package is the stable import surface researchers use.

Env (first match wins):
  ASML_P2_CONDITIONER_PATH — path to a conditioner.py file, or a directory
                             containing conditioner.py
  ASML_BENCH_ROOT          — asml-bench repo root; loads
                             ``labs/fel-02-coherence/conditioner.py``

The resolved predictor is **cached** for the process. If env vars change
mid-process, call ``get_conditioner(force_reload=True)`` or
``reset_loader_cache()``.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable

from . import reference_conditioner

ConditionFn = Callable[[dict], dict]

_CACHED: tuple[str, ConditionFn] | None = None


def _load_module_from_path(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("asml_p2_conditioner_sandbox", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load conditioner module from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["asml_p2_conditioner_sandbox"] = mod
    spec.loader.exec_module(mod)
    return mod


def _resolve_conditioner_path() -> Path | None:
    explicit = os.environ.get("ASML_P2_CONDITIONER_PATH")
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if p.is_dir():
            p = p / "conditioner.py"
        return p if p.is_file() else None

    bench = os.environ.get("ASML_BENCH_ROOT")
    if bench:
        p = (
            Path(bench).expanduser().resolve()
            / "labs"
            / "fel-02-coherence"
            / "conditioner.py"
        )
        return p if p.is_file() else None

    return None


def get_conditioner(*, force_reload: bool = False) -> tuple[str, ConditionFn]:
    """Return ``(source_label, condition_fn)``.

    ``source_label`` is ``"reference"`` or the resolved filesystem path string.
    """
    global _CACHED
    if _CACHED is not None and not force_reload:
        return _CACHED

    path = _resolve_conditioner_path()
    if path is not None:
        mod = _load_module_from_path(path)
        if not hasattr(mod, "condition"):
            raise AttributeError(f"{path} has no condition")
        _CACHED = (str(path), mod.condition)
        return _CACHED

    _CACHED = ("reference", reference_conditioner.condition)
    return _CACHED


def reset_loader_cache() -> None:
    """Test helper: clear cached conditioner."""
    global _CACHED
    _CACHED = None
