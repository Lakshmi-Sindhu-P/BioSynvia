import contextlib
from hashlib import sha256
import io
import json
from pathlib import Path
import tempfile
import unittest

from biosynvia.audit import audit
from biosynvia.cli import main


HEADER = "experiment_id,cultivation_id,time_hours,variable,value,unit\n"


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.sensors = self.root / "sensors.csv"
        self.measurements = self.root / "measurements.csv"
        self.sensors.write_text(HEADER + "pair1,A,0,pH,7,pH\npair1,B,0,pH,7,pH\npair2,C,0,pH,7,pH\n")
        self.measurements.write_text(HEADER + "pair1,A,2,VCD,1,cells/mL\npair1,B,2,VCD,2,cells/mL\npair2,C,2,VCD,3,cells/mL\n")

    def run_audit(self):
        return audit(self.sensors, self.measurements)

    def codes(self):
        return {error["code"] for error in self.run_audit()["errors"]}

    def test_valid_report_preserves_paired_group_identity(self):
        report = self.run_audit()
        self.assertTrue(report["valid"])
        self.assertEqual(report["cultivation_to_experiment"], {"A": "pair1", "B": "pair1", "C": "pair2"})
        self.assertEqual(report["target_candidates"][0]["experiment_count"], 2)
        self.assertEqual(report["sources"]["sensors"]["sha256"], sha256(self.sensors.read_bytes()).hexdigest())
        self.assertEqual(report, self.run_audit())

    def test_future_sensors_do_not_count_as_available(self):
        self.sensors.write_text(HEADER + "pair1,A,3,pH,7,pH\n")
        report = self.run_audit()
        self.assertEqual(report["target_candidates"][0]["observations_with_any_sensor_at_or_before_time"], 0)

    def test_blank_measurement_is_missing_not_zero(self):
        self.measurements.write_text(HEADER + "pair1,A,2,VCD,,cells/mL\n")
        summary = self.run_audit()["tables"]["measurements"]["variables"]["VCD"]
        self.assertEqual(summary["missing"], 1)
        self.assertIsNone(summary["min"])

    def test_duplicate_is_rejected_and_candidates_suppressed(self):
        with self.sensors.open("a") as handle:
            handle.write("pair1,A,0,pH,8,pH\n")
        self.assertIn("duplicate", self.codes())
        self.assertEqual(self.run_audit()["target_candidates"], [])

    def test_conflicting_experiment_between_tables_is_rejected(self):
        self.measurements.write_text(HEADER + "pair9,A,2,VCD,1,cells/mL\n")
        self.assertIn("group_conflict", self.codes())

    def test_mixed_units_are_rejected(self):
        self.measurements.write_text(HEADER + "pair1,A,2,VCD,1,cells/mL\npair1,A,3,VCD,2,cells/L\n")
        self.assertIn("unit", self.codes())

    def test_bad_numeric_values_are_rejected(self):
        for time, value in [("-1", "7"), ("nan", "7"), ("inf", "7"), ("0", "nan"), ("0", "inf"), ("zero", "7")]:
            with self.subTest(time=time, value=value):
                self.sensors.write_text(HEADER + f"pair1,A,{time},pH,{value},pH\n")
                self.assertIn("numeric", self.codes())

    def test_out_of_order_times_are_rejected(self):
        self.sensors.write_text(HEADER + "pair1,A,4,pH,7,pH\npair1,A,0,pH,7,pH\n")
        self.assertIn("time_order", self.codes())

    def test_malformed_headers_and_rows_are_rejected(self):
        for text, code in [("", "header"), ("a,a\n1,2\n", "header"),
                           (HEADER + "pair1,A,0,pH,7\n", "row_width"),
                           (HEADER + ",A,0,pH,7,pH\n", "required")]:
            with self.subTest(text=text):
                self.sensors.write_text(text)
                self.assertIn(code, self.codes())

    def test_header_only_and_invalid_encoding_are_rejected(self):
        self.sensors.write_text(HEADER)
        self.assertIn("empty", self.codes())
        self.sensors.write_bytes(b"\xff\xfe")
        self.assertIn("csv", self.codes())

    def call_cli(self, output):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(["audit", "--sensors", str(self.sensors),
                         "--measurements", str(self.measurements), "--output", str(output)])

    def test_cli_writes_report_and_preserves_inputs(self):
        original = self.sensors.read_bytes()
        output = self.root / "reports" / "audit.json"
        self.assertEqual(self.call_cli(output), 0)
        self.assertTrue(json.loads(output.read_text())["valid"])
        self.assertEqual(self.sensors.read_bytes(), original)
        self.assertEqual(self.call_cli(self.sensors), 1)
        self.assertEqual(self.sensors.read_bytes(), original)
        before = output.read_bytes()
        self.assertEqual(self.call_cli(output), 1)
        self.assertEqual(output.read_bytes(), before)

    def test_invalid_data_returns_nonzero_with_report(self):
        self.sensors.write_text(HEADER)
        output = self.root / "failed.json"
        self.assertEqual(self.call_cli(output), 2)
        self.assertFalse(json.loads(output.read_text())["valid"])

    def test_missing_source_returns_nonzero_without_report(self):
        self.sensors.unlink()
        output = self.root / "missing.json"
        self.assertEqual(self.call_cli(output), 1)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
