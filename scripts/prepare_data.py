"""Back up original data and save copied, queryable inspection datasets."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from biosynvia.preparation import prepare

parser = argparse.ArgumentParser()
parser.add_argument("--archive", type=Path, default=Path("data/raw/Dataset.zip"))
parser.add_argument("--backups", type=Path, default=Path("data/backups"))
parser.add_argument("--output", type=Path, default=Path("data/processed/v1"))
parser.add_argument("--max-age-minutes", type=float, default=5)
args = parser.parse_args()
prepare(args.archive, args.backups, args.output, args.max_age_minutes)
