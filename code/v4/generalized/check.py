"""Finite exact-arithmetic audits; these do not prove the dimension theorem."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import math
import random

HERE = Path(__file__).resolve().parent
RNG = random.Random(40620261112)


def sigma(q):
    return {sum(a * 3**j for j, a in enumerate(w))
            for w in product((0, 1), repeat=q)}


def residue(x, modulus):
    x = Fraction(x)
    return (x.numerator * pow(x.denominator, -1, modulus)) % modulus


def capacity_audit():
    total = 0
    maxima = {}
    # Given A, the largest possible B is the intersection of target-a.
    # Thus all A below also check every nonempty subset B of that intersection.
    for q in (1, 2):
        m = 3**q
        for adjacent in (False, True):
            base = sigma(q)
            if adjacent:
                base |= {(a + 1) % m for a in base}
            bound = 9 * 2**(q-1) if adjacent else 2**q
            max_product = 0
            for z in range(m):
                target = {(a + z) % m for a in base}
                for mask in range(1, 1 << m):
                    A = [a for a in range(m) if mask >> a & 1]
                    B = set(range(m))
                    for a in A:
                        B &= {(t-a) % m for t in target}
                    value = len(A) * len(B)
                    assert value <= bound, (q, z, A, B)
                    max_product = max(max_product, value)
                    total += 1
            maxima[f'q{q}_adjacent{int(adjacent)}'] = max_product
    # More levels: exhaustive small A and reproducible larger random A.
    for q in (3, 4, 5):
        m = 3**q
        candidates = ([set(a) for k in (1, 2, 3)
                       for a in combinations(range(m), k)] if q == 3 else [])
        candidates += [set(RNG.sample(range(m), RNG.randint(1, min(35, m))))
                       for _ in range(1500)]
        for adjacent in (False, True):
            base = sigma(q)
            if adjacent:
                base |= {a+1 for a in base}
            bound = 9 * 2**(q-1) if adjacent else 2**q
            for A in candidates:
                z = RNG.randrange(m)
                target = {(t+z) % m for t in base}
                B = set(range(m))
                for a in A:
                    B &= {(t-a) % m for t in target}
                assert len(A) * len(B) <= bound
                total += 1
    return {'maximal_partner_checks': total, 'small_exhaustive_maxima': maxima,
            'exhaustive_all_subsets_levels': [1, 2],
            'higher_levels': 'all |A|<=3 at q=3; seeded random at q=3,4,5'}


def arithmetic_audit():
    total = 0
    carries = Counter()
    for _ in range(12000):
        q, E, j = RNG.randint(1, 6), RNG.randint(1, 8), RNG.randint(0, 8)
        L = j+E+q
        X = RNG.randrange(3**L)
        numerator = RNG.choice([a for a in range(-35, 36) if a % 3])
        denominator = RNG.choice([a for a in range(1, 20) if a % 3])
        u = Fraction(numerator, denominator)
        c = 1+3**E*u
        v = j+E
        P = X % 3**j
        tj = 3**E*u*P
        tv = residue(tj, 3**v)
        D = (tj-tv)/3**v
        e = ((X % 3**v)+tv)//3**v
        source = (X//3**j) % 3**q
        end = (X//3**v) % 3**q
        actual = (residue(c*X, 3**L)//3**v) % 3**q
        predicted = residue(u*source+end+D+e, 3**q)
        assert e in (0, 1) and actual == predicted
        carries[e] += 1
        total += 1
    return {'exact_rational_window_identities': total, 'carry_frequencies': dict(carries)}


def palette(word, letters, edges, relation, Q, threshold):
    n = len(letters)
    palettes = [set(range(Q)) for _ in range(n)]
    assigned = []
    fingerprint = []
    outgoing = defaultdict(list)
    for j, k in edges:
        outgoing[j].append(k)
    for j in range(n):
        light = set()
        for a in palettes[j]:
            bad = sum(any(not relation(j, k, word[:j], a, b) for b in palettes[k])
                      for k in outgoing[j])
            if bad < threshold:
                light.add(a)
        z = letters[j]
        assert z in palettes[j]
        if z in light:
            assigned.append(light)
        else:
            fingerprint.append((j, z))
            assigned.append({z})
            for k in outgoing[j]:
                palettes[k] = {b for b in palettes[k]
                               if relation(j, k, word[:j], z, b)}
                assert letters[k] in palettes[k]
    bad_edges = sum(any(not relation(j, k, word[:j], a, b)
                        for a in assigned[j] for b in assigned[k])
                    for j, k in edges)
    assert len(fingerprint)*threshold <= Q*n
    assert bad_edges <= Q*threshold*n
    return tuple(fingerprint), assigned


def container_audit():
    # Random finite word families. Relations are generated from those families,
    # ensuring admissibility but allowing arbitrary prefix dependence and
    # completely nonlocal letter maps. Replay is checked by grouping (prefix,F).
    runs = 0
    heavy = 0
    for scenario in range(30):
        L = 12
        Q = 2 if scenario % 2 else 4
        words = RNG.sample(list(product((0, 1), repeat=L)), 35)
        zmap = {w: [RNG.randrange(Q) for _ in range(L)] for w in words}
        edges = list(combinations(range(L), 2))
        allowed = defaultdict(set)
        for w in words:
            for j, k in edges:
                allowed[j, k, w[:j]].add((zmap[w][j], zmap[w][k]))
        def relation(j, k, prefix, a, b):
            return (a, b) in allowed[j, k, prefix]
        for threshold in (1, 2, 4, 8):
            groups = {}
            for w in words:
                F, assigned = palette(w, zmap[w], edges, relation, Q, threshold)
                heavy += len(F)
                for j in range(L):
                    key = (j, w[:j], F)
                    value = frozenset(assigned[j])
                    assert groups.setdefault(key, value) == value
                runs += 1
    return {'finite_family_word_runs': runs, 'heavy_source_records': heavy,
            'checks': ['truth preservation', 'fingerprint size',
                       'full-product bad-edge bound', 'prefix/fingerprint replay'],
            'note': 'Algorithm is checked also at small positive thresholds; entropy theorem uses T>=2Q.'}


def tree_extract(numbers):
    groups = defaultdict(list)
    for x in numbers:
        groups[x % 3].append(x)
    group = max(groups.values(), key=len)
    selected = []
    depth = 1
    while len(group) > 1:
        sub = defaultdict(list)
        for x in group:
            sub[(x//3**depth) % 3].append(x)
        best = max(sub, key=lambda z: len(sub[z]))
        if len(sub) > 1:
            other = next(z for z in sub if z != best)
            selected.append((depth, sub[other][0]))
        group = sub[best]
        depth += 1
    anchor = group[0]
    for depth, x in selected:
        d = x-anchor
        actual = 0
        while d % 3 == 0:
            actual += 1
            d //= 3
        assert actual == depth
    return selected


def extraction_and_lower_audit():
    extraction_runs = 0
    for K in range(1, 5):
        J = 2*3**(K-1)+1
        for _ in range(100):
            pool = set()
            while len(pool) < J:
                n = RNG.randrange(1, 10**12)
                if n % 3:
                    pool.add(n)
            selected = tree_extract(pool)
            assert len(selected) >= K
            extraction_runs += 1
    lower_checks = 0
    for L in range(1, 14):
        U = [sum(a*3**(2*j) for j, a in enumerate(w))
             for w in product((0, 1), repeat=(L+1)//2)]
        assert len(U) == 2**((L+1)//2)
        good = sigma(L)
        for x in U:
            for k in range(5):
                assert ((1+3**(2*k+1))*x) % 3**L in good
                lower_checks += 1
    return {'finite_tree_extractions': extraction_runs,
            'known_lower_construction_checks': lower_checks}


if __name__ == '__main__':
    results = {'date': '2026-11-12', 'all_assertions_passed': True,
               'capacity': capacity_audit(), 'arithmetic': arithmetic_audit(),
               'causal_palettes': container_audit(),
               'extraction_and_lower': extraction_and_lower_audit(),
               'exact_dimension_decimal': math.log(2)/(2*math.log(3)),
               'limitations': 'Finite audits; no independent review or formal verification.'}
    (HERE/'CHECKS.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))
