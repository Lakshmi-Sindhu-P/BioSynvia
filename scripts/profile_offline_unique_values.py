"""Enumerate original offline assay values without substituting aligned zeros.

Uses the source-exact per-cell audit table, not the publisher-aligned values.
Only descriptive counts are pooled; individual run identities remain intact.
"""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def profile(source, output):
    source, output = Path(source), Path(output)
    manifest_path = source.parent / 'stage12_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    if digest(source) != manifest['outputs'][source.name]:
        raise ValueError('Source table does not match its frozen manifest.')
    if output.exists():
        raise ValueError('Choose a new output directory; existing reports are preserved.')
    groups = defaultdict(list)
    with source.open(newline='') as handle:
        for row in csv.DictReader(handle):
            family = row['source_sheet'].split('_offline_', 1)[1]
            if family not in ('CellAnalysis', 'MediumAnalysis'):
                raise ValueError('Unexpected offline source family.')
            if row['field'] == 'Time (h)':
                continue
            if row['run_id'] != row['experiment_id'] + '_' + row['reactor_id']:
                raise ValueError('Inconsistent run identity.')
            value = json.loads(row['raw_value_json'])
            if (value is None) != (row['source_blank'] == 'True'):
                raise ValueError('Original blank flag and original value disagree.')
            if value is not None and (isinstance(value, bool) or
                    not isinstance(value, (float, int)) or not math.isfinite(value)):
                raise ValueError('Unexpected nonnumeric or nonfinite assay value.')
            groups[(family, row['field'], row['run_id'])].append(value)
    output.mkdir(parents=True)
    global_groups = defaultdict(list)
    for (family, field, run), values in groups.items():
        global_groups[(family, field)].extend(values)

    def summarize(family, field, run, values):
        numeric = [v for v in values if v is not None]
        counts = Counter(numeric)
        return {'family': family, 'field': field, 'run_id': run,
                'records': len(values), 'missing_original_cells': len(values)-len(numeric),
                'recorded_numeric_zeros': counts[0], 'distinct_numeric_values': len(counts),
                'minimum': min(numeric) if numeric else None,
                'maximum': max(numeric) if numeric else None,
                'values_and_counts': [{'value': v, 'count': counts[v]} for v in sorted(counts)]}

    pooled = [summarize(f, c, 'ALL_RUNS_DESCRIPTIVE_ONLY', v)
              for (f, c), v in sorted(global_groups.items())]
    per_run = [summarize(f, c, r, v) for (f, c, r), v in sorted(groups.items())]
    for name, rows in [('summary.csv', pooled), ('summary_by_run.csv', per_run)]:
        with (output/name).open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=[k for k in rows[0] if k != 'values_and_counts'])
            writer.writeheader()
            writer.writerows({k: v for k, v in r.items() if k != 'values_and_counts'} for r in rows)
    (output/'distinct_values.json').write_text(json.dumps(pooled, indent=2, allow_nan=False)+'\n')
    (output/'distinct_values_by_run.json').write_text(json.dumps(per_run, indent=2, allow_nan=False)+'\n')
    metadata = {'source': str(source.resolve()), 'source_sha256': digest(source),
                'source_manifest_sha256': digest(manifest_path),
                'method': 'Exact numeric equality of decoded original raw_value_json. No rounding or imputation. '
                          'Nulls counted separately; zero remains numeric. Time columns excluded. '
                          'Pooling is descriptive only; no joins or model fitting.',
                'measurement_columns': len(pooled), 'run_field_groups': len(per_run),
                'outputs': {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()}}
    (output/'provenance.json').write_text(json.dumps(metadata, indent=2)+'\n')
    return pooled


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('data/processed/v5/assay_source_cells.csv'))
    parser.add_argument('--output', type=Path, default=Path('reports/offline-unique-values'))
    args = parser.parse_args()
    rows = profile(args.source, args.output)
    print(json.dumps([{k: v for k, v in row.items() if k != 'values_and_counts'} for row in rows], indent=2))
