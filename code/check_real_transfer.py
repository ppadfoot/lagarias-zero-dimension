"""Exact rational checks for the finite-word bridge; no old verifier imported."""
from fractions import Fraction
from pathlib import Path
import json


def floor(x):
    return x.numerator // x.denominator


def digit01_integer(n):
    while n:
        if n % 3 == 2:
            return False
        n //= 3
    return True


def full_digit01(x):
    ip = floor(x)
    if not digit01_integer(ip):
        return False
    f = x - ip
    seen = set()
    while f and f not in seen:
        seen.add(f)
        y = 3*f
        d = floor(y)
        if d == 2:
            return False
        f = y-d
    return True


# Include all finite and purely periodic 0/1 words through length six,
# several integer parts, and rational points outside the target for testing
# the exact identity independently of the digit restriction.
points = {Fraction(a,b) for b in range(1,32) for a in range(0,4*b+1)}
for length in range(1,7):
    for mask in range(2**length):
        n = sum(((mask >> j) & 1)*3**j for j in range(length))
        for ip in (0,1,3,4):
            points.add(ip+Fraction(n,3**length))
            points.add(ip+Fraction(n,3**length-1))
slopes = sorted({Fraction(p,q) for p in range(1,13) for q in range(1,13)
                 if p % 3 and q % 3} | {Fraction(2)**j for j in range(-6,7)})
full_flags = {x:full_digit01(x) for x in points}
counts = dict(identities=0, full_target_instances=0, finite_target_instances=0,
              negative_shifts=0, rational_noninteger_shifts=0)
for c in slopes:
    p,q = c.numerator,c.denominator
    for x in sorted(points):
        both_full = full_flags[x] and full_digit01(c*x)
        for L in range(1,8):
            mod = 3**L
            tx,ty = floor(mod*x),floor(mod*c*x)
            u,y = tx % mod,ty % mod
            beta = ty-c*tx
            assert Fraction(-1) < beta < c
            assert (q*beta).denominator == 1
            assert beta.denominator % 3
            residue = ((c*u+beta).numerator *
                       pow((c*u+beta).denominator,-1,mod)) % mod
            assert residue == y
            assert tx//mod == floor(x)
            counts['identities'] += 1
            counts['negative_shifts'] += beta < 0
            counts['rational_noninteger_shifts'] += beta.denominator != 1
            if digit01_integer(tx) and digit01_integer(ty):
                assert digit01_integer(u) and digit01_integer(residue)
                counts['finite_target_instances'] += 1
            if both_full:
                assert digit01_integer(tx) and digit01_integer(ty)
                assert digit01_integer(u) and digit01_integer(residue)
                counts['full_target_instances'] += 1

varying=[]
x,c=Fraction(1,2),Fraction(1,4)
assert full_digit01(x) and full_digit01(c*x)
for L in range(1,9):
    beta=floor(3**L*c*x)-c*floor(3**L*x)
    varying.append({'L':L,'beta':str(beta)})
assert {v['beta'] for v in varying} == {'0','-1/4'}
result={'status':'PASS','points':len(points),'slopes':len(slopes),**counts,
        'changing_shift_example':{'X':'1/2','c':'1/4','values':varying},
        'scope':'Exact finite bridge only; the dimension proof additionally uses the independently reviewed causal entropy theorem and infinite extraction.'}
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
