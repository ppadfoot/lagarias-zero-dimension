# Powers of two in ternary: zero-dimensional exceptional sets

**Timofei Iuzhakov** · Research preprint · **Version 2.0.0 — 6 November 2026**

**The paper proves the dimension assertions in two conjectures of Lagarias: the 3-adic conjecture and the real conjecture. In both settings, it also proves the stronger conclusion of packing dimension zero. Version 2 adds a uniform finite-visit theorem and vanishing nesting constants.**

[**Read the current paper · 29 pages**](https://github.com/ppadfoot/lagarias-zero-dimension/releases/download/v2.0.0/lagarias_zero_dimension.pdf) · [v2 release](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v2.0.0) · [Original v1](https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v1.0.0) · [How to cite](#citation)

## Three results at a glance

Repeatedly double a number and look at its base-3 digits. Which starting values avoid the digit **2** infinitely often? Lagarias formulated dimension conjectures for these exceptional starting values over both the 3-adic integers and the real numbers.

| Result | What the paper proves | First appeared |
| --- | --- | --- |
| **3-adic exceptional set** | $\dim_H E_2=\dim_P E_2=0$. Establishes the Hausdorff assertion of **Lagarias's Conjecture 1.7**, with the additional packing conclusion. | **v1.0.0**, 5 November 2026 |
| **Uniform finite-visit theorem** | $\Gamma_H=\Gamma_P=0$. For every positive dimension threshold, a sufficiently large **finite** number of visits already forces dimension below that threshold. | **v2.0.0**, 6 November 2026 |
| **Real exceptional set** | $\dim_H E_{\mathbb R}=\dim_P E_{\mathbb R}=0$. Establishes the Hausdorff assertion of **Lagarias's Conjecture 1.4**, again with the additional packing conclusion. | **v2.0.0**, 6 November 2026 |

Conjecture numbers refer to Lagarias's [2009 journal paper](https://doi.org/10.1112/jlms/jdn080). In its [arXiv version](https://arxiv.org/abs/math/0512006), the real and 3-adic assertions are called **Conjectures A and B**, respectively.

## Version 1: the 3-adic dimension conjecture

Let $\Sigma\subset\mathbb Z_3$ be the 3-adic Cantor set: its digits are all **0 or 1**. Define

$$
E_2=\{x\in\mathbb Z_3:2^n x\in\Sigma\text{ for infinitely many }n\ge0\}.
$$

Version 1 proves

$$
\boxed{\dim_H E_2=\dim_P E_2=0.}
$$

**Why this matters.** A published bound of Abram, Bolshakov and Lagarias was $\dim_H E_2\le\log_3\varphi\approx0.438018$, where $\varphi$ is the golden ratio. The v1 theorem reaches **zero**, the value conjectured by Lagarias, and controls packing dimension as well. See their [paper on multiplicative translates of 3-adic Cantor sets](https://arxiv.org/abs/1508.05967) for that earlier bound.

Version 1 also supplies the shared combinatorial ingredient: a **finite causal-container theorem**, with a complete proof. It turns digit constraints that depend on the already-read prefix into compatible products of conditional alphabets, with controlled information cost.

**Where to read it:** [v1 PDF, Theorem 1.1 and Appendix A](https://github.com/ppadfoot/lagarias-zero-dimension/releases/download/v1.0.0/lagarias_zero_dimension.pdf). The same dimension conclusion appears as **Corollary 6.2** of v2.

## Version 2: two further advances

### 1. A finite number of visits already controls dimension

Let $F_k$ contain the 3-adic starting values whose doubling orbit visits $\Sigma$ at least $k$ times, at distinct nonnegative times. Version 2 proves

$$
\boxed{\Gamma_H:=\lim_{k\to\infty}\dim_H F_k=0,
\qquad\Gamma_P:=\lim_{k\to\infty}\dim_P F_k=0.}
$$

The stronger covering statement is explicit: for every $\delta>0$, there is a finite $J$ such that $F_J$ has a countable cover by compact sets, each of upper box dimension at most $\delta$. **The number $J$ is chosen before the visit times are given.**

This strengthens v1: zero dimension for the infinite-visit set alone does not imply that the dimensions of the finite-visit sets tend to zero. The new proof provides that uniform control. Its arithmetic core is a uniform finite extraction theorem, proved using unit equations, finite Ramsey theory and valuation-minimal determinants.

**Where to read it:** v2 **Theorem 1.1**, with the extraction theorem in **Theorem 2.1** and the dimension argument in **Section 6**.

### 2. The real dimension conjecture, including packing dimension

Let $E_{\mathbb R}$ consist of positive real numbers $\lambda$ for which the **full ternary expansion** of $2^n\lambda$ uses only 0 and 1 for infinitely many $n$. The condition includes every digit after the ternary point. Version 2 proves

$$
\boxed{\dim_H E_{\mathbb R}=\dim_P E_{\mathbb R}=0.}
$$

**Why this matters.** This is the real exceptional set in Lagarias's Conjecture 1.4. The paper proves its conjectured Hausdorff dimension and the stronger packing conclusion. The proof includes a separate transfer from real digit prefixes to finite affine 3-adic constraints, uniform over the finitely many possible shifts.

The full-digit condition is essential: Lagarias's different problem using only the integer parts $\lfloor2^n\lambda\rfloor$ has exceptional-set Hausdorff dimension $\log_3 2$.

**Where to read it:** v2 **Theorem 7.1**, with the complete proof in **Sections 8–11**. The causal-container proof from v1 is reproduced unchanged in **Appendix A**; the required two-translate capacity estimate is proved in **Lemma 9.1**.

## What this means for Erdős Problem 406

These results determine the dimensions of the exceptional sets and strengthen the 3-adic result to a uniform finite-visit statement. Erdős's original question asks whether the particular starting value **1** is exceptional. **The assertion $1\notin E_2$ remains open here:** a zero-dimensional set can still contain that point. Countability and emptiness are also not established by these dimension theorems.

## Papers, proofs and verification

| Resource | Contents |
| --- | --- |
| [Current paper](paper/lagarias_zero_dimension.pdf) and [LaTeX source](paper/lagarias_zero_dimension.tex) | Complete v2 manuscript, including both new proof branches and the full shared appendix |
| [Version history](CHANGELOG.md) | Results introduced in each manuscript version, with links to the corresponding papers |
| [Verification code](code/) and [recorded results](verification/combined_summary.json) | Original finite-container checks, exact linear checks, 632,835 real-transfer identities and 5,400 affine-carry identities |
| [Internal review reports](audit/README.md) | Final-source mathematical reviews, their scope and exact source hashes |
| [Publication checklist](PUBLICATION_CHECKLIST.json) | Build, PDF inspection and package checks for the v2 release |
| [Companion paper: integer quotients of ternary Cantor numbers](https://github.com/ppadfoot/ternary-cantor-quotients) | A separate paper on a power lower bound and an infinite exceptional family |

Run all checks with **Python 3.10 or newer**, standard library only, with assertions enabled:

```bash
python3 run_all_checks.py
```

Build the PDF with Tectonic 0.17.0:

```bash
cd paper
tectonic lagarias_zero_dimension.tex
```

The finite programs supplement the general proofs. The manuscript and code received internal AI-assisted reviews; these are **not external peer review or proof-assistant verification**. AI assistance was used in mathematical development, editing, code and internal review. Sole author: **Timofei Iuzhakov**.

## Citation

**Cite the version containing the result you use:** v1 for the original 3-adic exceptional-set theorem; v2 for the finite-visit/nesting theorem or the real theorem. The v1 and v2 releases retain their own papers, source archives and dates. The repository's current README may receive explanatory updates between manuscript releases; use a versioned release for a fixed reference.

[CITATION.cff](CITATION.cff) and [CITATION.bib](CITATION.bib) describe the current manuscript:

```bibtex
@unpublished{iuzhakov2026lagarias,
  author = {Timofei Iuzhakov},
  title = {Zero dimension for the real exceptional set and vanishing 3-adic nesting constants},
  year = {2026},
  note = {Version 2.0.0; research preprint},
  url = {https://github.com/ppadfoot/lagarias-zero-dimension/releases/tag/v2.0.0}
}
```

For computational reproduction, also identify the code commit. No DOI or arXiv identifier has been assigned to this preprint.
