#!/usr/bin/env python3
"""Exact finite checks for the analytic positive-density section.

Author: Timofei Iuzhakov.
Python standard library only. No archived data, floating point, network,
or asymptotic extrapolation. These checks are not used to prove density.
Run from any directory; output is written next to this script.
"""
import argparse
from collections import deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def cantor_fraction(a, d):
    """Exact membership in real C for 0<a<d, gcd(d,3)=1."""
    assert 0 < a < d and d % 3
    seen = set()
    while a not in seen:
        seen.add(a)
        digit, a = divmod(3 * a, d)
        if digit == 1:
            return False
        assert a != 0
    return True


def graph(M):
    assert M > 1 and M % 3 == 1
    edges = {}
    todo = deque([0])
    seen = {0}
    while todo:
        c = todo.popleft()
        row = []
        for a in (0, 1):
            for b in (0, 1):
                z = c + M * a - b
                if z % 3 == 0:
                    cp = z // 3
                    assert 0 <= 2 * cp < M
                    row.append((a, b, cp))
                    if cp not in seen:
                        seen.add(cp)
                        todo.append(cp)
        assert len(row) == (2 if c % 3 == 0 else 1)
        edges[c] = row
    return edges


def reach(edges, start):
    seen = {start}
    todo = [start]
    while todo:
        c = todo.pop()
        for _, _, cp in edges[c]:
            if cp not in seen:
                seen.add(cp)
                todo.append(cp)
    return seen


def components(edges):
    # Deliberately simple independent transitive-closure method at small M.
    closures = {c: reach(edges, c) for c in edges}
    unseen = set(edges)
    result = []
    while unseen:
        c = min(unseen)
        comp = {d for d in unseen if d in closures[c] and c in closures[d]}
        result.append(comp)
        unseen -= comp
    return result


def branch_positive(edges, comps):
    return any(sum(cp in comp for _, _, cp in edges[c]) >= 2
               for comp in comps for c in comp)


def integer_cantor(x):
    while x:
        x, r = divmod(x, 3)
        if r == 2:
            return False
    return True


def factor(n):
    ans = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                e += 1
                n //= p
            ans.append((p, e))
        p += 1
    if n > 1:
        ans.append((n, 1))
    return ans


def order3(n):
    assert n >= 2 and n % 3
    x, k = 3 % n, 1
    while x != 1:
        x = 3 * x % n
        k += 1
    return k


def carmichael(n):
    ans = 1
    for p, e in factor(n):
        v = 2 ** (e - 2) if p == 2 and e >= 3 else (p - 1) * p ** (e - 1)
        ans = lcm(ans, v)
    return ans


def run(proof):
    denominators, rational_checks = [], 0
    for d in range(2, 601):
        if not d % 3:
            continue
        good = False
        for a in range(1, d):
            if gcd(a, d) == 1:
                rational_checks += 1
                good |= cantor_fraction(a, d)
        if good:
            denominators.append(d)
    odd = [d for d in denominators if d % 2]
    graphs, zero, sifted, positive = 0, [], [], []
    for M in range(4, 601, 3):
        E = graph(M)
        comps = components(E)
        pos = branch_positive(E, comps)
        graphs += 1
        if pos:
            positive.append(M)
        else:
            zero.append(M)
            terminal = [S for S in comps
                        if all(cp in S for c in S for _, _, cp in E[c])]
            assert terminal
            for S in terminal:
                assert all(c % 3 and len(E[c]) == 1 for c in S)
                assert all(cantor_fraction(2 * c + 1, M + 1) for c in S)
        q = M + 1
        if q % 6 == 5 and not any(q % d == 0 for d in odd):
            # All possible divisors <=q have already been classified.
            assert not any(cantor_fraction(a, q) for a in range(1, q))
            assert pos
            sifted.append(q)
    witness_checks = 0
    D = [x for x in range(1, 3 ** 6) if integer_cantor(x)]
    for a in D:
        for b in D:
            if b % a:
                continue
            M = b // a
            # Verify block concatenation, and carry branching after removing 3's.
            assert integer_cantor(a * (1 + 3 ** 6 + 3 ** 18))
            assert integer_cantor(b * (1 + 3 ** 6 + 3 ** 18))
            unit = M
            while unit % 3 == 0:
                unit //= 3
            if unit > 1:
                E = graph(unit)
                assert branch_positive(E, components(E))
            witness_checks += 1
    product_checks = 0
    for n in range(2, 5001):
        if not n % 3:
            continue
        P = 1
        for p, _ in factor(n):
            P *= order3(p)
        assert n * order3(n) >= carmichael(n) * P
        product_checks += 1
    association = []
    for k in range(1, min(6, len(odd)) + 1):
        moduli = odd[:k]
        exact = Fraction(0)
        for j in range(k + 1):
            for S in combinations(moduli, j):
                exact += Fraction((-1) ** j, lcm(*S) if S else 1)
        lower = Fraction(1)
        for d in moduli:
            lower *= Fraction(d - 1, d)
        assert exact >= lower > 0
        association.append({"moduli": moduli, "density_without_1_over_6": str(exact),
                            "product_lower_bound": str(lower)})
    return {
        "status": "PASS",
        "scope": "Finite exact consistency checks only; no numerical density or tail claim",
        "rational_membership_checks": rational_checks,
        "denominators_up_to_600": denominators,
        "carry_graphs": graphs,
        "zero_dimensional_graphs": zero,
        "sifted_q_up_to_600": sifted,
        "finite_witness_block_checks": witness_checks,
        "order_product_checks": product_checks,
        "finite_association_checks": association,
        "source_sha256": {p.name: sha256(p.read_bytes()).hexdigest()
                          for p in (proof, Path(__file__).resolve())},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proof", type=Path,
                        default=HERE / "positive_density_section.tex")
    parser.add_argument("--output", type=Path,
                        default=HERE / "positive_density_checks.json")
    args = parser.parse_args()
    result = run(args.proof)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k in {"status", "rational_membership_checks", "carry_graphs",
                               "finite_witness_block_checks", "order_product_checks"}},
                     sort_keys=True))
