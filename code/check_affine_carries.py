"""Exact regression check of the affine carry identity (not a proof certificate)."""
from fractions import Fraction
from pathlib import Path
import json
import random


def residue(x, digits):
    x = Fraction(x)
    modulus = 3 ** digits
    return (x.numerator * pow(x.denominator, -1, modulus)) % modulus


def block(x, start, width):
    return residue((Fraction(x) - residue(x, start)) / 3 ** start, width)


rng = random.Random(406)
counts = {"identities": 0, "negative_shifts": 0,
          "nonintegral_shifts": 0, "nonzero_carries": 0,
          "admissible_output_blocks": 0}
for r in (3, 4, 5):
    exponents = [2 * t for t in range(1, r - 1)]
    terminal = 2 * (r - 1)
    for _ in range(1800):
        coefficients = [rng.choice((-8, -5, -2, 1, 4, 7, 10))
                        for t in exponents]
        unit = rng.choice((Fraction(-5, 2), Fraction(-1, 4),
                           Fraction(1, 2), Fraction(7, 5)))
        beta = Fraction(rng.randrange(-40, 41), rng.choice((1, 2, 4, 5, 8)))
        source = rng.randrange(4)
        width = rng.randrange(1, 5)
        v = source + terminal
        x = rng.randrange(3 ** (v + width))
        slope = 1 + sum(a * 3 ** e for a, e in zip(coefficients, exponents))
        slope += unit * 3 ** terminal
        prefix = residue(x, source)
        t = beta + 3 ** terminal * unit * prefix
        low_t = residue(t, v)
        center = (t - low_t) / 3 ** v
        low_parts = [residue(x, v), low_t]
        low_parts += [3 ** e * residue(a * x, v - e)
                      for a, e in zip(coefficients, exponents)]
        assert len(low_parts) == r
        assert all(0 <= z < 3 ** v for z in low_parts)
        carry = sum(low_parts) // 3 ** v
        assert 0 <= carry <= r - 1
        expression = unit * block(x, source, width) + center + carry
        expression += block(x, v, width)
        expression += sum(block(a * x, v - e, width)
                          for a, e in zip(coefficients, exponents))
        actual = block(slope * x + beta, v, width)
        assert residue(expression, width) == actual
        counts["identities"] += 1
        counts["negative_shifts"] += beta < 0
        counts["nonintegral_shifts"] += beta.denominator != 1
        counts["nonzero_carries"] += carry != 0
        counts["admissible_output_blocks"] += all(
            (actual // 3 ** j) % 3 in (0, 1) for j in range(width))

result = {"status": "PASS", "seed": 406, **counts,
          "scope": "Affine causal identity for arbitrary finite inputs, including negative rational shifts; not a check of the infinite dimension theorem."}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
