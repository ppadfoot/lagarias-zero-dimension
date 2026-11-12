"""Independent exact finite checks of the arbitrary-coefficient coding."""
from itertools import product
from pathlib import Path
import json
import random

RNG = random.Random(60320261112)


def F(r):
    d = r % 3
    return (r-d)//3 + (d == 2)


def predictor(r, a, k, u):
    t = F(r)+3**(k-1)*u*a
    for _ in range(k-1):
        t = F(t)
    return t % 3


def code(w, k, u):
    r = 0
    out = []
    carries = [r]
    predicted = []
    for a in w:
        d = r % 3
        assert (d+a) % 3 in (0, 1)
        p = predictor(r, a, k, u)
        predicted.append(p)
        if d:
            b = 0
        else:
            p0, p1 = predictor(r, 0, k, u), predictor(r, 1, k, u)
            assert (p1-p0) % 3 == u % 3
            b = a if p0 and p1 else int(p != 0)
        out.append(b)
        r = F(r)+3**(k-1)*u*a
        carries.append(r)
    for j in range(len(w)-k):
        assert predicted[j] == carries[j+k] % 3
        assert not (out[j] == out[j+k] == 1)
    return tuple(out)


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a


def good(x, L):
    for _ in range(L):
        x, d = divmod(x, 3)
        if d == 2:
            return False
    return True


def run():
    checked_words = 0
    checked_parameters = 0
    zero_family_cases = 0
    for L in range(1, 10):
        ws = list(product((0, 1), repeat=L))
        xs = [sum(a*3**j for j, a in enumerate(w)) for w in ws]
        for k in range(1, 6):
            # Long positive and negative coefficient strings exercise prefixes
            # beyond L, while the proof handles the infinite strings.
            us = [1, 2, -1, -2]
            us += [RNG.choice([-1, 1])*RNG.randrange(1, 3**(L+k+4))
                   for _ in range(25)]
            for u in us:
                if u % 3 == 0:
                    continue
                lam = 1+3**k*u
                words = [w for w, x in zip(ws, xs) if good(lam*x, L)]
                outputs = [code(w, k, u) for w in words]
                assert len(set(outputs)) == len(outputs)
                bound = 1
                for a in range(k):
                    chain = len(range(a, L, k))
                    bound *= fib(chain+2)
                assert len(words) <= bound
                if u == -1:
                    polynomial_count = 1
                    for a in range(k):
                        polynomial_count *= len(range(a, L, k))+1
                    assert len(words) == polynomial_count
                    for w in words:
                        assert all(w[j] <= w[j+k] for j in range(L-k))
                    zero_family_cases += 1
                checked_words += len(words)
                checked_parameters += 1
    result = {'all_assertions_passed': True,
              'parameter_length_cases': checked_parameters,
              'admissible_word_encodings': checked_words,
              'negative_multiplier_exact_count_cases': zero_family_cases,
              'checks': ['predictor of delayed restriction',
                         'different free branches get different output bits',
                         'injectivity at finite prefix lengths',
                         'absence of two output ones at distance k',
                         'Fibonacci product prefix bound'],
              'limitation': 'Finite independent audits; the arbitrary Z_3 proof is analytic.'}
    return result


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('A03_CODING_CHECKS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
