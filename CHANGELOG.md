# Manuscript versions

Each release fixes a manuscript, its source, verification code and review record. The main README explains the results and may be updated independently of the manuscript versions.

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
