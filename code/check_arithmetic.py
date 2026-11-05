#!/usr/bin/env python3
"""Independent finite checks of the arithmetic identities, not of the theorem."""
from fractions import Fraction
from itertools import product
from random import Random
import json
from pathlib import Path
rng=Random(40620261105)

def unit(p, bound):
    while True:
        n=rng.randrange(-bound,bound+1)
        if n%p:return n

def mod_fraction(x, p, m):
    x=Fraction(x)
    modulus=p**m
    return (x.numerator*pow(x.denominator,-1,modulus))%modulus

def val_int(n,p):
    if n==0:return None
    v=0
    while n%p==0:n//=p;v+=1
    return v

def val_fraction(x,p):
    x=Fraction(x)
    if x==0:return None
    return val_int(x.numerator,p)-val_int(x.denominator,p)

counts={'ordinary_carry':0,'integer_approximation_and_anchor':0,'two_target_residues':0,'valuation_nondegeneracy':0,'template_pair_codegrees':0}
for p in [2,3,5,7]:
 for r in range(3,9):
  for _ in range(200):
   q=rng.randrange(1,5);j=rng.randrange(0,5)
   es=[];last=0
   for t in range(r-2):last+=rng.randrange(q,q+4);es.append(last)
   E=last+rng.randrange(q,q+4);v=j+E
   A=[unit(p,20) for t in es]
   u=Fraction(unit(p,20),unit(p,20));d=Fraction(rng.randrange(-500,501),unit(p,20))
   X=rng.randrange(p**(v+q));Y=[a*X for a in A]
   c=1+sum(a*p**e for a,e in zip(A,es))+p**E*u
   Z=c*X+d
   P=X%(p**j)
   T=d+p**E*u*P
   tv=mod_fraction(T,p,v)
   Dj=(T-tv)/p**v
   assert Dj.denominator%p
   lows=[X%(p**v)]+[p**e*(y%(p**(v-e))) for e,y in zip(es,Y)]+[tv]
   carry=sum(lows)//p**v
   assert 0<=carry<=r-1
   B0=(X//p**j)%(p**q)
   Bmid=[(y//p**(v-e))%(p**q) for e,y in zip(es,Y)]
   Bend=(X//p**v)%(p**q)
   out=(mod_fraction(Z,p,v+q)//p**v)%(p**q)
   assert out==mod_fraction(u*B0+sum(Bmid)+Bend+Dj+carry,p,q)
   counts['ordinary_carry']+=1
   # Exact ordinary-integer approximation and actual-unit anchor algebra.
   a=[Fraction(unit(p,20),unit(p,20)) for t in es]
   ustar=Fraction(unit(p,20),unit(p,20))
   cstar=1+sum(at*p**e for at,e in zip(a,es))+ustar*p**E
   approx=[mod_fraction(at,p,E-e+q) for at,e in zip(a,es)]
   delta=Fraction(rng.randrange(-20,21)*p**(E+q),unit(p,20))
   cnew=(1+delta)*cstar
   unew=(cnew-1-sum(at*p**e for at,e in zip(approx,es)))/p**E
   assert val_fraction(unew,p)==0
   diff=val_fraction(unew-ustar,p)
   assert diff is None or diff>=q
   counts['integer_approximation_and_anchor']+=1
  # Two-target reduction: each fixed residue has at most two ordinary lifts.
  M=r-1;b=1
  while p**b<=M:b+=1
  lowrange=range(-M,p**b)
  for a0 in range(p**b):
   reps=[z for z in lowrange if z%p**b==a0]
   assert 1<=len(reps)<=2
   if len(reps)==2:assert reps[1]-reps[0]==p**b
   counts['two_target_residues']+=1
 for _ in range(1000):
  exponents=sorted(rng.sample(range(18),rng.randrange(1,7)))
  terms=[unit(p,100)*p**e for e in exponents]
  for bits in product([0,1],repeat=len(terms)):
   if not any(bits):continue
   selected=[(e,t) for e,t,b in zip(exponents,terms,bits) if b]
   assert val_int(sum(t for e,t in selected),p)==selected[0][0]
   counts['valuation_nondegeneracy']+=1
# Separated template pair-codegree; arbitrary offsets satisfying exact condition.
for r in range(3,9):
 for _ in range(100):
  prev=0;templates=[]
  for i in range(5):
   gaps=[prev+1+rng.randrange(5) for t in range(r-1)]
   pos=[0]
   for g in gaps:pos.append(pos[-1]+g)
   prev=pos[-1];templates.append(pos)
  distance_to_pairs={}
  for i,offsets in enumerate(templates):
   for a in range(r):
    for b in range(a+1,r):distance_to_pairs.setdefault(offsets[b]-offsets[a],[]).append((i,a,b))
  assert all(len({x[0] for x in xs})==1 and len(xs)<=r*(r-1)//2 for xs in distance_to_pairs.values())
  assert len({x for row in templates for x in row[1:]})==sum(len(row)-1 for row in templates)
  counts['template_pair_codegrees']+=1
out={'status':'PASS','scope':'Finite checks of arithmetic identities only; no verification of ESS or container lemma or dimension theorem','seed':40620261105,'counts':counts}
Path(__file__).with_name('arithmetic_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
