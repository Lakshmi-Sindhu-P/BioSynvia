"""Manifest-bound, read-only identity verification of the released v6 bundle."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

V6_MANIFEST = 'd74465cbb353af872681cf3c6bbd1055ee0523441a889ec90832d7fc3affa45e'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assert_isolation(assays, lineage):
    parents = {}
    for row in assays:
        key = row['assay_id']
        if key in parents:
            raise ValueError('Duplicate assay identity.')
        if row['run_id'] != row['experiment_id'] + '_' + row['reactor_id']:
            raise ValueError('Invalid parent run identity.')
        parents[key] = row
    seen = set()
    for row in lineage:
        parent = parents.get(row['assay_id'])
        if parent is None:
            raise ValueError('Lineage lacks an assay parent.')
        if any(row[key] != parent[key] for key in ('experiment_id', 'reactor_id', 'run_id')):
            raise ValueError('Cross-experiment or cross-reactor lineage.')
        if not row['source_sheet'].startswith(row['reactor_id'] + '_'):
            raise ValueError('Source sheet belongs to another reactor.')
        if not Path(row['source_file']).name.startswith(row['experiment_id'] + '_'):
            raise ValueError('Source workbook belongs to another experiment.')
        if '_offline_' in row['source_sheet']:
            raise ValueError('Offline assay used as inline predictor.')
        key = (row['assay_id'], row['feature'])
        if key in seen:
            raise ValueError('Duplicate assay-feature lineage.')
        seen.add(key)
    if {key[0] for key in seen} != set(parents):
        raise ValueError('Assays and lineage do not cover the same identities.')
    return {'assays': len(parents), 'lineage_rows': len(seen), 'identity_mismatches': 0}


def verify(bundle, expected_manifest=V6_MANIFEST):
    bundle = Path(bundle)
    manifest_path = bundle / 'stage12_manifest.json'
    if sha(manifest_path) != expected_manifest:
        raise ValueError('Released manifest fingerprint mismatch.')
    manifest = json.loads(manifest_path.read_text())
    tables = {}
    for name in ('assay_decisions.csv', 'feature_lineage.csv'):
        path = bundle / name
        if sha(path) != manifest['outputs'][name]:
            raise ValueError('Released table fingerprint mismatch.')
        with path.open(newline='') as handle:
            tables[name] = list(csv.DictReader(handle))
    result = assert_isolation(tables['assay_decisions.csv'], tables['feature_lineage.csv'])
    if result['lineage_rows'] != result['assays'] * 40:
        raise ValueError('Expected forty candidate features per original assay.')
    return {**result, 'manifest_sha256': expected_manifest,
            'table_sha256': {name: sha(bundle/name) for name in tables},
            'model_fit_permitted': False, 'scope': 'Engineering identity check, not scientific approval.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, default=Path('data/processed/v6'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.bundle)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded)
