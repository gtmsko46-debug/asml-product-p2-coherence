"""M1 contract tests for asml_product_p2_coherence."""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from asml_product_p2_coherence import (
    ASSUMPTION_CARD,
    CARD_IF_LOSS_DB,
    ConditionerReport,
    condition,
    condition_metrics,
)
from asml_product_p2_coherence.loader import get_conditioner, reset_loader_cache


SAMPLE = {
    "coherence": 0.6,
    "pupil_fill_error": 0.25,
    "photons": 1.0,
    "bandwidth": 0.001,
}


class TestCondition(unittest.TestCase):
    def setUp(self) -> None:
        reset_loader_cache()
        os.environ.pop("ASML_BENCH_ROOT", None)
        os.environ.pop("ASML_P2_CONDITIONER_PATH", None)

    def tearDown(self) -> None:
        reset_loader_cache()
        os.environ.pop("ASML_BENCH_ROOT", None)
        os.environ.pop("ASML_P2_CONDITIONER_PATH", None)

    def test_report_keys_and_card(self) -> None:
        report = condition(SAMPLE)
        self.assertIsInstance(report, ConditionerReport)
        self.assertEqual(report.assumption_card_id, "coherence-if-v1")
        self.assertEqual(report.assumption_card_id, ASSUMPTION_CARD)
        self.assertEqual(report.if_loss_db, CARD_IF_LOSS_DB)
        self.assertIn("pupil_fill_error", report.etendue_proxy)
        d = report.to_dict()
        for key in (
            "speckle",
            "pupil_fill_error",
            "photons_kept",
            "if_loss_db",
            "uncertainty",
            "assumption_card_id",
            "etendue_proxy",
            "conditioner_source",
        ):
            self.assertIn(key, d)

    def test_uncertainty_present(self) -> None:
        report = condition(SAMPLE)
        self.assertIsInstance(report.uncertainty, dict)
        for metric in ("speckle", "pupil_fill_error", "photons_kept", "if_loss_db"):
            self.assertIn(metric, report.uncertainty)
            self.assertGreater(report.uncertainty[metric], 0.0)

    def test_point_estimates(self) -> None:
        m = condition_metrics(SAMPLE)
        self.assertIn("speckle", m)
        self.assertEqual(m["if_loss_db"], CARD_IF_LOSS_DB)

    def test_loader_fallback_reference(self) -> None:
        source, fn = get_conditioner(force_reload=True)
        self.assertEqual(source, "reference")
        out = fn(SAMPLE)
        self.assertIn("speckle", out)
        report = condition(SAMPLE)
        self.assertEqual(report.conditioner_source, "reference")

    def test_loader_bench_path(self) -> None:
        bench = Path("/workspace/asml-bench/labs/fel-02-coherence/conditioner.py")
        if bench.is_file():
            with mock.patch.dict(os.environ, {"ASML_BENCH_ROOT": "/workspace/asml-bench"}):
                reset_loader_cache()
                source, fn = get_conditioner(force_reload=True)
                self.assertTrue(source.endswith("conditioner.py"))
                out = fn(SAMPLE)
                self.assertIn("speckle", out)
        else:
            with tempfile.TemporaryDirectory() as td:
                path = Path(td) / "conditioner.py"
                path.write_text(
                    "def condition(field):\n"
                    "    return {'speckle': 0.1, 'pupil_fill_error': 0.05, "
                    "'photons_kept': 1.0}\n",
                    encoding="utf-8",
                )
                with mock.patch.dict(os.environ, {"ASML_P2_CONDITIONER_PATH": str(path)}):
                    reset_loader_cache()
                    source, fn = get_conditioner(force_reload=True)
                    self.assertEqual(source, str(path.resolve()))
                    self.assertEqual(fn(SAMPLE)["speckle"], 0.1)

    def test_missing_coherence_raises(self) -> None:
        with self.assertRaises(KeyError):
            condition({"pupil_fill_error": 0.2, "photons": 1.0})
