"""Independent finite diagnostics for Stage 16's entropy and boundary transfer.
No finite test certifies the infinite theorem. Uses standard library only.
"""
from collections import defaultdict, Counter
from itertools import product, combinations
from math import log
import random, json
from pathlib import Path

def entropy(weights):
    total=sum(weights)
    return -sum((w/total)*log(w/total) for w in weights if w)

def conditional(words, weights, value, condition):
    groups=defaultdict(lambda:defaultdict(float))
    for w,p in zip(words,weights):groups[condition(w)][value(w)]+=p
    total=sum(weights)
    return sum(sum(g.values())/total*entropy(g.values()) for g in groups.values())

def expected_log_support(words,weights,value,condition):
    groups=defaultdict(set)
    for w in words:groups[condition(w)].add(value(w))
    total=sum(weights)
    return sum(p*log(len(groups[condition(w)]))/total for w,p in zip(words,weights))

rng=random.Random(4062026)
checks=0
for L in range(2,7):
    universe=list(product(range(2),repeat=L))
    masks=range(1,1<<len(universe)) if L<=3 else [rng.randrange(1,1<<len(universe)) for _ in range(160)]
    for mask in masks:
        words=[w for i,w in enumerate(universe) if mask>>i&1]
        for F in [lambda w:0,lambda w:w[-1],lambda w:sum(w)%2]:
            weights=[1+i%3 for i in range(len(words))]
            H=conditional(words,weights,lambda w:w,F)
            hs=[conditional(words,weights,lambda w,t=t:w[t],lambda w,t=t:(w[:t],F(w))) for t in range(L)]
            assert abs(H-sum(hs))<1e-10
            for b in range(1,L):
                for k in range(1,L-b+1):
                    N=L-b-k+1
                    rhs=0
                    for j in range(N):
                        cond=lambda w,j=j:(w[:j+b],F(w))
                        val=lambda w,j=j,k=k:w[j+b:j+b+k]
                        h=conditional(words,weights,val,cond)
                        assert abs(h-sum(hs[j+b:j+b+k]))<1e-10
                        ew=expected_log_support(words,weights,val,cond)
                        assert h<=ew+1e-10
                        rhs+=ew
                    assert H<=rhs/k+(b+k-1)*log(2)+1e-10
                    checks+=1

# Direct incidence counts, including systems shorter than their template span.
incidence=0
for r in range(3,6):
    for N in range(1,12):
        alltemplates=[(0,)+c for c in combinations(range(1,9),r-1)]
        for _ in range(80):
            templates=[rng.choice(alltemplates) for _ in range(1+rng.randrange(4))]
            K=len(templates);R=max(t[-1] for t in templates)
            weights=[rng.randrange(5) for _ in range(N)];M=4
            B=rng.randrange(1,r*M+4)
            edges=[tuple(j+d for d in t) for t in templates for j in range(max(0,N-t[-1]))]
            bad=sum(sum(weights[v] for v in e)>B for e in edges)
            lhs=r*K*sum(weights)
            rhs=B*K*N+r*M*bad+r*M*K*R
            assert lhs<=rhs
            degrees=Counter(v for e in edges for v in e)
            assert sum(r*K-degrees[v] for v in range(N))==r*sum(min(N,t[-1]) for t in templates)
            incidence+=1

# Negative control: supports from one path need not form a valid rectangle.
W=[(0,0,0),(0,0,1),(1,1,1)];x=(0,0,0)
supports=[{w[t] for w in W if w[:t]==x[:t]} for t in range(3)]
assert all(sum(w)%3 in {0,1} for w in W)
assert any(sum(w)%3==2 for w in product(*supports))
result={'status':'PASS_COMPONENT_DIAGNOSTICS_ONLY','entropy_cases':checks,'incidence_cases':incidence,'conditional_support_negative_control':'reproduced','scope':'Overlap entropy and finite boundary counts; no proof certification by computation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
