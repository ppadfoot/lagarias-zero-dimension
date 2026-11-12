"""Exact checks of the new affine periodic-target bridge; not a dimension proof."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def floor(x):
    return x.numerator // x.denominator


def frac(x):
    return x - floor(x)


def residue(x, modulus):
    assert x.denominator % 3
    return x.numerator * pow(x.denominator, -1, modulus) % modulus


def sigma(word, length):
    for _ in range(length):
        word, digit = divmod(word, 3)
        if digit == 2:
            return False
    return word == 0


def in_periodic_cantor(x):
    x = frac(x)
    seen = set()
    while x not in seen:
        seen.add(x)
        x *= 3
        digit = floor(x)
        if digit == 2:
            return False
        x -= digit
    return True


def bridge(y, c, d, length):
    modulus = 3**length
    t_integer = floor(modulus*y)
    v_integer = floor(modulus*(c*y+d))
    shift_integer = floor(modulus*d)
    u = t_integer % modulus
    delta = F(v_integer) - c*t_integer - shift_integer
    theta = frac(modulus*d)
    assert delta == c*frac(modulus*y) + theta - frac(modulus*(c*y+d))
    assert -1 < delta < c+1
    assert (delta*c.denominator).denominator == 1
    beta = shift_integer + delta
    assert beta.denominator % 3
    assert residue(c*u+beta, modulus) == v_integer % modulus
    admissible = in_periodic_cantor(y) and in_periodic_cantor(c*y+d)
    if admissible:
        assert sigma(u, length)
        assert sigma(residue(c*u+beta, modulus), length)
    return admissible


def main():
    tails = {F(0), F(1, 2)}
    for width in range(1, 5):
        for digits in product((0, 1), repeat=width):
            word = sum(d*3**j for j, d in enumerate(digits))
            tails.add(F(word, 3**width))
            tails.add(F(word, 3**width-1))
    # Include both admissible inputs and inputs with a forbidden digit.
    ys = sorted({F(a)+t for a in (-2, 0, 2) for t in tails} |
                {F(-1, 3), F(2, 3), F(5, 9), F(11, 7)})
    cs = [F(1, 16), F(1, 4), F(1, 2), F(1), F(2), F(4), F(16), F(5, 7)]
    ds = [F(-7, 3), F(-1, 4), F(0), F(1, 3), F(5, 9), F(7, 8)]
    checked = admissible = 0
    for y, c, d, length in product(ys, cs, ds, range(1, 7)):
        admissible += bridge(y, c, d, length)
        checked += 1

    # Check the finite residual-alphabet size independently of the proof text.
    for c in cs:
        p, q = c.numerator, c.denominator
        alphabet = [F(i, q) for i in range(-q+1, p+q)]
        assert len(alphabet) == p+2*q-1
        assert all(-1 < x < c+1 and x.denominator % 3 for x in alphabet)

    # A fixed shift across all depths is not valid, even at admissible points.
    old_shifts = set()
    for length in range(1, 7):
        m = 3**length
        old_shifts.add(F(floor(m*F(1, 8)))-F(1, 4)*floor(m*F(1, 2)))
    assert old_shifts == {F(-1, 4), F(0)}

    # Removing the large integer shift D loses the congruence.
    m = 27
    assert residue(F(0), m) != floor(m*F(1, 3)) % m
    # Omitting theta from (3.1) fails when 3^L d is not integral.
    y, c, d, length = F(1, 2), F(1, 4), F(1, 4), 1
    m = 3**length
    actual = F(floor(m*(c*y+d))) - c*floor(m*y) - floor(m*d)
    erroneous = c*frac(m*y)-frac(m*(c*y+d))
    assert actual != erroneous
    # An integer-part restriction cannot replace the fractional restriction.
    assert sigma(floor(F(2, 3)), 1) and not in_periodic_cantor(F(2, 3))

    # Circle all-digit corollary: halve a point of 2K and split by integer parity.
    parity_checks = 0
    for z, integer in product(tails, range(-3, 5)):
        if z == F(1, 2):
            continue  # 2z=1 is the identified endpoint, treated separately.
        y = z+F(integer, 2)
        assert in_periodic_cantor(y-F(integer % 2, 2))
        parity_checks += 1

    result = {
        "status": "passed",
        "exact_bridge_checks": checked,
        "admissible_input_and_output_checks": admissible,
        "parity_checks": parity_checks,
        "input_count": len(ys),
        "slopes": [str(c) for c in cs],
        "offsets": [str(d) for d in ds],
        "depths": [1, 6],
        "incorrect_shortcuts_rejected": [
            "one shift vector for all depths",
            "discard floor(3^L d)",
            "discard fractional part of 3^L d",
            "integer-part condition implies fractional condition"
        ],
        "limits": "Finite rational checks validate identities, not the infinite dimension theorem; irrational offsets are handled by the analytic proof. No new independent agent review."
    }
    Path(__file__).with_name("CHECKS.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
