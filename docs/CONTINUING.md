# Continuing Work

## Repository state

- Repository: `Shakeri-Lab/opt-book`
- Local branch: `main`
- Remote base commit: `7a68944` on `origin/main`
- GitHub Pages: <https://shakeri-lab.github.io/opt-book/>
- Canonical edition: HTML
- Derived edition: PDF
- Publication state: public rolling `v0.x` site; no annotated book release tag
  yet

## Current build

Build Plan v2 is the approved implementation baseline. C02, “One Pass, Two
Failures,” is the accepted pilot. C03, “The Grid Under the Update,” C04, “One
Step, Many Clocks,” C05, “The Safe Zone Is Logarithmic,” C06, “One Square,
Two Regimes,” C07, “The Sphere Has a Finite Price,” and C08, “One Average, Two
Edges,” are locally complete. C09, “The Bulk Is Not a Verdict,” replaces the
asymptotic-edge significance shortcut in the source material with a matched
finite-null contract. C10, “Full Rank, Few Directions,” closes Act I with an
effective-rank covariance diagnostic. C11, “The Gradient Has a Memory,” opens
Act II with fan-out accumulation and checkpoint/recomputation contracts. Both
local HTML and the derived PDF render successfully; source, contract, browser,
and PDF audits pass subject to the documented untagged-PDF fallback.

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
now carry bounded Audit branches; C12 owns the later CG/quasi-Newton harvest.
The shared paper-reading interface is
`docs/PAPER-AUTOPSY-PROTOCOL.md`.

Current forced dual-edition build:

- 156 total PDF pages;
- C02 spans 14 physical pages (pages 13–26);
- C03 spans 14 physical pages (pages 27–40);
- C04 spans 14 physical pages (pages 41–54);
- C05 spans 12 physical pages (pages 55–66);
- C06 spans 15 physical pages (pages 69–83);
- C07 spans 12 physical pages (pages 85–96);
- C08 spans 14 physical pages (pages 97–110);
- C09 spans 16 physical pages (pages 111–126);
- C10 spans 12 physical pages (pages 127–138);
- C11 spans 12 physical pages (pages 139–150);
- C02 contains 2,745 rendered non-code words, excluding the bibliography;
- C03 contains 2,756 rendered non-code words, excluding the bibliography;
- C04 contains 2,233 rendered non-code words, excluding the bibliography;
- C05 contains 2,163 rendered non-code words, excluding the bibliography;
- C06 contains 2,328 rendered non-code words, excluding Sources;
- C07 contains 1,753 rendered non-code words, excluding Sources;
- C08 contains 1,905 rendered non-code words, excluding Sources;
- C09 contains 2,507 rendered non-code words, excluding Sources;
- 42 passing harness tests and 2 passing repository fixture tests;
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
QUARTO_PYTHON="$OPT_BOOK_ENV/bin/python" quarto render
```

Fast audits:

```bash
"$OPT_BOOK_ENV/bin/python" scripts/run_fast_audits.py
```

## Current chapters

- Active contracts: `docs/chapter-contracts/C10.md` and
  `docs/chapter-contracts/C11.md`
- Active manuscripts: `chapters/act1/10-effective-rank.qmd` and
  `chapters/act2/11-reverse-accumulation.qmd`
- Harness increments: `harness/src/trainable_harness/spectra.py` and
  `harness/src/trainable_harness/autodiff.py`
- Evidence: `artifacts/claims/c10-effective-samples-001.json`,
  `artifacts/claims/c11-fanout-001.json`, and
  `artifacts/claims/c11-checkpoint-001.json`
- Current harness pin: `artifacts/harness/ch-11/manifest.json`
- Current source integrations: both
  `docs/source-audits/2026-icml-*.md` files and
  `docs/PAPER-AUTOPSY-PROTOCOL.md`

The C02–C11 wheels are built, vendored, and content-addressed. Their annotated
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

Gate the C12 curvature contract. Read both tutorial source audits, then replace
tutorial-level claims with primary-source verification before authoring.
Annotated `harness-ch-02-v1` through `harness-ch-11-v1` tags remain a separate
release task. Do not create placeholder chapter files for C01 or C12–C17.
