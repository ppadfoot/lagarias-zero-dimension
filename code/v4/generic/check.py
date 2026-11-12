"""Exact finite audits of identities used in PROOF_RU.txt.

The infinite theorem is analytic; finite checks are not a replacement for it.
Run with Python 3 and NumPy. The JSON report is written beside this script.
"""

from fractions import Fraction
from pathlib import Path
import json
import numpy as np


def sigma(n):
    result = np.array([0], dtype=np.int64)
    for j in range(n):
        result = np.concatenate((result, result + 3**j))
    return result


def rational(x):
    return str(x)


def main():
    report = {
        "scope": "Exact finite identities, not a proof by numerical extrapolation",
        "levels": [],
        "block_geometry": [],
        "positivity_coding": [],
    }
    all_q = {}
    previous_counts = None
    for n in range(1, 8):
        modulus = 3**n
        points = sigma(n)
        units = points[points % 3 == 1]
        allowed = np.zeros(modulus, dtype=bool)
        allowed[points] = True
        second_sum = 0
        unit_sum = 0
        counts = {}
        q_values = {}
        minimum = 2**n
        maximum = 0
        for lam in range(1, modulus, 3):
            affine = (points[:, None] - lam * points[None, :]) % modulus
            r = np.bincount(affine.ravel(), minlength=modulus)
            assert int(r.sum()) == 4**n
            assert 1 <= int(r.min()) <= int(r.max()) <= 2**n
            minimum = min(minimum, int(r.min()))
            maximum = max(maximum, int(r.max()))
            second_sum += int(np.dot(r, r))
            qn = int(allowed[(lam * units) % modulus].sum())
            q_values[lam] = qn
            unit_sum += qn
            # Exact full-prefix identity, including arbitrarily many initial zeros.
            expected_full = 1 + qn + sum(
                all_q[j][lam % (3**j)] for j in range(1, n)
            )
            assert int(r[0]) == expected_full
            if previous_counts is not None:
                low_modulus = 3 ** (n - 1)
                # This is precisely E(D_n | beta mod3^(n-1)) = D_(n-1).
                assert np.array_equal(
                    r.reshape(3, low_modulus).sum(axis=0),
                    4 * previous_counts[lam % low_modulus],
                )
            counts[lam] = r
        slopes = 3 ** (n - 1)
        actual_second = Fraction(3**n * second_sum, 16**n * slopes)
        expected_second = Fraction(3, 2) - Fraction(1, 2) * Fraction(3, 4)**n
        actual_first = Fraction(unit_sum, slopes)
        expected_first = Fraction(4, 3) ** (n - 1)
        assert actual_second == expected_second
        assert actual_first == expected_first
        report["levels"].append({
            "n": n,
            "all_slopes_1_mod_3": slopes,
            "affine_pairs_counted": slopes * 4**n,
            "min_R": minimum,
            "max_R": maximum,
            "mean_squared_L2": rational(actual_second),
            "predicted_squared_L2": rational(expected_second),
            "mean_unit_prefix_count": rational(actual_first),
            "martingale_consistency": True,
            "full_prefix_identity": True,
        })
        all_q[n] = q_values
        previous_counts = counts

    # Exhaustive local audit of the fresh-parameter permutation and block equation.
    for m, j in [(1, 1), (1, 3), (2, 2), (2, 3), (3, 3)]:
        low_modulus, block_modulus = 3**j, 3**m
        low_sigma, block_sigma = sigma(j), sigma(m)
        low_allowed = set(map(int, low_sigma))
        block_allowed = set(map(int, block_sigma))
        tested_prefixes = tested_extensions = 0
        for low_lam in range(1, low_modulus, 3):
            ell = low_lam % block_modulus
            for prefix0 in low_sigma:
                prefix = int(prefix0)
                if prefix % 3 != 1 or (low_lam * prefix) % low_modulus not in low_allowed:
                    continue
                tested_prefixes += 1
                shifts = []
                for fresh in range(block_modulus):
                    lam = low_lam + low_modulus * fresh
                    low_out = (lam * prefix) % low_modulus
                    beta = ((lam * prefix - low_out) // low_modulus) % block_modulus
                    shifts.append(beta)
                    expected_beta = (low_lam * prefix // low_modulus + fresh * prefix) % block_modulus
                    assert beta == expected_beta
                    admitted = 0
                    for z0 in block_sigma:
                        z = int(z0)
                        full_input = prefix + low_modulus * z
                        out_block = (lam * full_input // low_modulus) % block_modulus
                        assert out_block == (ell * z + beta) % block_modulus
                        admitted += int(out_block in block_allowed)
                        tested_extensions += 1
                    assert admitted >= 1
                assert sorted(shifts) == list(range(block_modulus))
        report["block_geometry"].append({
            "m": m, "j": j,
            "admissible_unit_prefixes": tested_prefixes,
            "tested_extensions": tested_extensions,
            "fresh_shift_is_permutation": True,
            "exact_block_equation": True,
        })

    # Check finite versions of the nonstandard digit coding in the positivity lemma.
    # Includes lambda=1: the conditional positivity lemma is meaningful even though
    # absolute continuity fails at that particular parameter.
    for lam in [1, 4, 7, 10, 28, -2, -8, -26]:
        digits = [0, 1, -lam]
        for n in range(1, 7):
            modulus = 3**n
            residues = np.array([0], dtype=np.int64)
            for j in range(n):
                residues = np.concatenate([residues + 3**j * d for d in digits])
            residues %= modulus
            assert len(np.unique(residues)) == modulus
            if n >= 2:
                # T deletes the first custom digit, just as in equation (13).
                for z0 in residues:
                    z = int(z0)
                    r = z % 3
                    nxt = (z - digits[r]) // 3
                    assert (z - (digits[r] + 3 * nxt)) % modulus == 0
        report["positivity_coding"].append({"lambda": lam, "max_n": 6, "bijection": True})

    report["status"] = "all_exact_checks_passed"
    target = Path(__file__).with_name("EXACT_CHECKS.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "report": str(target.resolve())}))


if __name__ == "__main__":
    main()
