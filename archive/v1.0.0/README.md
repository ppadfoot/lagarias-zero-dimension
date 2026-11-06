# Zero Hausdorff and packing dimension for the 3-adic exceptional set of powers of two

**Timofei Iuzhakov** · Manuscript version **1.0.0** · 5 November 2026

[Read the paper](paper/lagarias_zero_dimension.pdf) · [LaTeX source](paper/lagarias_zero_dimension.tex) · [Full causal-container proof](paper/causal_container.tex) · [Verification scope](audit/VERIFICATION.md) · [Citation metadata](CITATION.cff)

Let

```math
\Sigma=\left\{\sum_{j\ge0}\varepsilon_j3^j:\varepsilon_j\in\{0,1\}\right\},\qquad
E_2=\{x\in\mathbb Z_3:2^nx\in\Sigma\text{ for infinitely many }n\ge0\}.
```

The manuscript proves

```math
\dim_H E_2=\dim_P E_2=0.
```

More precisely, for every positive epsilon, it constructs a countable cover by compact sets with upper box dimension at most epsilon. The proof combines the Evertse–Schlickewei–Schmidt finite-rank unit-equation theorem, a fully proved causal container lemma, Kneser's addition theorem, and conditional entropy.

The Hausdorff assertion is [Lagarias's Conjecture 1.7 (2009)](https://doi.org/10.1112/jlms/jdn080). The packing assertion is stronger. The paper does not prove countability of E2, E2={0}, or the pointwise Erdős assertion that 1 is outside E2.

## Reproduce the finite checks

Python **3.10 or newer**, standard library only:

```bash
python3 run_checks.py
```

Run with assertions enabled. Six programs check exact arithmetic identities, entropy calculations, full-product compatibility, origin accounting, nested projection queues, and replay from final fingerprints. The suite includes a nonvacuous container instance with 1,048,576 edges. Details and logs are written to `verification/`; individual JSON results are in `code/`.

These computations test finite instances and implementation invariants. They are not a proof-assistant certificate for the theorem. The infinite result is supported by the written proof. Three separate AI agent reviews of the complete proof and the exact final English source are included in `audit/`; no external peer review or formal verification is claimed.

## Build the PDF

The release PDF was built with [Tectonic](https://tectonic-typesetting.github.io/) **0.17.0**:

```bash
cd paper
tectonic -X compile lagarias_zero_dimension.tex
```

The first build may download the standard TeX packages and fonts. The two TeX files are sufficient. A conventional LaTeX installation with the listed packages can also compile the source.

## Version and citation

Cite **version 1.0.0** and the repository commit used. `v1.0.0` identifies this research release. A BibTeX key is a local citation label; it is not an identifier issued by a publisher or evidence of priority. No DOI or arXiv identifier is claimed.

```bibtex
@misc{iuzhakov2026lagarias,
  author = {Timofei Iuzhakov},
  title = {Zero Hausdorff and packing dimension for the 3-adic exceptional set of powers of two},
  year = {2026},
  note = {Version 1.0.0. Manuscript with finite verification code},
  url = {https://github.com/ppadfoot/lagarias-zero-dimension}
}
```

Public GitHub timestamps record when this version became publicly available. They are not a guarantee of novelty or of priority over all independent work. The source history and review scope are described in [PROVENANCE.md](audit/PROVENANCE.md).

ChatGPT assisted with mathematical development, code, editing, and internal review, as disclosed in the manuscript. The sole named author is Timofei Iuzhakov.
