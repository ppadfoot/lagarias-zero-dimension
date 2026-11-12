# Version 4 review record

Prepared 12 November 2026. Mathematical author: **Timofei Iuzhakov**.

Version 4 adds complete sections on generalized exceptional dimension, Haar-typical multiplicative intersections, and fractional-part/fixed moving targets. The exact selection and exclusions appear in the [publication inventory](../../INVENTORY.md); the [source-question map](source_question_map.txt) distinguishes the original questions from known inputs and further consequences.

| Section | Independent final-source review | Proof and attribution map |
| --- | --- | --- |
| Exact generalized dimension | [Generalized-section review](final_generalized_review.txt) | [A02 source map](a02_source_map.txt) |
| Typical intersection dimensions and parameter geometry | [Typical-section review](final_typical_review.txt) | [A03 source map](a03_source_map.txt) |
| Fractional parts and fixed moving targets | [Circle integration review](final_circle_integration_review.txt) | [Circle source map](circle_source_map.txt) |

Each mathematical report identifies the source it actually reviewed and its SHA256 hash. A pass applies to that revision and the claims within the report's scope. The [root integration review](root_integration_review.txt) records assembly checks and the relationship to preserved earlier sections. Build, visual inspection, code reruns and release packaging are recorded separately in [PUBLICATION_CHECKLIST.json](../../PUBLICATION_CHECKLIST.json).

The [v4 verification scripts](../../code/v4) test finite arithmetic, capacities, collisions, coding and transfer identities. Passing these checks supports the corresponding identities; it does not replace an all-depth proof. No script is represented as proving the exclusion of the point 1.

The three new proof files are fully included under [paper](../../paper). Development-note identifiers in the source maps provide provenance only. Those notes and private chats are neither required to build the article nor invoked in place of a supplied proof. The circle section states its dependence on earlier finite-word results already present in the same manuscript.

These are internal AI-assisted mathematical reviews, including reviewers who did not author the section they checked. They are not external journal peer review or formal proof-assistant verification. The historical [v3 reports](../v3/README.md), earlier reports and research ledger retain their original scope. Inclusion in v4 does not freshly certify every historical assertion or establish worldwide priority.

The companion [ternary-cantor-quotients](https://github.com/ppadfoot/ternary-cantor-quotients) remains a separate article. Its new candidates require their own integrated manuscript and final-source review; this review record does not certify or publish that future update.
