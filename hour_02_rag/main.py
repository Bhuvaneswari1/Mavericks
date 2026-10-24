"""Hour 2: load → chunk → embed/index → retrieve → answer."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.core import Knowledge,answer,ROOT
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--policy',default=str(ROOT/'data/policies.csv')); p.add_argument('--question',default='What documents for account opening?'); p.add_argument('--semantic',action='store_true')
    a=p.parse_args(); print(json.dumps(answer(a.question,Knowledge(a.policy,a.semantic)),indent=2))
