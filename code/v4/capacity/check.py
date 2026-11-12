"""Reproducible finite audits of sharpened capacity and affine carry."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent
RNG = random.Random(406120211)


def residue(x, m):
    x = Fraction(x)
    return x.numerator * pow(x.denominator, -1, m) % m


def run():
    capacity = 0
    maxima = {}
    for q in (1, 2, 3):
        m = 3**q
        sig = {sum(a*3**j for j, a in enumerate(w))
               for w in product((0, 1), repeat=q)}
        arr = sorted(sig)
        maximum = 0
        for u in range(m):
            if u % 3 == 0:
                continue
            for z in range(m):
                target = {(a+z+e) % m for a in sig for e in (0, 1)}
                for mask in range(1, 1 << len(arr)):
                    A = [a for i, a in enumerate(arr) if mask >> i & 1]
                    B = set(sig)
                    for a in A:
                        B &= {(t-u*a) % m for t in target}
                    assert len(A)*len(B) <= 2**(q+1)
                    maximum = max(maximum, len(A)*len(B))
                    capacity += 1
        assert maximum == 2**(q+1)
        maxima[q] = maximum
    affine = 0
    for _ in range(10000):
        q, E, j = RNG.randint(1, 6), RNG.randint(1, 8), RNG.randint(0, 7)
        v = j+E
        X = RNG.randrange(3**(v+q))
        u = Fraction(RNG.choice([n for n in range(-50, 51) if n % 3]),
                     RNG.choice([n for n in range(1, 30) if n % 3]))
        beta = Fraction(RNG.randint(-10000, 10000),
                        RNG.choice([n for n in range(1, 30) if n % 3]))
        c = 1+3**E*u
        P = X % 3**j
        t = beta+3**E*u*P
        low = residue(t, 3**v)
        D = (t-low)/3**v
        carry = ((X % 3**v)+low)//3**v
        predicted = residue(u*((X//3**j) % 3**q)
                            + (X//3**v) % 3**q+D+carry, 3**q)
        actual = residue(c*X+beta, 3**(v+q))//3**v
        assert carry in (0, 1) and actual == predicted
        affine += 1
    return {'all_assertions_passed': True,
            'restricted_alphabet_maximal_partner_checks': capacity,
            'capacity_maxima': maxima,
            'affine_exact_rational_identities': affine,
            'limitations': 'Finite tests complement the proofs; not formal verification.'}


if __name__ == '__main__':
    report = run()
    (HERE/'REFINEMENT_CHECKS.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
