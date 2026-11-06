import importlib.util
from pathlib import Path
import tempfile
import unittest

HAS_ANALYSIS = importlib.util.find_spec("pandas") is not None
if HAS_ANALYSIS:
    import pandas as pd
    from biosynvia.preparation import (TARGET, backup_archive, combine_original_assays,
                                      numeric_copy, snapshot_stream)


@unittest.skipUnless(HAS_ANALYSIS, "Run with optional analysis dependencies")
class PreparationTests(unittest.TestCase):
    def test_working_copy_changes_types_without_mutating_original(self):
        original = pd.DataFrame({"time": ["0", "1"], "value": ["bad", "3.2"]})
        preserved = original.copy(deep=True)
        working, audit = numeric_copy(original)
        self.assertTrue(pd.isna(working.value.iloc[0]))
        self.assertEqual(audit[1]["new_invalid_or_nonfinite"], 1)
        pd.testing.assert_frame_equal(original, preserved)
        working.loc[1, "value"] = 99
        self.assertEqual(original.loc[1, "value"], "3.2")

    def test_backup_is_separate_verified_and_never_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.zip"
            source.write_bytes(b"synthetic source")
            backup, digest = backup_archive(source, root / "backup")
            self.assertNotEqual(source, backup)
            self.assertEqual(source.read_bytes(), backup.read_bytes())
            self.assertEqual(backup_archive(source, root / "backup"), (backup, digest))
            backup.write_bytes(b"altered backup")
            with self.assertRaisesRegex(ValueError, "refusing overwrite"):
                backup_archive(source, root / "backup")

    def test_missing_assay_and_recorded_zero_are_distinct(self):
        cell = pd.DataFrame({"Time (h)": [0, 1], TARGET: [0., 4.]})
        medium = pd.DataFrame({"Time (h)": [0, 1], "Glucose (g/L)": [None, 3.]})
        result, _ = combine_original_assays(cell, medium)
        self.assertEqual(result[TARGET].iloc[0], 0)
        self.assertTrue(pd.isna(result["Glucose (g/L)"].iloc[0]))
        self.assertEqual(result.target_review_reason.iloc[0], "recorded_zero_pending_assay_review")
        self.assertFalse(result.scientific_label_approved.any())

    def test_future_perturbation_cannot_change_snapshot(self):
        original = pd.DataFrame({"Time (h)": [0., 1., 2.], "signal": [10., 20., 30.], "Status": ["Ok"] * 3})
        first = snapshot_stream(original, [1.5], 1)
        changed = original.copy(deep=True)
        changed.loc[2, "signal"] = 9999
        self.assertEqual(first, snapshot_stream(changed, [1.5], 1))
        self.assertEqual(first[0]["inspection_value"], 20)

    def test_stale_and_warning_values_remain_in_lineage_but_not_features(self):
        original = pd.DataFrame({"Time (h)": [0., 1.], "signal": [10., 20.], "Status": ["Ok", "Warning Active"]})
        warning = snapshot_stream(original, [1.], 1)[0]
        self.assertEqual(warning["source_value"], 20)
        self.assertIsNone(warning["inspection_value"])
        self.assertEqual(warning["reason"], "sensor_status_requires_review")
        stale = snapshot_stream(original, [5.], 1)[0]
        self.assertEqual(stale["reason"], "stale")

    def test_duplicate_sensor_times_retain_alternatives_and_exclude_ambiguous_value(self):
        original = pd.DataFrame({"Time (h)": [0., 0.], "signal": [1., 2.]})
        import json
        result = snapshot_stream(original, [0.], 1)[0]
        self.assertEqual(result["reason"], "duplicate_source_time_requires_review")
        self.assertIsNone(result["inspection_value"])
        self.assertIsNone(result["source_value"])
        self.assertEqual([row["value"] for row in json.loads(result["source_candidates_json"])], [1., 2.])

    def test_constant_zero_fit_channel_flag_does_not_discard_valid_batch_feed_zero(self):
        original = pd.DataFrame({"Time (h)": [0., 1.], "C (300kHz)": [0., 0.],
                                 "Cumulative feed weight (g)": [0., 0.]})
        rows = snapshot_stream(original, [1.], 1)
        self.assertEqual(rows[0]["reason"], "constant_zero_derived_channel")
        self.assertEqual(rows[1]["inspection_value"], 0)

    def test_derived_channel_quality_does_not_learn_from_future_nonzero(self):
        original = pd.DataFrame({"Time (h)": [0., 1., 2.], "C (300kHz)": [0., 0., 0.]})
        first = snapshot_stream(original, [1.], 1)
        original.loc[2, "C (300kHz)"] = 100
        self.assertEqual(first, snapshot_stream(original, [1.], 1))


if __name__ == "__main__":
    unittest.main()
