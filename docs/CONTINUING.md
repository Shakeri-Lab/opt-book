# Continuing Work

## Repository state

- Repository: `Shakeri-Lab/opt-book`
- Local branch: `main`
- Reviewed predecessor: `aff0b20` on `origin/main`; use `git log -1` for the
  revision that supersedes it
- GitHub Pages: <https://shakeri-lab.github.io/opt-book/>
- Canonical edition: HTML
- Derived editions: recto-aware print PDF and continuous screen PDF
- Publication state: public rolling `v0.x` site; no annotated book release tag
  yet; the first forward-only harness source tag is
  `harness-ch-14-r2-v1`

## Current build

Build Plan v2 is the approved implementation baseline. The complete approved
C01–C17 core now has locally complete drafts. C01 installs the resource model;
C02–C10 build numerical stability and high-dimensional geometry; C11–C17
carry reverse accumulation, curvature objects, stochastic regimes,
criticality, coordinate-wise normalization, edge of stability, and
matrix-update geometry through the terminal Paper Autopsy Protocol. The
unnumbered Coda now closes the opening loss-spike incident with all five
diagnostic controls. Three authored act interludes now make the lens handoffs
explicit, every recap ends on a question, every Sources section supplies a
reading order, and the final appendix hands the blank Incident Card to the reader
after the references. On 2026-08-01 the author accepted C01/C03–C17, the C14
revision, the Coda, all three act interludes, the Incident Card, the On-Ramp,
and *Beyond This Volume*; C02 remains the previously accepted pilot. D01–D50
are ratified. D45 supersedes the earlier gated-Act-III possibility for this
volume: the unnumbered continuation map owns the course synthesis routes. Both
local HTML and both derived PDFs render successfully; source, contract, HTML,
and PDF audits pass subject to the documented untagged-PDF fallback.

The unnumbered On-Ramp now makes the prerequisite boundary explicit: no prior
deep-learning course is required. It supplies a 20–30 minute diagnostic, a
three-stop repair route through the earlier sibling volume, one minimal NumPy
training loop, and a Chapter 1 readiness checklist. Searchable technical
locators now appear in all chapter titles. C14, C16, and C17 carry worked
transfer bridges, while C04/C10/C17 build the Incident Card cumulatively. The
unnumbered *Beyond This Volume* section maps the course's attention/kernel,
IO-aware, parallel-scan, and feature-learning synthesis without opening a new
act in this book.

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

The full instructor-supplied `Others lectures/` shelf has now been compared
against C01–C17. Its review, collection fingerprints, claim hazards,
deduplication decisions, and bounded integration map live in
`docs/source-audits/other-lectures-shelf-audit.md`. The recommended harvest is
three short main-text seams (C04 explicit-discretization bridge, C05 Gaussian
Lipschitz concentration, and C12 normal-equation conditioning) plus nine
diagnostic exercise changes. T1–T3 are now implemented with their assumptions
and primary/canonical routing on the page. The exercise package remains a
separate bounded revision; no new chapter or Act III expansion is implied.

Roberts and Yaida's *The Principles of Deep Learning Theory* has received a
separate model-level audit in
`docs/source-audits/pdlt-effective-theory.md`. D50 is now implemented. C14
separates moment, pair-geometry, Jacobian-spectrum, and depth-to-width
contracts; its two new class-(a) witnesses use the corrected zero-bias ReLU
correlation map and the exact finite-width fluctuation law. Historical
`ch-14` remains untouched, while the forward-only `ch-14-r2` wheel carries
the new controls. The feature-learning mechanism is routed to the unnumbered
continuation map rather than made into a second theoretical spine.

Current forced multi-edition build:

- 258 print-PDF pages and 238 screen-PDF pages; the print edition retains 22
  recto/verso blank pages and the screen edition has none;
- physical print chapter openers for C01–C17 are pages 23, 31, 47, 61, 79,
  91, 107, 119, 133, 149, 163, 175, 187, 197, 207, 215, and 223; the Coda
  begins on 233, *Beyond This Volume* on 239, and the provenance note on 241;
- physical spans for C01–C17 are 8, 16, 14, 18, 12, 16, 12, 14, 16, 14, 12,
  12, 10, 10, 8, 8, and 10 pages; the Coda spans 6 pages and the continuation
  map spans 2;
- source non-code word counts excluding Sources for C01–C17 are 1,247,
  2,733, 2,577, 2,243, 2,236, 2,344, 2,040, 2,195, 2,536, 2,065, 1,898,
  2,524, 1,516, 2,396, 1,199, 1,235, and 1,898;
- `artifacts/book-metrics.json` is the single audited ledger for those values;
  `scripts/audit_book_metrics.py` fails when the rendered build drifts;
- 58 passing harness and repository tests;
- nine current deep-revision evidence verifiers pass: eight match their deterministic
  controls within declared numerical gates, while the device-scoped timing protocol re-executes and
  checks its count/rate arithmetic without a false cross-device speed gate;
  the claim directory remains clean;
- every frozen HTML and TeX execution is now traceback-free; the rendered
  audit rejects stale `cell-output-error` blocks;
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
- Final take-away object: `chapters/appendices/incident-card.qmd`
- Most recent harness increment:
  `harness/src/trainable_harness/update_geometry.py`
- Evidence: `artifacts/claims/coda-incident-001.json`
- Current harness pin: `artifacts/harness/ch-17/manifest.json`
- Most recent forward-only revision pin:
  `artifacts/harness/ch-14-r2/manifest.json`
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
- licensing constraints on the resource shelf, especially permission to name
  privately supplied lecture collections in the public provenance note.

## Next safe action

The author-acceptance and D29–D50 ratification gates are closed. T1–T3 are
implemented; E1–E9 remain a separate displacement-controlled exercise pass.
The next queued work is D23 sibling reciprocity at v0.2, registration of the
KMP staircase as a C16 Paper-audit exhibit, and the R17 figure-byte
determinism audit. The course's synthesis has a stable unnumbered route rather
than an implied Act III. D34 is forward-only: preserve SHA-256 identities for
historical rolling-draft wheels and require an annotated source tag for every
new wheel.
