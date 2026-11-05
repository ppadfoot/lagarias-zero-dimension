#!/usr/bin/env python3
"""Finite regression checks for Stage16. The theorems are proved analytically.

No ordinary exponent search, conjecture certification, or numerical
substitute for the causal-container proof is performed here.
"""
from pathlib import Path
from collections import Counter
import argparse
import json
import random
import time


def check_ordinary_carry():
    rng = random.Random(40616)
    cases = 0
    attained = set()
    for p in (2, 3, 5):
        for r in range(3, 8):
            for k in (1, 2, 4):
                b = 1
                while p**b <= r - 1:
                    b += 1
                q = b + k
                offsets = [(t + 1)*q for t in range(r - 2)]
                terminal = (r - 1)*q
                for j in (0, 1, 3):
                    v = j + terminal
                    modulus = p**q
                    for _ in range(24):
                        x = rng.randrange(p**(v + q + 2))
                        coeff = []
                        for _ in offsets:
                            a = 0
                            while a % p == 0:
                                a = rng.randrange(-2*p**q, 2*p**q)
                            coeff.append(a)
                        u = 0
                        while u % p == 0:
                            u = rng.randrange(-p**q, p**q)
                        d = rng.randrange(-p**(v + q), p**(v + q))
                        rows = [a*x for a in coeff]
                        prefix = x % p**j
                        t = d + p**terminal*u*prefix
                        low_t = t % p**v
                        center = (t - low_t)//p**v
                        low_parts = [x % p**v, low_t]
                        low_parts += [p**e*(y % p**(v-e))
                                      for e, y in zip(offsets, rows)]
                        assert len(low_parts) == r
                        assert all(0 <= z < p**v for z in low_parts)
                        carry = sum(low_parts)//p**v
                        assert 0 <= carry <= r-1
                        c = 1 + sum(a*p**e for a,e in zip(coeff,offsets)) + u*p**terminal
                        output_window = ((c*x+d)//p**v) % modulus
                        lhs = u*((x//p**j) % modulus) + (x//p**v) % modulus
                        lhs += sum((y//p**(v-e)) % modulus for e,y in zip(offsets,rows))
                        lhs += center + carry
                        assert lhs % modulus == output_window
                        attained.add((p,r,carry))
                        cases += 1
    return {'cases':cases,'primes':[2,3,5],
            'includes_negative_coefficients_and_centers':True,
            'distinct_attained_prime_arity_carry_triples':len(attained)}


def check_two_upper_translates():
    cases = 0
    two_lifts = 0
    for p in (2,3,5):
        for b in (1,2,3):
            base = p**b
            for m in sorted({1,base//2,base-1}):
                for residue in range(base):
                    lifts = {(low-e-residue)//base
                             for low in range(base) for e in range(m+1)
                             if (low-e-residue) % base == 0}
                    assert len(lifts) <= 2
                    if len(lifts) == 2:
                        assert max(lifts)-min(lifts) == 1
                        two_lifts += 1
                    cases += 1
    return {'low_residue_cases':cases,'cases_attaining_two_lifts':two_lifts,
            'tests_extreme_allowed_carry_p_to_b_minus_one':True}


def words(p, forbidden, length):
    out = []
    for n in range(p**length):
        d = [(n//p**j) % p for j in range(length)]
        if all(tuple(d[j:j+len(forbidden)]) != forbidden
               for j in range(length-len(forbidden)+1)):
            out.append(n)
    return out


def check_coset_occupancy():
    cases = 0
    records = []
    for p, forbidden, depth in ((2,(0,0),8),(3,(0,1,2),6),(3,(2,),7)):
        language = [words(p,forbidden,h) for h in range(depth+1)]
        for k in range(depth+1):
            for h in range(k+1):
                low_modulus = p**(k-h)
                # Translations permute these residue classes, so all z are covered.
                counts = Counter(n % low_modulus for n in language[k])
                assert max(counts.values(),default=0) <= len(language[h])
                cases += 1
        records.append({'p':p,'forbidden_word_low_to_high':list(forbidden),
                        'maximum_depth':depth,'language_counts':[len(a) for a in language]})
    return {'coset_class_checks':cases,'targets':records,
            'includes_nonproduct_languages':True}


def check_entropy_boundaries():
    cases = 0
    for b in range(1,9):
        for k in range(1,13):
            for length in range(b+k,b+k+40):
                n = length-b-k+1
                multiplicities = [0]*length
                for i in range(n):
                    for t in range(i+b,i+b+k):
                        multiplicities[t] += 1
                assert max(multiplicities) <= k
                assert sum(multiplicities) == k*n
                assert sum(k-m for m in multiplicities) == k*(b+k-1)
                for span in (0,1,n-1,n,n+3):
                    starts = max(n-span,0)
                    assert n-starts == min(span,n)
                cases += 1
    return {'block_length_cases':cases,'includes_shorter_than_two_blocks':True,
            'edge_span_cases_per_block_case':5}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    checks=[]
    for name,fn in [('ordinary_carry',check_ordinary_carry),
                    ('two_upper_translates',check_two_upper_translates),
                    ('subshift_coset_occupancy',check_coset_occupancy),
                    ('overlap_and_short_interval_boundary',check_entropy_boundaries)]:
        started=time.monotonic()
        details=fn()
        checks.append({'name':name,'status':'PASS',
                       'elapsed_seconds':round(time.monotonic()-started,4),**details})
    result={'status':'PASS','checks':checks,'ordinary_exponent_interval_scans':0,
            'previous_stage_scans_rerun':False,
            'scope':'Finite regression checks only; mathematical proofs are in the report.',
            'not_proved_by_this_program':['The general recurrence theorem','Countability of E2',
                                         '1 not in E2','E2={0}','Exact list 1,4,256']}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
