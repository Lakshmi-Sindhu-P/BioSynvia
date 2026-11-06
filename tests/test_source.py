from hashlib import md5
from pathlib import Path
import tempfile
import unittest
import zipfile

from biosynvia.source import inventory_archive, reconcile_structure


class SourceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "synthetic.zip"

    def test_checksum_mismatch_blocks_inventory(self):
        self.path.write_bytes(b"incorrect download")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            inventory_archive(self.path)

    def test_inventory_counts_and_does_not_extract(self):
        with zipfile.ZipFile(self.path, "w") as archive:
            for index in range(12):
                mode = "batch" if index < 9 else "fed-batch"
                archive.writestr(f"raw/EXP{index + 1:03d}_{mode}.xlsx", b"synthetic placeholder")
                for reactor in ("R01", "R02"):
                    for kind in ("inline", "offline"):
                        archive.writestr(f"aligned/EXP{index + 1:03d}_{mode}_{reactor}_{kind}.csv", "synthetic")
        checksum = md5(self.path.read_bytes(), usedforsecurity=False).hexdigest()
        report = inventory_archive(self.path, expected_md5=checksum)
        self.assertEqual(report["warnings"], [])
        self.assertEqual(len(report["files"]), 60)
        self.assertTrue(report["checksum_verified"])
        self.assertTrue(report["experiment_structure"]["valid"])
        self.assertFalse((self.path.parent / "raw").exists())

    def test_incomplete_archive_and_unsafe_path_are_flagged(self):
        with zipfile.ZipFile(self.path, "w") as archive:
            archive.writestr("../bad.csv", "synthetic")
        checksum = md5(self.path.read_bytes(), usedforsecurity=False).hexdigest()
        report = inventory_archive(self.path, expected_md5=checksum)
        self.assertEqual(len(report["warnings"]), 4)

    def test_duplicate_combination_cannot_hide_a_missing_reactor(self):
        files = [{"path": "aligned/EXP001_batch_R01_inline.csv"},
                 {"path": "duplicate/EXP001_batch_R01_inline.csv"}]
        result = reconcile_structure(files)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Duplicate aligned" in error for error in result["errors"]))
        self.assertTrue(any("Missing aligned combination: EXP001/R02/inline" in error
                            for error in result["errors"]))

    def test_mode_mismatch_is_rejected(self):
        files = [{"path": "raw/EXP001_batch.xlsx"},
                 {"path": "aligned/EXP001_fed-batch_R01_inline.csv"}]
        result = reconcile_structure(files)
        self.assertTrue(any("Mode mismatch" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
