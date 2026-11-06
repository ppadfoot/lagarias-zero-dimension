# Verification scope: version 2.0.0

The final merged manuscript and unchanged causal-container appendix receive two independent internal full-source reviews. The reports named `final_*` bind their conclusions to exact SHA-256 source hashes. The authoring agents also checked preservation of their source arguments; these checks are not independent reviews of their own contributions.

The v2 review covers the uniform finite-visit theorem, vanishing 3-adic nesting constants, the E2 corollary, and the separate real infinite-visit proof. It specifically distinguishes virtual anchors in the finite-visit argument from true-visit anchors in the real extraction, and checks the real affine word bound, floor transfer, countable compact covers and packing-dimension limit. The shared causal-container appendix remains unchanged from v1 and is included in the dependency review.

Run `python3 run_all_checks.py` with Python 3.10 or newer and assertions enabled. The original six-program suite is retained. Additional checks cover exact linear geometry, 632835 real-transfer identities and 5400 affine-carry identities. Machine-readable outcomes and execution logs are in `verification/combined_summary.json` and its accompanying logs.

The original v1 verification description and reports retain their historical scope; its description is preserved in `archive/v1.0.0/audit/VERIFICATION.md`. Older reports do not certify the new merged source. `PUBLICATION_CHECKLIST.json` records the final package checks.

Finite programs check identities and implementation invariants; they do not prove universal assertions by extrapolation. The external unit-equation and Kneser theorems are cited inputs. Internal AI-assisted reviews are not external peer review or Lean/Coq/Isabelle verification.
