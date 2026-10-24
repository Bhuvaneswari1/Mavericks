"""Hour 5: invoke the real LangGraph with an inspectable state."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.core import ROOT
from shared.graph import build
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--question',default='What documents for account opening?'); p.add_argument('--policy',default=str(ROOT/'data/policies.csv')); p.add_argument('--requests',default=str(ROOT/'data/requests.csv')); p.add_argument('--semantic',action='store_true'); a=p.parse_args()
    print(json.dumps(build(Path(a.policy),Path(a.requests),a.semantic).invoke({'question':a.question},config={'recursion_limit':10}),indent=2))
