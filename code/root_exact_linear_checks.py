"""Exact adversarial checks of the Monge/Cramer bridges; not a proof substitute."""
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import json
import random


def valuation(a):
    a = Fraction(a)
    if not a:
        return float('inf')
    n, d = abs(a.numerator), a.denominator
    result = 0
    while n % 3 == 0:
        result += 1
        n //= 3
    while d % 3 == 0:
        result -= 1
        d //= 3
    return result


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    result = Fraction(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        value = a[j][j]
        result *= value
        for i in range(j + 1, len(a)):
            ratio = a[i][j] / value
            for k in range(j + 1, len(a)):
                a[i][k] -= ratio * a[j][k]
    return result


def main():
    rng = random.Random(40620261106)
    minors = cramer = zero_errors = 0
    for d in range(1, 6):
        for trial in range(12):
            q = 1 + trial % 4
            # Coordinate growth order deliberately differs from exponent order.
            slopes = [0] + rng.sample([v for v in range(-9, 10) if v], d - 1)
            exponents = [[200 * t + slopes[t] * i for t in range(d)]
                         for i in range(d + 2)]
            for row in exponents:
                assert row[0] == 0
                assert all(row[t + 1] - row[t] >= q for t in range(d - 1))
            for t, s in combinations(range(d), 2):
                assert len({row[t] - row[s] for row in exponents}) == len(exponents)
            for indices in combinations(range(d + 2), d):
                selected = [exponents[i] for i in indices]
                matrix = [[3 ** e for e in row] for row in selected]
                costs = [sum(selected[i][p[i]] for i in range(d))
                         for p in permutations(range(d))]
                minimum = min(costs)
                assert costs.count(minimum) == 1
                denominator = determinant(matrix)
                assert valuation(denominator) == minimum
                minors += 1
                errors = [0 if (trial + i) % 5 == 0 else
                          rng.choice([-5, -2, -1, 1, 2, 4, 5]) *
                          3 ** (max(row) + q + rng.randrange(5))
                          for i, row in enumerate(selected)]
                for t in range(d):
                    changed = [row[:] for row in matrix]
                    for i, error in enumerate(errors):
                        changed[i][t] = error
                    correction = determinant(changed) / denominator
                    assert valuation(correction) >= q
                    zero_errors += not bool(correction)
                    cramer += 1
    # Direct finite-field capacity check for any number of factors: once two
    # nonsingletons are present, their sum already fills F3.
    subsets = [{i for i in range(3) if mask & (1 << i)} for mask in range(1, 8)]
    capacity_pairs = 0
    for a in subsets:
        for b in subsets:
            total = {(x + y) % 3 for x in a for y in b}
            if len(total) <= 2:
                assert len(a) * len(b) <= 2
            capacity_pairs += 1
    result = dict(status='PASS', exact_monomial_minors=minors,
                  exact_cramer_corrections=cramer,
                  zero_corrections_explicitly_allowed=zero_errors,
                  finite_field_capacity_pairs=capacity_pairs,
                  seed=40620261106,
                  scope='Finite exact consistency checks, not the Ramsey/ESS proof.')
    destination = Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
