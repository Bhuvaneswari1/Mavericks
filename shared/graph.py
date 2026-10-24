"""Shared LangGraph capstone: supervisor → one worker → reviewer → END."""
from typing import TypedDict
import re
from shared.core import ROOT,Knowledge,answer,lookup

class State(TypedDict,total=False):
    question: str
    route: str
    answer: str
    sources: list[str]
    steps: list[str]
    review: str

def route_question(question):
    if re.search(r'\bSR\d+\b',question,re.I):
        return 'request'
    if any(w in question.lower() for w in ['policy','account','card','address','document','opening']):
        return 'policy'
    return 'general'

def build(policy=ROOT/'data/policies.csv',requests=ROOT/'data/requests.csv',semantic=False):
    from langgraph.graph import StateGraph,START,END
    from langsmith import traceable
    knowledge=Knowledge(policy,semantic)
    @traceable(name='bank-supervisor')
    def supervisor(s):
        return {'route':route_question(s['question']),'steps':['supervisor']}
    @traceable(name='bank-policy-worker')
    def policy_worker(s):
        return {**answer(s['question'],knowledge),'steps':s['steps']+['policy_worker']}
    @traceable(name='bank-request-worker')
    def request_worker(s):
        rid=re.search(r'\bSR\d+\b',s['question'],re.I).group().upper()
        row=lookup(rid,requests)
        text=row.get('error') or f"{row['request_id']}: {row['service']} — {row['status']}. Next action: {row['next_action']}"
        return {'answer':text,'sources':[] if 'error' in row else [f'{requests.name if hasattr(requests,"name") else "requests.csv"}:{rid}'],'steps':s['steps']+['request_worker']}
    def general(s):
        return {'answer':'Ask about account opening, lost cards, address updates, or a synthetic request ID such as SR1001. Other topics need demo branch staff.','sources':[],'steps':s['steps']+['general']}
    def reviewer(s):
        # Deterministic check observes provenance, not factual entailment.
        return {'review':'Source references attached; human verification required.' if s.get('sources') else 'No source-backed response; use branch follow-up.', 'steps':s['steps']+['reviewer']}
    g=StateGraph(State)
    for name,fn in [('supervisor',supervisor),('policy',policy_worker),('request',request_worker),('general',general),('reviewer',reviewer)]:
        g.add_node(name,fn)
    g.add_edge(START,'supervisor')
    g.add_conditional_edges('supervisor',lambda s:s['route'],{'policy':'policy','request':'request','general':'general'})
    for name in ['policy','request','general']: g.add_edge(name,'reviewer')
    g.add_edge('reviewer',END)
    return g.compile()
