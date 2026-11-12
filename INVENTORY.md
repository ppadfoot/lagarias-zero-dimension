# Publication inventory and selection

Timofei Iuzhakov · 12 November 2026

## Results selected for version 4

Version 4 extends the existing article with three complete proof sections. The selection below records what this version adds; the version-3 inventory is preserved afterwards as a dated historical snapshot. The article keeps the citation key `iuzhakov2026lagarias` and the sole author Timofei Iuzhakov.

| Selected result | What version 4 establishes | Source question and scope |
| --- | --- | --- |
| **Exact generalized exceptional dimension** | Hausdorff and packing dimensions of $`E_*`$, its generalized Hausdorff nesting constant $`\Gamma_*`$, and its packing nesting limit all equal $`\tfrac12\log_3 2`$. The section also gives a quantitative upper convergence rate and a sharp Assouad bound for each fixed infinite family of distinct unit multipliers. | Abram–Lagarias (2014), Problem 1.6 and (1.14). The positive lower bound and Bolshakov construction were already known; the matching upper bound is the new part included here. This is the internal A02 group. |
| **Exact typical intersection dimensions** | For Haar-almost every $`\lambda\in1+3\mathbb Z_3`$, the Hausdorff, packing, lower box and upper box dimensions of $`\Sigma\cap\lambda^{-1}\Sigma`$ are all $`\log_3(4/3)`$. A full-support fair measure, a sharp golden-ratio bound for nonidentity unit multipliers and the punctured dimension limits at the identity complete the section. | Addresses the measure-theoretic part of the parameter programme in Abram–Lagarias §2.4. A03 is an internal label, not a numbered source conjecture. The full exceptional spectrum and category questions remain outside the result. |
| **Fractional-part and fixed moving-target exceptional sets** | The real circle exceptional set has Hausdorff and packing dimension zero. The theorem permits any fixed sequence of real target translations, with a parallel 3-adic statement and any fixed finite number of alternatives per time. | Answers Lagarias's §5 fractional-part question for the digits-0,1 target $`K_{01}`$. The standard digits-0,2 target $`K_{02}=2K_{01}`$ is an additional proved variant. Each target sequence is fixed before the starting point is chosen. |

The complete proofs are in [generalized exceptional sets](paper/generalized_exceptional.tex), [typical intersections](paper/typical_intersections.tex), and [circle targets](paper/circle_targets.tex). The [v4 review record](audit/v4/README.md) identifies the exact reviewed sources, while the [source-question map](audit/v4/source_question_map.txt) distinguishes external questions, known inputs and extensions. Finite verification scripts in [code/v4](code/v4) check arithmetic and combinatorial identities; they supplement the proofs.

The supporting lemmas, convergence rate, measure construction and coding consequences are organized within these three arguments. They are not counted as additional independently resolved source conjectures. The prior dimension, metric and counting sections remain part of the same article and retain their original version attribution.

## Selection boundaries for version 4

- **Still unresolved here:** $`1\notin E_2`$, the exact list of good powers, a subpolynomial count of actual good powers, the full exceptional parameter spectrum and category questions, and the sharp quotient-counting asymptotics. No reduction, restricted pattern family or finite computation is promoted to a solution of these targets.
- **Separate companion article:** [ternary-cantor-quotients](https://github.com/ppadfoot/ternary-cantor-quotients) keeps its own article and citation identity. New quotient-specific material is reserved for its own reviewed update; it is not absorbed into this v4 or silently assigned a new status here.
- **Review scope:** the v4 reports apply to the named final source hashes. Historical ledgers and earlier reviews retain their original scope. This update does not freshly certify every archived research claim or claim worldwide priority.
- **Public package:** the selected proofs, verification code and scoped review reports are included. Raw private chat exports are not publication dependencies and are not included.

## Historical version-3 snapshot — 7 November 2026

The remaining text preserves the earlier inventory. Its references to “this update,” deferred results and then-current companion versions describe **version 3**, not the current v4 selection above. Where later results supersede those decisions, the v4 selection takes precedence; the earlier record remains available for version history.

This inventory separates the new version-3 sections from earlier publications and from the remaining research programme. Its baseline covers **217 formal historical records, 51 grouped results and 20 recovered archives**; later packets extend and supersede that baseline. These counts describe records and sources, **not 217 independent new theorems**. The complete available mathematical ledger is retained in [research_inventory.json](inventory/research_inventory.json), with source hashes in [source_manifest.json](inventory/source_manifest.json).

The historical review labels in the ledger are inherited. Inclusion in that ledger is not a new proof certification. Fresh publication review applies to the exact final sources named in [the review record](audit/v3/README.md). Raw private chat transcripts are not part of this publication.

## Results selected for the new sections of version 3

| Result | Why it belongs in this paper | Proof scope |
| --- | --- | --- |
| Generic absence of three nonzero visits | For varying bases, strengthens the earlier countability result to absence of any nonzero point in the third visit layer | One Haar-null exceptional set of bases, simultaneously for all starting points and times; excludes no prescribed base |
| Complete finite maximal-branching classification | Identifies both coefficient configurations and every allowed target; supplies the rigidity used in the metric proof | Every finite depth; not a conjecture inferred from enumerated depths |
| Summability of reduced Cantor denominators | Connects rational Cantor orbits to multiplicative-order estimates and controls an infinite sieve tail | Interior reduced denominators prime to 3, each denominator counted once; explicit external analytic input |
| Linear order of positive-dimensional multipliers | Determines the order of growth in Lagarias's second counting problem | Positive lower natural density; no asserted natural-density limit |
| Linear gap between positive-dimensional and finite-witness multipliers | Shows quantitatively that integer-witness constructions omit a large class of positive-dimensional intersections | Lower bound for the difference of sets, not a linear lower bound for the finite quotient count |

These form two complete, independent arguments in the updated article. The main results do not depend on the earlier causal-container manuscript or on an unproved statement about the point 1.

## Earlier publications, preserved

| Existing manuscript | Results already published there | Treatment in this update |
| --- | --- | --- |
| Dimension paper v1.0.0 | Zero Hausdorff and packing dimensions of the 3-adic infinite-visit set | Original release and citation preserved |
| Dimension paper v2.0.0 | Vanishing finite-visit nesting constants and the real full-expansion dimension theorem | Original release, source and PDF preserved; not relabelled as new |
| Quotient paper v1.0.0 | Lower-bound exponent 0.6660585297… and the infinite family 621·3^(4k)−20 of sporadic exceptions | Original release preserved; version-3 counting theorem linked |

The earlier dimension assertions correspond to Lagarias's Conjectures A/B in the arXiv version, or 1.4/1.7 in the journal numbering. This update does not claim a new complete recertification of every line of those earlier manuscripts.

## Completed research retained outside the present article

These subjects remain in the mathematical inventory. They are not silently discarded or claimed as theorems proved in version 3.

| Subject | Latest retained content | Publication decision |
| --- | --- | --- |
| Quotient power exponent | 0.691726633148796… from a separate block/coset-energy certificate | Separate strengthening requiring its own full integration and final-source review; not attributed to quotient v1 |
| Real finite-visit and forbidden-word extensions; finite-rank slopes | Broader dimension and covering results in the recovered corpus | Preserve source and inherited status; separate from the two independent new proofs |
| Spectrum, plateaux and carry-graph geometry | Golden-boundary classification, fixed-graph estimates and explicit zero-dimensional multiplier families | Preserved as distinct results, not consequences of the new metric theorem |
| Visit counts and affine Fourier estimates | Uniform sublinear counts, conditional-digit costs, rational starting-height bounds | Counting bounds permit infinitely many sparse visits; omitted from the main article |
| Repeated/common blocks and rational tails | Subspace-theorem restrictions with precise height, length and rank hypotheses | No proof that every good power must satisfy the restrictive hypotheses |
| Rational denominators and numerator orbits | Scoped denominator classifications, the orbit with denominator 4561 and partial phase exclusions | No complete rational-orbit exclusion asserted |
| Original window conjecture W | Resolved in the effective-windows packet of our internal manuscript B | Internal conjecture, not a numbered question of Lagarias; its auxiliary formulation is not a third headline problem |
| Actual powers and effective strict windows | Every actual time triple has a finite strict window; stronger logarithmic windows in specified classes | Parameter branching loss does not exclude a fixed surviving point |
| Sparse and structured integer exponents | Complete input ternary-weight classification through weight 7; repunit, defect, support and run families with stated scopes | Infinite-family results, but no forcing into those families; no extrapolation to all weights |
| Uniform run centres and repair paths | All-run identities and exact counterexamples to particular termination arguments | Method diagnostics, not a proof of E1 |
| Height strip and block splitting | Exact endpoint reduction and uniform sublinear block-splitting constraints | No exclusion of all good integer endpoints |
| B=0-preserving damping | Exact weighted endpoint identity and a uniform gap; oriented Fourier formulas | The required eventual phase estimate is unproved; not a new exclusion theorem |

The latest packets supersede older scope statements. For example, weight 7 replaces the earlier weight-4/5/6 thresholds; the generic three-visit theorem replaces the older open metric target and countability conclusion. The earlier energy estimate itself is still open even though the metric target was proved by a different argument.

## Questions that remain open in this programme

- Finiteness of the good powers: **1 not in E₂**.
- The stronger exact list of good powers, with exponents 0, 2 and 8 for base 2.
- The exact asymptotic **M_H(X) ~ X/2** and the long-entrance contribution for fixed terminal denominators.
- The sharp order of **M_C(X)**.
- The universal eventual occurrence of every fixed digit word (Lagarias's Conjecture E).
- The unproved primitive-energy estimate and the additional spectral and rational-orbit problems retained in the ledger.

No search result, internal review, finite computation, version number or GitHub timestamp is treated as a proof of worldwide novelty. Versioned files and immutable commit links identify exactly what was made public.
