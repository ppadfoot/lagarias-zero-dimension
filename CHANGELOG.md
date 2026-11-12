# Manuscript versions

Each release fixes a manuscript, its source, verification code and review record. The main README explains the results and may be updated independently of the manuscript versions.

## v4.0.0 — 12 November 2026

Same article, title, sole author and citation key `iuzhakov2026lagarias`. **54 pages.** All mathematical proof sections from v1–v3 and the causal-container appendix are retained. Three complete sections are added:

- **Section 15: exact generalized dimension.** The Hausdorff and packing dimensions of the generalized exceptional set, and the generalized nesting constant, equal one half of `log_3 2`. The matching lower bound was already known from Abram–Lagarias and Bolshakov; this version proves the upper bound, a quantitative convergence estimate, and a sharp Assouad bound for a fixed infinite common multiplier family.
- **Section 16: exact typical intersection dimension.** For Haar-almost every multiplier in `1+3 Z_3`, the Hausdorff, packing and both box dimensions of the homogeneous intersection equal `log_3(4/3)`. An all-unit isometric coding extends the golden-ratio bound, gives sharp punctured limits near the identity, and identifies the dimension of the canonical digit-fair measure.
- **Section 17: the circle question and fixed moving targets.** The fractional-part exceptional set for ternary digits 0 and 1 has zero Hausdorff and packing dimension, answering the question in §5 of Lagarias's arXiv manuscript. The standard middle-thirds target also has dimension zero. The section proves the stated fixed real and 3-adic moving-target extensions.

Five new finite verification programs are included alongside the old suite. Three independent internal cross-reviews are bound to the final English proof sources; source attribution, integration and build checks are recorded separately. These are AI-assisted internal reviews, not external peer review.

The generalized exceptional set is not the dyadic exceptional set. The typical-parameter theorem does not select a prescribed rational multiplier. Neither the pointwise assertion `1 not in E_2`, the full intersection spectrum, nor the remaining arithmetic counting problems are claimed to be solved.

[Paper](https://github.com/ppadfoot/lagarias-zero-dimension/releases/download/v4.0.0/lagarias_zero_dimension.pdf) · [Release](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v4.0.0) · [Reviews](audit/v4/README.md)

## v3.0.0 — 7 November 2026

Same article, title, sole author and citation key `iuzhakov2026lagarias`. **39 pages.** All v2 mathematical proof sections and the causal-container appendix are retained.

- Theorem 13.1: generic absence of any three nonzero visits, simultaneous in all starting points and times.
- Theorem 13.2: complete finite digital rigidity, followed by exact enumeration and a rational-height cutoff.
- Theorem 14.1: linear order of the positive-dimensional multiplier count and a linear gap from finite-integer quotients.
- Theorem 14.2: summability and quantitative tail of reduced Cantor denominators prime to 3.

The two new arguments are independent. Added portable checks, fresh section and integration reviews, a research inventory and an explicit publication checklist. The order-of-growth part of Lagarias's Problem 2 is settled; its leading density constant, the sharp finite-quotient count and E1 remain open.

[Paper](https://github.com/ppadfoot/lagarias-zero-dimension/releases/download/v3.0.0/lagarias_zero_dimension.pdf) · [Release](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v3.0.0)

## v2.0.0 — 6 November 2026

**Zero dimension for the real exceptional set and vanishing 3-adic nesting constants**  
Timofei Iuzhakov · 29 pages

[Paper](https://github.com/ppadfoot/lagarias-zero-dimension/releases/download/v2.0.0/lagarias_zero_dimension.pdf) · [Release and complete archive](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v2.0.0)

### New results in this version

- **Uniform finite-visit control — Theorem 1.1.** For every $\delta>0$, some finite number $J$ of visits gives a countable compact cover of $F_J$ whose members have upper box dimension at most $\delta$. The visit count is fixed before the visit times are specified.
- **Vanishing nesting constants — Theorem 1.1.** Both $\Gamma_H=\lim_k\dim_H F_k$ and $\Gamma_P=\lim_k\dim_P F_k$ equal zero. This strengthens the infinite-visit conclusion of v1.
- **Real exceptional-set dimension — Theorem 7.1.** The full, untruncated real exceptional set satisfies $\dim_H E_{\mathbb R}=\dim_P E_{\mathbb R}=0$. The Hausdorff assertion is Lagarias's Conjecture 1.4; the packing conclusion is stronger.

### Complete proofs added

The uniform finite extraction theorem appears as Theorem 2.1. The real proof includes its own infinite-set extraction, a uniform affine finite-word bound, the exact floor-error transfer and the countable compact-cover argument. The two-translate capacity lemma and its proof appear in Lemma 9.1.

The v1 conclusion $\dim_H E_2=\dim_P E_2=0$ is recovered as Corollary 6.2. The complete causal-container appendix is reproduced unchanged from v1. Additional verification programs and reviews cover the new arguments.

The new finite-visit and real results first appear in this release. The v1 release, tag, manuscript and archive remain available at their original version links.

## v1.0.0 — 5 November 2026

**Zero Hausdorff and packing dimension for the 3-adic exceptional set of powers of two**  
Timofei Iuzhakov

[Paper](https://github.com/ppadfoot/lagarias-zero-dimension/releases/download/v1.0.0/lagarias_zero_dimension.pdf) · [Release and complete archive](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v1.0.0)

### Result in the original publication

**Theorem 1.1:** the 3-adic infinite-visit exceptional set satisfies

$$
\dim_H E_2=\dim_P E_2=0.
$$

The Hausdorff assertion is Lagarias's Conjecture 1.7. The manuscript also proves the stronger packing conclusion and a countable compact cover with arbitrarily small upper box dimension.

The proof combines unit-equation extraction, exact carry identities, a finite causal-container theorem proved in Appendix A, and a sumset capacity estimate. The release includes the manuscript, source, finite verification code and internal review reports.

The real exceptional-set theorem and the uniform finite-visit/nesting theorem were added in v2.

