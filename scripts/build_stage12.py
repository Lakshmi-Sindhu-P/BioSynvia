"""Save versioned Stage1/2 protocol evidence; no model fitting."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from biosynvia.stage12 import build
parser=argparse.ArgumentParser()
parser.add_argument('--archive',type=Path,default=Path('data/raw/Dataset.zip'))
parser.add_argument('--parent',type=Path,default=Path('data/processed/v3'))
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--configs',type=Path,default=Path('configs'))
args=parser.parse_args()
result=build(args.archive,args.parent,args.output,args.configs,command=' '.join(sys.argv))
print(result['status'],result['tables'])
