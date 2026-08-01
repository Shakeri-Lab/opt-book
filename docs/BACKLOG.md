# Backlog

## Build-blocking

- Obtain author acceptance of the locally complete C03–C17 chapters.
- Resolve D34 before release identity is frozen. Do not backfill false
  commit/tag identities onto the sixteen C02–C17 wheels already built; their
  content-addressed artifacts remain the rolling-draft identities.
- Obtain explicit author ratification of provisional D29–D33. Their editorial
  policies are implemented, but implementation is not recorded as acceptance.
- Decide the complete-book budget from the committed C01–C17 metrics ledger
  rather than extrapolating from the C02 pilot alone.

## Cross-book

- Add `docs/public-anchors.md` and anchor CI to the sibling repository after
  explicit write authority for that repository.
- At opt-book v0.2, add reciprocal sibling pointers at the five approved
  collision surfaces.
- Add mutual colophon pointers when the new site is public.

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

## Gated other-lectures enrichment pass

Keep the proposed pass bounded to three main-text seams and nine diagnostic
exercise changes; do not add a chapter or open Act III:

- **T1 / C04:** identify the exact quadratic recurrence as explicit Euler on
  the corresponding gradient flow, with the nonlinear/stochastic boundary.
- **T2 / C05:** add a compact Gaussian Lipschitz concentration
  proof-with-pointer, including its center and distribution boundaries.
- **T3 / C12:** state and diagnose
  `kappa(J^T J) = kappa(J)^2`, then compare representation/solver contracts.
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

## Release identity decision

- **D34 pending:** choose a forward-only annotated tagging scheme for harness
  artifacts. Recommended: begin with the first wheel built from a recorded
  commit and tag (`harness-ch-12-v1` or later), never invent identities for the
  ten existing public draft wheels, and retain their SHA-256 identities.

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

## Deferred by scope

- Act III decision after core budget evidence.
- Full Rosetta alias redirects beyond terms actually introduced.
- Full historical harness matrix until immutable publication tags exist; the
  current and immediately previous vendored wheels already run per PR.
