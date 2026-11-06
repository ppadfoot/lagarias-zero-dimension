# Verification scope

The proof was reviewed along three separate lines:

1. **Arithmetic and unit equations:** nondegeneracy, extraction of separated templates, approximation by integer coefficients, the true-visit anchor, countability of covering data, and exact carries.
2. **Finite causal containers:** full-origin multiplicity, source branches, all-rank recording, projection queues, lifetime charging, retirement, complete Cartesian products, and reconstruction from the final fingerprint.
3. **Entropy and dimension:** conditional supports, Kneser capacity, incidence deficits, overlapping windows, countable compact covers, and the order of limits giving packing dimension zero.

Each reviewer also read the complete final English source. Exact source hashes and the scope of each conclusion appear in the `*_final_review.txt` files. The source-stage reports retain their original local references.

## Finite programs

| Program | Scope |
| --- | --- |
| `check_arithmetic.py` | 4,800 carry identities; 4,800 finite anchor/approximation cases; 262 low residues; 78,768 distinct-valuation subsums; 600 template configurations |
| `check_local_identities.py` | General carry and two-target identities, coset occupancy, and boundary multiplicities from the archived Stage 16 tests |
| `check_entropy_transfer.py` | 17,220 entropy diagnostics and 2,640 boundary instances; negative control showing why actual tuples alone do not imply full-product compatibility |
| `upstream_container_engine.py` | Eight finite fixtures; origin and queue invariants; 1,600 complete fingerprint replays |
| `check_nonlocal_replay.py` | All 2,339 feasible words of five specified models with deliberately nonlocal joint letters; measurability, conditional supports, and full products |
| `check_nonvacuous_budget.py` | Latin-square triple system: N=3,072, 1,048,576 edges, theta=1/2, predicted bad-edge bound 768,000, actual fingerprint size 5 and zero bad edges |

The arithmetic, set, and container checks use exact integer/rational operations. The entropy diagnostic uses floating-point logarithms with explicit tolerances; its analytic inequalities are proved in the paper. The container engine was copied from the historical Stage 12 verification code, inspected, and independently rerun. The new nonlocal and nonvacuous tests add independent checks around that implementation.

Many small stress fixtures use thresholds for which the entropy bound is vacuous; they exercise queue and charging paths. The separate million-edge fixture verifies a genuinely nonvacuous parameter choice. None of these finite computations establishes the universal lemma by extrapolation.

The external unit-equation theorem and Kneser's theorem are cited mathematical inputs. They are not re-proved or formally checked by these programs. No Lean/Coq/Isabelle certificate or external journal review is included.
