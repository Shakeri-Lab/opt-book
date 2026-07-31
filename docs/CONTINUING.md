# Continuing Work

## Repository state

- Repository: `Shakeri-Lab/opt-book`
- Local branch: `main`
- Remote: configured, but the repository has no commits yet
- Canonical edition: HTML
- Derived edition: PDF
- Publication state: not committed, tagged, pushed, or deployed

## Current build

Build Plan v2 is the approved implementation baseline. C02, “One Pass, Two
Failures,” is the accepted pilot. C03, “The Grid Under the Update,” C04, “One
Step, Many Clocks,” C05, “The Safe Zone Is Logarithmic,” C06, “One Square,
Two Regimes,” C07, “The Sphere Has a Finite Price,” and C08, “One Average, Two
Edges,” are locally complete. C09, “The Bulk Is Not a Verdict,” is locally
complete and replaces the asymptotic-edge significance shortcut in the source
material with a matched finite-null contract. Both local HTML and the derived
PDF render successfully; source, contract, browser, and PDF audits pass subject
to the documented untagged-PDF fallback.

Current forced dual-edition build:

- 132 total PDF pages;
- C02 spans 14 physical pages (pages 11–24);
- C03 spans 14 physical pages (pages 25–38);
- C04 spans 16 physical pages (pages 39–54);
- C05 spans 12 physical pages (pages 55–66);
- C06 spans 15 physical pages (pages 69–83);
- C07 spans 12 physical pages (pages 85–96);
- C08 spans 14 physical pages (pages 97–110);
- C09 spans 16 physical pages (pages 111–126);
- C03 contains 2,647 rendered non-code words, excluding the bibliography;
- C04 contains 1,984 rendered non-code words, excluding the bibliography;
- C05 contains 2,163 rendered non-code words, excluding the bibliography;
- C06 contains 2,328 rendered non-code words, excluding Sources;
- C07 contains 1,753 rendered non-code words, excluding Sources;
- C08 contains 1,905 rendered non-code words, excluding Sources;
- C09 contains 2,507 rendered non-code words, excluding Sources;
- 19.80 seconds for a clean forced dual-edition execution/render;
- 36 passing harness tests and 38 passing repository tests.

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

- Active contract: `docs/chapter-contracts/C09.md`
- Active manuscripts: `chapters/act1/08-random-operators.qmd` and
  `chapters/act1/09-marchenko-pastur.qmd`
- Harness increment: `harness/src/trainable_harness/spectra.py`
- Evidence: the eight `artifacts/claims/c07-*.json`,
  `artifacts/claims/c08-*.json`, and `artifacts/claims/c09-*.json` records
- Current harness pin: `artifacts/harness/ch-09/manifest.json`

The C02–C09 wheels are built, vendored, and content-addressed locally. They do
not become immutable published pins until their source commits and annotated
harness tags exist.

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

Review and freeze C03–C09, then gate the C10 contract. Publication requires
source commits and annotated `harness-ch-02-v1` through `harness-ch-09-v1`
tags before the manifests can become immutable. Do not create placeholder
chapter files for C01 or C10–C17.
