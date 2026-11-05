"""A nonvacuous finite instance of the exact stated constants.
Latin-square triples have pair-codegree 1 and matching future links.
N=3072, |E|=1048576, theta=1/2, E_bad_bound=768000 < |E|.
No claim that a finite instance proves the infinite theorem.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import json
from upstream_container_engine import Run
assert __debug__
class Row:
 def __init__(self,i,n):self.i,self.n=i,n
 def __len__(self):return self.n if self.i<self.n else 0
 def __iter__(self):
  if self.i<self.n:
   for u in range(self.n):yield u,(self.n+u,2*self.n+(u+self.i)%self.n)
class Edges:
 def __init__(self,n):self.n=n
 def __getitem__(self,i):return Row(i,self.n)
 def items(self):
  for i in range(3*self.n):yield i,self[i]
 def values(self):
  for i in range(3*self.n):yield self[i]
class LatinModel:
 def __init__(self,n):
  self.n=n;self.N=3*n;self.length=3*n;self.Q=2;self.q=1;self.r=3;self.C=1;self.D=1;self.query_order='min';self.edges=Edges(n)
 def allowed(self,i,s,prefix,letters):return letters!=(1,1,1)

def main():
 n=1024;m=LatinModel(n);Ts=120;T={2:5}
 theta=m.Q*(Fraction(m.D*sum(T.values())+1,Ts)+Fraction(1,T[2]))
 bad_bound=m.Q*(Ts+m.D*sum(T.values()))*m.N
 assert theta==Fraction(1,2)
 assert bad_bound<n*n
 # First block all true 1, two later blocks all true 0. Every edge is allowed.
 word=(1<<n)-1
 run=Run(m,word,Ts,T).run()
 replay=Run(m,word,Ts,T,dict(run.F)).run()
 assert (run.F,run.A,run.states)==(replay.F,replay.A,replay.states)
 # Independent exact combinatorial check: forbidden triple occurs in the
 # complete assigned product iff each one of its three palettes contains 1.
 bad=sum(1 for i in range(n) for u in range(n) if all(1 in run.A[j] for j in (i,n+u,2*n+(u+i)%n)))
 assert bad<=bad_bound
 assert len(run.F)<=theta*m.N
 # Each source's target positions are disjoint; each cross-block pair has
 # one possible third endpoint determined by s=v-u modulo n. No within-block
 # pair occurs. Thus C=1, established algebraically for all listed edges.
 report={'status':'PASS','N':m.N,'edge_count':n*n,'alphabet_size':2,'arity':3,'pair_codegree':1,'thresholds':{'source':Ts,'rank2':5},'theta':str(theta),'fingerprint_bound':str(theta*m.N),'actual_fingerprint_size':len(run.F),'bad_edge_bound':bad_bound,'actual_bad_edges':bad,'nonvacuous':bad_bound<n*n,'full_fingerprint_replay':True,'counters':dict(run.stats)}
 Path(__file__).with_name('nonvacuous_results.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
