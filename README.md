# Zero dimension for the real exceptional set and vanishing 3-adic nesting constants

**Timofei Iuzhakov** · Research preprint **2.0.0** · 6 November 2026

[Paper](paper/lagarias_zero_dimension.pdf) · [LaTeX](paper/lagarias_zero_dimension.tex) · [Versioned release](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v2.0.0) · [Citation](CITATION.cff)

The dyadic nesting constants satisfy Gamma_H=Gamma_P=0. The untruncated real exceptional set has Hausdorff and packing dimension zero. The earlier zero-dimensional 3-adic exceptional-set theorem is recovered as a corollary.

The manuscript does not resolve Erdős Problem 406, exclude 1 from E2, or prove countability of E2. The multiplier lower bound, where discussed, is not a bound on the number of exceptional powers of two.

## Version history

v1.0.0 (5 November 2026) proved zero Hausdorff and packing dimension of E2. Its [release](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v1.0.0) and original files in `archive/v1.0.0/` are preserved. Version 2.0.0 first adds the uniform finite-visit theorem and the full real exceptional-set theorem. These additions are not backdated to v1.0.0. The real theorem uses its own affine finite-word transfer, not the bare Gamma=0 conclusion.

## Reproduction

Python 3.10 or newer, standard library only, assertions enabled:

```bash
python3 run_all_checks.py
```

The finite programs test identities, algorithm invariants and the supplied certificate. They do not replace the general mathematical arguments. Results and execution logs are included. The final-source internal reviews and their scope are in `audit/`.

Build with Tectonic 0.17.0 (or a conventional LaTeX installation):

```bash
cd paper
tectonic lagarias_zero_dimension.tex
```

## Citation

Cite the exact manuscript version and relevant theorem. For the code, also identify the commit. No DOI or arXiv identifier is claimed.

```bibtex
@unpublished{iuzhakov2026lagarias,
  author = {Timofei Iuzhakov},
  title = {Zero dimension for the real exceptional set and vanishing 3-adic nesting constants},
  year = {2026},
  note = {Version 2.0.0; research preprint},
  url = {https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v2.0.0}
}
```

AI assistance was used for mathematical development, editing, code and internal review. Sole author: Timofei Iuzhakov. Internal reviews are not external peer review or proof-assistant verification; novelty and worldwide priority are not certified by GitHub timestamps.
