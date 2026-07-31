# Continuing Work

## Repository state

- Repository: `Shakeri-Lab/opt-book`
- Local branch: `main`
- Reviewed predecessor: `3878f13` on `origin/main`; use `git log -1` for the
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
matrix-update geometry through the terminal Paper Autopsy Protocol. The
unnumbered Coda now closes the opening loss-spike incident with all five
diagnostic controls. C02 is the accepted pilot; C01/C03–C17 and the Coda
remain author-review drafts. Act III is still gated by D02 and was not
silently created. Both local HTML and the derived PDF render successfully;
source, contract, HTML, and PDF audits pass subject to the documented
untagged-PDF fallback.

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

- 236 total PDF pages;
- physical chapter openers for C01–C17 are pages 15, 23, 39, 53, 69, 81,
  97, 109, 123, 139, 151, 163, 175, 185, 191, 201, and 209; the Coda begins on
  219 and the provenance note on 225;
- physical spans for C01–C17 are 8, 16, 14, 16, 12, 16, 12, 14, 16, 12, 12,
  12, 10, 6, 10, 8, and 10 pages; the Coda spans 6 pages;
- source non-code word counts excluding Sources for C01–C17 are 1,232,
  2,746, 2,588, 2,081, 2,031, 2,345, 2,042, 2,219, 2,544, 1,994, 1,889,
  2,332, 1,493, 1,016, 1,151, 1,044, and 1,499;
- `artifacts/book-metrics.json` is the single audited ledger for those values;
  `scripts/audit_book_metrics.py` fails when the rendered build drifts;
- 57 passing harness and repository tests;
- seven new deep-revision evidence verifiers pass: six match their deterministic
  controls exactly, while the device-scoped timing protocol re-executes and
  checks its count/rate arithmetic without a false cross-device speed gate;
  the claim directory remains clean;
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
SOURCE_DATE_EPOCH=0 PYTHONHASHSEED=0 MPLBACKEND=Agg \
  QUARTO_PYTHON="$OPT_BOOK_ENV/bin/python" quarto render
```

Fast audits:

```bash
"$OPT_BOOK_ENV/bin/python" scripts/run_fast_audits.py
```

## Current chapters

- Most recent contract: `docs/chapter-contracts/CODA.md`
- Most recent manuscript: `chapters/coda.qmd`
- Most recent harness increment:
  `harness/src/trainable_harness/update_geometry.py`
- Evidence: `artifacts/claims/coda-incident-001.json`
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

Perform author review of the deep-revised C01/C13–C17 and Coda first, then
accept C03–C12 by diff. Decide whether D02 opens any Act III synthesis only
after that review. Annotated harness tags remain a separate release task under
open decision D34; do not invent source identities for rolling-draft wheels.
