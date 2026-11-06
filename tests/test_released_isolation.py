"""Regression proof for the frozen release and deliberately crossed identities."""
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.verify_released_isolation import assert_isolation, verify


class ReleasedIsolationTests(unittest.TestCase):
    def setUp(self):
        self.assays = [{'assay_id': 'a', 'experiment_id': 'EXP001',
                        'reactor_id': 'R01', 'run_id': 'EXP001_R01'}]
        self.lineage = [{**self.assays[0], 'feature': 'sensor',
                         'source_sheet': 'R01_inline_CO2',
                         'source_file': 'Individual raw data tables/EXP001_batch.xlsx'}]

    def test_released_v6_manifest_and_all_lineage_identities(self):
        bundle = Path(__file__).resolve().parents[1] / 'data/processed/v6'
        result = verify(bundle)
        self.assertEqual((result['assays'], result['lineage_rows']), (378, 15120))

    def test_rejects_cross_reactor_and_cross_experiment(self):
        for field, value in [('reactor_id', 'R02'), ('experiment_id', 'EXP002'),
                             ('run_id', 'EXP002_R02'), ('source_sheet', 'R02_inline_CO2'),
                             ('source_file', 'EXP002_batch.xlsx')]:
            with self.subTest(field=field):
                rows = deepcopy(self.lineage)
                rows[0][field] = value
                with self.assertRaises(ValueError):
                    assert_isolation(self.assays, rows)

    def test_rejects_offline_predictors(self):
        self.lineage[0]['source_sheet'] = 'R01_offline_CellAnalysis'
        with self.assertRaises(ValueError):
            assert_isolation(self.assays, self.lineage)

    def test_rejects_duplicate_parents_and_lineage(self):
        with self.assertRaises(ValueError):
            assert_isolation(self.assays * 2, self.lineage)
        with self.assertRaises(ValueError):
            assert_isolation(self.assays, self.lineage * 2)

    def test_rejects_wrong_manifest(self):
        with self.assertRaises(ValueError):
            verify(Path(__file__).resolve().parents[1] / 'data/processed/v6', '0' * 64)


if __name__ == '__main__':
    unittest.main()
