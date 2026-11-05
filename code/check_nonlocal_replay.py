"""Stress the finite causal lemma with deliberately nonlocal letters.
Uses the inspected archived engine as an implementation, and independently
checks prefix/fingerprint measurability and complete Cartesian products.
Finite tests do not replace the proof. Python >= 3.10; assertions required.
"""
from collections import Counter,defaultdict
from itertools import product
from fractions import Fraction
from pathlib import Path
import json,random
from upstream_container_engine import Model,Run,merge_counts
assert __debug__
class NonlocalModel(Model):
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw)
  rng=random.Random(self.seed+1234)
  self.permutation=list(range(self.length));rng.shuffle(self.permutation)
 def letter(self,w,i):
  return sum(((w>>self.permutation[(i+t)%self.length])&1)<<t for t in range(self.q))
 def feasible(self,w):
  return all(self.allowed(i,s,w%(2**i),(self.letter(w,i),)+tuple(self.letter(w,j) for j in targets)) for i,edges in self.edges.items() for s,targets in edges)
class NonlocalRun(Run):
 def __init__(self,m,word,*a,**kw):
  super().__init__(m,word,*a,**kw)
  self.actual=[m.letter(word,i) for i in range(m.N)]

def check(m,T0,T):
 feasible=[w for w in range(2**m.length) if m.feasible(w)]
 assert feasible
 # Every feasible word is used: conditional-support checks are exhaustive
 # for the stated finite model, not random samples from its support.
 runs=[NonlocalRun(m,w,T0,T).run() for w in feasible]
 cells={};supports=defaultdict(set);totals=Counter()
 for run in runs:
  F=tuple(sorted(run.F.items()))
  rr=NonlocalRun(m,run.word,T0,T,dict(F)).run()
  assert (run.F,run.A,run.states)==(rr.F,rr.A,rr.states)
  totals['replays']+=1
  for i in range(m.N):
   key=(i,run.word%2**i,F)
   val=(run.states[i],tuple(sorted(run.A[i])))
   if key in cells:
    assert cells[key]==val
    totals['same_prefix_fingerprint_comparisons']+=1
   cells[key]=val
   supports[key].add(m.letter(run.word,i))
  merge_counts(totals,run.stats)
 for run in runs:
  F=tuple(sorted(run.F.items()))
  for i in range(m.N):
   assert supports[i,run.word%2**i,F]<=run.A[i]
   totals['nonlocal_support_inclusions']+=1
  bad=0
  for i,edges in m.edges.items():
   for s,targets in edges:
    if any(not m.allowed(i,s,run.word%2**i,vs) for vs in product(*(run.A[j] for j in (i,)+targets))):bad+=1
   totals['complete_products_checked']+=len(edges)
  assert bad<=m.Q*(T0+m.D*sum(T.values()))*m.N
  assert len(run.F)<=m.Q*m.N*(Fraction(m.D*sum(T.values())+1,T0)+Fraction(1,T[2])+m.D*sum(Fraction(1+sum(T[l] for l in range(2,j)),T[j]) for j in range(3,m.r)))
 return {'name':m.name,'length':m.length,'q':m.q,'r':m.r,'permutation':m.permutation,'feasible_words':len(feasible),'thresholds':{'source':T0,**T},'counts':dict(totals)}

spec=[
 (NonlocalModel('nonlocal_triples',11,1,[(0,1,2),(0,3,6)],'sparse',3),1,{2:2}),
 (NonlocalModel('nonlocal_four',11,1,[(0,1,2,3)],'sparse',5),1,{2:5,3:2}),
 (NonlocalModel('nonlocal_four_Q4',10,2,[(0,2,4,6)],'sparse',9,query_order='max'),1,{2:7,3:2}),
 (NonlocalModel('nonlocal_five_Q4',10,2,[(0,2,4,6,8)],'sparse',11),1,{2:3,3:2,4:4}),
 (NonlocalModel('nonlocal_six',10,1,[(0,1,2,3,4,5)],'sparse',13,query_order='max'),1,{2:8,3:3,4:2,5:6})]
results=[check(*s) for s in spec]
total=Counter()
for r in results:merge_counts(total,r['counts'])
report={'status':'PASS','scope':'Exhaustive feasible-word tests on 5 nonlocal-letter models; not a universal certificate. Engine is archived code, verification of support/product claims is separate.','models':results,'totals':dict(total)}
Path(__file__).with_name('nonlocal_replay_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','models':len(results),'totals':dict(total)},indent=2))
