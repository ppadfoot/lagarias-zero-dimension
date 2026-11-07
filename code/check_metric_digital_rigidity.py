#!/usr/bin/env python3
"""Exact regression checks for the metric digital-rigidity section.

Author: Timofei Iuzhakov.
Python 3.9+; standard library only; no network or archived-file dependency.
This program does not prove any all-depth or measure-theoretic assertion.
It exhausts every coefficient pair and intercept at depths 1 through 4,
and checks complete prefix cubes in 27 explicitly listed parameter cases.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


def digits(m, balanced=False):
    values = [0]
    for j in range(m):
        step = 3**j
        if balanced:
            values = [x + d * step for x in values for d in (-1, 1)]
        else:
            values += [x + step for x in values]
    return values


def predicted_full_triples(m):
    modulus = 3**m
    inv2 = pow(2, -1, modulus)
    # (a,b,target scaling,balanced target length), after sign normalization.
    pairs = [(1, 1, 1, m)]
    for g in range(1, m):
        for sign in (-1, 1):
            t = (1 + sign * 3**g) % modulus
            inverse = pow(t, -1, modulus)
            pairs.extend([(t, 1, 1, g), (1, t, 1, g),
                          (inverse, inverse, inverse, g)])
    assert len({(a, b) for a, b, scale, g in pairs}) == 6*m - 5
    triples = set()
    for aa, bb, scale, g in pairs:
        for sa in (-1, 1):
            for sb in (-1, 1):
                a, b = sa*aa % modulus, sb*bb % modulus
                for p in digits(g, balanced=True):
                    c = scale*p % modulus
                    u = ((a+b-1)*inv2-c)*inv2 % modulus
                    triples.add((a, b, u))
    return triples


def check_classification():
    rows = []
    for m in range(1, 5):
        modulus = 3**m
        dd = digits(m)
        units = [a for a in range(modulus) if a % 3]
        actual = set()
        for a in units:
            for b in units:
                # Unpruned direct convolution: every pair and every target.
                histogram = [0]*modulus
                for x in dd:
                    for y in dd:
                        histogram[(a*x+b*y) % modulus] += 1
                counts = [0]*modulus
                for residue, count in enumerate(histogram):
                    if count:
                        for z in dd:
                            counts[(z-residue) % modulus] += count
                assert max(counts) <= modulus
                actual.update((a, b, u) for u, count in enumerate(counts)
                              if count == modulus)
        assert actual == predicted_full_triples(m)
        pair_count = len({(a, b) for a, b, u in actual})
        assert pair_count == 24*m-20
        assert len(actual) == 28*2**m-48
        rows.append(dict(m=m, unit_pairs=len(units)**2,
                         intercepts=len(units)**2*modulus,
                         full_pairs=pair_count, full_triples=len(actual)))
    return rows


def power(x, n, depth):
    modulus, order = 3**depth, 3**(depth-1)
    exponent = n.numerator*pow(n.denominator, -1, order) % order
    return pow(x, exponent, modulus)


def phi(mu, nu, n, depth):
    modulus = 3**depth
    ratio = nu*pow(mu, -1, modulus) % modulus
    return mu*power(ratio, n, depth) % modulus


def mod_fraction(x, modulus):
    return x.numerator*pow(x.denominator, -1, modulus) % modulus


def valuation(n):
    value, s = abs(n.numerator), 0
    assert value and n.denominator % 3
    while value % 3 == 0:
        value //= 3
        s += 1
    return s


def check_cubes():
    stats = dict(parameter_cases=0, cubes=0, cube_members=0,
                 shift_identities=0, descendant_checks=0, game_counts=0)
    rows = []
    parameters = [Fraction(3), Fraction(6), Fraction(9), Fraction(18),
                  Fraction(27), Fraction(-3), Fraction(-9),
                  Fraction(3, 2), Fraction(9, 2)]
    for n in parameters:
        s = valuation(n)
        for m in (1, 2, 3):
            q = m+s+1
            modulus = 3**m
            dm, ds = digits(m), digits(s)
            dm_set = set(dm)
            aq = [1+3*x for x in digits(q-1)]
            aq_set = set(aq)
            dq_set = set(digits(q))
            low_modulus = 3**(q-s)
            # Exhaustively list groups by their lower nu prefix.
            lows = [1+3*x for x in digits(q-s-1)]
            cubes = [(mu, nu0) for mu in aq for nu0 in lows
                     if phi(mu, nu0, n, q) in dq_set]
            selected = cubes[:64]
            for mu, nu0 in selected:
                rho = nu0*pow(mu, -1, 3**(m+1)) % (3**(m+1))
                aa = mod_fraction(1-n, modulus)*power(rho, n, m) % modulus
                bb = mod_fraction(n/3**s, modulus)*power(rho, n-1, m) % modulus
                assert aa % 3 and bb % 3
                value0 = phi(mu, nu0, n, q+m+1)
                uu = value0 // 3**q % modulus
                delta = (mod_fraction(n/3**s, 3**(m+1))
                         *power(rho, n-1, m+1)) % 3**(m+1)
                total = 0
                for e in ds:
                    nu = nu0+low_modulus*e
                    assert nu in aq_set and phi(mu, nu, n, q) in dq_set
                    assert nu*pow(mu, -1, 3**(m+1)) % 3**(m+1) == rho
                    assert phi(mu, nu, n, q+m+1) == (
                        value0+3**q*delta*e) % 3**(q+m+1)
                    stats['shift_identities'] += 1
                    for x in dm:
                        for y in dm:
                            child = phi(mu+3**q*x, nu+3**q*y, n, q+m)
                            direct = child // 3**q in dm_set
                            linear = (uu+bb*e+aa*x+3**s*bb*y) % modulus in dm_set
                            assert direct == linear
                            total += direct
                            stats['descendant_checks'] += 1
                    stats['cube_members'] += 1
                game = sum((uu+aa*x+bb*z) % modulus in dm_set
                           for x in dm for z in dm)
                assert total == 2**s*game
                assert game <= 3**m
                stats['cubes'] += 1
                stats['game_counts'] += 1
            stats['parameter_cases'] += 1
            rows.append(dict(N=str(n), s=s, m=m, q=q,
                             all_cubes=len(cubes), checked_cubes=len(selected)))
    assert any(row['m'] < row['s'] for row in rows)
    return stats, rows


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof', type=Path,
                        default=here/'metric_digital_rigidity.tex')
    parser.add_argument('--output', type=Path,
                        default=here/'metric_digital_rigidity_checks.json')
    args = parser.parse_args()
    classification = check_classification()
    counts, cubes = check_cubes()
    result = dict(
        author='Timofei Iuzhakov', status='PASS',
        proof_sha256=sha256(args.proof.read_bytes()).hexdigest(),
        checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        classification=classification, cube_counts=counts, cube_cases=cubes,
        scope=('Exhaustive classification for m=1,...,4. Exact complete-cube '
               'identities for 27 listed parameter cases, at most 64 groups '
               'per case. No all-depth or Haar-measure theorem is inferred '
               'from finite computation.'))
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', classification_depths=4,
                          unit_pairs=sum(row['unit_pairs'] for row in classification),
                          intercepts=sum(row['intercepts'] for row in classification),
                          cube_counts=counts)))


if __name__ == '__main__':
    main()
