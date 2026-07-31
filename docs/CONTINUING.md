# Continuing Work

## Repository state

- Repository: `Shakeri-Lab/opt-book`
- Local branch: `main`
- Reviewed predecessor: `3eb57b8` on `origin/main`; use `git log -1` for the
  revision that supersedes it
- GitHub Pages: <https://shakeri-lab.github.io/opt-book/>
- Canonical edition: HTML
- Derived edition: PDF
- Publication state: public rolling `v0.x` site; no annotated book release tag
  yet

## Current build

Build Plan v2 is the approved implementation baseline. The complete approved
C01–C17 core now has locally complete drafts. C01 installs the resource model;
C02–C10 build numerical stability and high-dimensional geometry; C11–C17
carry reverse accumulation, curvature objects, stochastic regimes,
criticality, coordinate-wise normalization, edge of stability, and
matrix-update geometry through the terminal Paper Autopsy Protocol. C02 is
the accepted pilot; C03–C17 remain author-review drafts. Act III is still
gated by D02 and was not silently created. Both local HTML and the derived PDF
render successfully; source, contract, HTML, and PDF audits pass subject to
the documented untagged-PDF fallback.

The 211-slide ICML 2026 tutorial *Is numerical optimization theory irrelevant
to machine learning practice in 2026?* has been reviewed completely as an
external reference-only source. Its integration and refusal map lives in
`docs/source-audits/2026-icml-optimization-theory-tutorial.md`. The current
revision sharpens C04's meaning of an optimal step, plants C08→C17 update
geometry, and registers new C13/C16 obligations without importing benchmark
or anecdotal claims.

The 131-slide ICML 2026 tutorial *Probabilistic Numerics — Computation is
Machine Learning* has also been reviewed completely. Its seam/refusal map is
`docs/source-audits/2026-icml-probabilistic-numerics-tutorial.md`. C02 and C03
now carry bounded Audit branches; C12 harvests the bounded CG/quasi-Newton
seam without importing the tutorial's full apparatus.
The shared paper-reading interface is
`docs/PAPER-AUTOPSY-PROTOCOL.md`.

Current forced dual-edition build:

- 210 total PDF pages;
- physical chapter openers for C01–C17 are pages 15, 21, 35, 49, 65, 77,
  93, 105, 119, 135, 147, 159, 171, 177, 183, 189, and 195;
- C01 and C13–C17 each use six physical pages through the next recto chapter
  opening; printed starts are 7, 163, 169, 175, 181, and 187;
- C02 contains 2,745 rendered non-code words, excluding the bibliography;
- C03 contains 2,756 rendered non-code words, excluding the bibliography;
- C04 contains 2,233 rendered non-code words, excluding the bibliography;
- C05 contains 2,163 rendered non-code words, excluding the bibliography;
- C06 contains 2,328 rendered non-code words, excluding Sources;
- C07 contains 1,753 rendered non-code words, excluding Sources;
- C08 contains 1,905 rendered non-code words, excluding Sources;
- C09 contains 2,507 rendered non-code words, excluding Sources;
- C10/C11 word counts are deliberately not mixed into the legacy manual
  series: the current reproducible HTML parser reports 1,801 and 1,924
  non-code words, respectively, but does not reproduce the earlier counting
  convention. The same source-side parser counts 2,344 prose-like words in
  C12. The same source-side approximation reports 848, 940, 814, 861, 935,
  and 1,042 words for C01 and C13–C17. Replace the entire manual series with
  one CI-emitted metrics ledger before using chapter counts comparatively;
- 55 passing harness tests and 2 passing repository fixture tests;
- all fast contract audits and the rendered HTML/PDF audit pass.

The harness is being born book-first. No course-wide package was found in the
reviewed course tree. If additional instructor-held harness code appears,
audit it as evidence before changing the public API.

## Environment

The intended local environment is Python 3.12 managed by `uv`, with the virtual
environment outside the Box-synchronized repository. Point a task-specific
variable at that environment, then use:

```bash
export OPT_BOOK_ENV=/absolute/path/outside/Box/opt-book/.venv
UV_PROJECT_ENVIRONMENT="$OPT_BOOK_ENV" uv sync
SOURCE_DATE_EPOCH=0 QUARTO_PYTHON="$OPT_BOOK_ENV/bin/python" quarto render
```

Fast audits:

```bash
"$OPT_BOOK_ENV/bin/python" scripts/run_fast_audits.py
```

## Current chapters

- Most recent contract: `docs/chapter-contracts/C17.md`
- Most recent manuscript: `chapters/act2/17-update-geometry.qmd`
- Most recent harness increment:
  `harness/src/trainable_harness/update_geometry.py`
- Evidence: `artifacts/claims/c17-update-norm-001.json`
- Current harness pin: `artifacts/harness/ch-17/manifest.json`
- Current source integrations: the ICML tutorial audits,
  `docs/source-audits/remaining-core-chapters.md`, and
  `docs/PAPER-AUTOPSY-PROTOCOL.md`

The C02–C17 wheels are built, vendored, and content-addressed. Their annotated
harness tags and manifest source identities remain intentionally absent; do
not backfill them with a commit that did not produce the wheel.

## Source warning retained

An instructor slide labels the current framework variance kernel “two-pass.”
The current primary source instead dispatches a Welford-style CUDA reduction.
Do not publish a backend claim without a version or commit pin. The chapter
teaches algorithmic choices rather than an unversioned framework fact.

## Inputs still welcome

- any harness or lab code held outside the reviewed tree;
- canonical confirmation for source variants;
- anonymized student feedback;
- reuse permissions for student work;
- licensing constraints on the resource shelf.

## Next safe action

Perform author review of C03–C17 as diff-based chapter acceptances, then decide
whether D02 opens any Act III synthesis. Annotated harness tags remain a
separate release task under open decision D34; do not invent source identities
for the rolling-draft wheels.
