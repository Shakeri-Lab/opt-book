# Backlog

## Build-blocking

- Decide the complete-book budget from the committed C01–C17 metrics ledger
  rather than extrapolating from the C02 pilot alone.

## Completed v0.2 publication gate

- Added the detached-PDF rights statement and enforced it in both PDF audits.
- Bound the public-draft 0.2 citation to source metadata and the annotated
  `book-v0.2.0` tag, including both derived-PDF digests.
- Added the diagnostic-card covenant and fast audit: the Paper Autopsy and
  Incident Card remain distinct, while every public manifestation of each is
  order-locked.
- Added the 0.2 changelog entry and release note.

## Completed 2026-08-01 acceptance and release-identity pass

- Recorded author acceptance of C01/C03–C17, the C14 revision, the Coda, all
  three act interludes, the Incident Card, the On-Ramp, and *Beyond This
  Volume*. C02 remains the previously accepted pilot.
- Recorded explicit author ratification of D29–D50.
- Resolved D34 forward-only: historical wheels retain SHA-256 identities;
  `harness-ch-14-r2-v1` begins the annotated source-tag contract.
- Implemented T1–T3 as bounded main-text seams in C04, C05, and C12.

## Completed 2026-08-01 alignment pass

- Added the no-prior-course On-Ramp and executable NumPy training loop.
- Replaced repeated printed verification scaffolding with the centralized
  claim helper and compact provenance strips.
- Added searchable chapter titles, the bounded *Beyond This Volume* map,
  C14/C16/C17 transfer bridges, cumulative act checkpoints, and a second
  deliberately non-identifiable incident.
- Added an audited continuous screen PDF while retaining the recto-aware print
  edition.

## Cross-book — completed at sibling v1.2.1

- The sibling repository now owns `docs/public-anchors.md`; CI checks all ten
  consumed interfaces in source and rendered HTML.
- Five collision surfaces carry bounded forward pointers into this volume,
  and both colophons identify the companion book.
- Any future change to a declared anchor is a coordinated interface migration.

## Accessibility

- **First-build result (2026-07-30):** the normal Quarto 1.10.18
  `include-in-header` route cannot activate the LaTeX PDF resource manager
  early enough. LuaHBTeX 1.24.0 stops with `Package tagpdf Error: PDF resource
  management is not active!`
- The smallest failing input is preserved in `tex/tagged-pdf-attempt.tex` and
  the acceptance contract in `tests/fixtures/tagged-pdf.md`.
- Install a version-pinned pre-documentclass template, validate its structure
  tree, and manually inspect reading order. Do not claim PDF/UA until those
  checks pass.
- Add `/ActualText` or native text alternatives for any future figure with
  embedded labels.

## Materials and provenance

- Receive or confirm any external harness/lab code.
- Confirm canonical Spring 2026 source variants.
- The `Others lectures/` shelf fingerprinting and exercise-deduplication pass
  is complete in `docs/source-audits/other-lectures-shelf-audit.md`. Preserve
  its external-reference-only status and route public claims to primary or
  canonical sources.
- Record student-work permissions before public reuse.
- Route the ICML 2026 optimization-theory tutorial's remaining load-bearing
  claims to primary papers at C13, C16, and C17 contract time; do not cite the
  tutorial as sole technical authority.
- C12 has routed the Probabilistic Numerics seam to Hennig (2015) and
  Hennig–Kiefel (2013), with its primary-source audit committed. Do not
  promote the tutorial's general information-operator framework into the
  core arc.

## Gated other-lectures exercise enrichment pass

T1–T3 are complete. Keep the remaining proposed pass bounded to nine
diagnostic exercise changes; do not add a chapter or open Act III:
- **E1–E5, E7–E9:** add the stable-quadratic-root, three-clock,
  alignment-lottery, median-of-means, finite-set projection,
  eigenspace-stability, condition-squaring, and criticality-implication
  exercises defined in the audit.
- **E6 / C08:** refine the existing power-iteration exercise with
  residual-norm stopping rather than increasing the exercise count.

Before implementation, resolve public/primary citations and enforce chapter
budgets by displacement. Particle optimization, full NTK/mean-field
development, chaining, constrained optimization, and method catalogs remain
branches or shelf material.

## Completed PDLT enrichment pass

- D50 is approved and implemented through a restructured four-rung C14
  ladder: moment, pair geometry, Jacobian spectrum, and depth-to-width trust.
- The zero-bias ReLU pair witness and exact
  `Var(q_L/q_0) = (1 + 5/n)^L - 1` control are claim-backed class-(a)
  studies. The page labels `5L/n` only as the small-parameter tangent.
- Historical `ch-14` remains byte-identical. New operations and claims use
  the explicitly forward-only `ch-14-r2` wheel; D34's forward-only identity
  rule applies.
- Frozen-feature dynamics now live in *Beyond This Volume*, function-space
  layer balance is a C17 exercise, the residual criticality callback is in
  C15, and dNTK/ddNTK/projector machinery remains on the shelf.
- Re-run the prose-overlap audit against the full PDLT arXiv text once that
  source is present in project knowledge; it is the one corpus gap in the
  2026-08-04 attribution review and does not block the citation repair.

## v1.0 print apparatus

- Build a real subject index.
- Derive a symbol index from the notation covenant.
- Add a theorem and named-wrong-answer index.
- Add running heads keyed to chapter titles.
- Complete the D24 tagged-PDF and reading-order validation gate.

## Completed chapter gates from the ICML 2026 source audit

- **C12 complete locally:** the disagreement witness, matrix-free action,
  bounded CG two-lens comparison, and quasi-Newton inference branch are
  implemented with explicit expectation and calibration boundaries.
- **C13 complete locally:** conditional descent, noise-to-signal ratio, batch
  assumptions, heavy-tail boundary, and clipping bias are on the page.
- **C16 complete locally:** the required CPU witness tracks top and
  gradient-direction curvature; glocal and staircase results remain branches.
- **C17 complete locally:** dual-norm geometry, rectangular polar factors,
  Newton–Schulz residuals, and the paper-autopsy endpoint are present;
  QJL/TurboQuant remains an Audit branch.

## Release identity decision — completed

- **D34 ratified:** historical C02–C17 wheels retain their content-addressed
  identities. `harness-ch-14-r2-v1` points to the committed source verified
  against the 0.18.0 wheel. Every future wheel records its commit and annotated
  source tag before publication.

## Paper-presentation menu after source verification

- Hennig (2015), *Probabilistic Interpretation of Linear Solvers*.
- Wenger et al. (2022), *Posterior and Computational Uncertainty in Gaussian
  Processes*.
- Hennig and Kiefel (2013), *Quasi-Newton Methods: A New Direction*.
- Kunstner et al. on optimizer behavior in gradient-dominated regimes and
  heavy-tailed labels.
- Fox et al. (2026) on glocal smoothness.

Add a paper to the public syllabus only after the book has introduced the
object needed to audit it.

## Named paper-audit exhibits

- **C16 staircase exhibit:** register Kim–Mishkin–Pilanci's staircase of
  connectivity as the width-indexed topology phase-transition target. Keep it
  at Paper-audit/further-reading depth under D33; use the published result as
  evidence and require the student to audit topology definition, width axis,
  finite-sample endpoint, and transfer boundary before drawing an edge-of-
  stability conclusion.

## Reproducible figure bytes

- **R17 queued:** turn the style guide's fixed environment and metadata rule
  into a mechanical two-render byte comparison. Do not normalize away a real
  dependency or source change merely to make the audit green.

## Deferred by scope

- No Act III in this volume; the unnumbered continuation map owns the course
  synthesis routes unless the author explicitly opens a separate volume.
- Full Rosetta alias redirects beyond terms actually introduced.
- Full historical harness matrix until immutable publication tags exist; the
  current and immediately previous vendored wheels already run per PR.
