# Backlog

## Build-blocking

- Obtain author acceptance of the locally complete C03–C12 chapters.
- Resolve D34 before the next harness wheel is built. Do not backfill false
  commit/tag identities onto the eleven C02–C12 wheels already built; their
  content-addressed artifacts remain the rolling-draft identities.
- Obtain explicit author ratification of provisional D29–D33. Their editorial
  policies are implemented, but implementation is not recorded as acceptance.
- Decide the complete-book budget from the five measured chapters rather than
  extrapolating from the C02 pilot alone.

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
- Complete shelf fingerprinting and exercise deduplication.
- Record student-work permissions before public reuse.
- Route the ICML 2026 optimization-theory tutorial's remaining load-bearing
  claims to primary papers at C13, C16, and C17 contract time; do not cite the
  tutorial as sole technical authority.
- C12 has routed the Probabilistic Numerics seam to Hennig (2015) and
  Hennig–Kiefel (2013), with its primary-source audit committed. Do not
  promote the tutorial's general information-operator framework into the
  core arc.

## Future chapter gates from the ICML 2026 source audit

- **C12 complete locally:** the disagreement witness, matrix-free action,
  bounded CG two-lens comparison, and quasi-Newton inference branch are
  implemented with explicit expectation and calibration boundaries.
- **C13:** independently derive the conditional expected-descent inequality;
  measure gradient signal, estimator variation, batch scaling, heavy-tail
  failure, and clipping bias. Use one exact quadratic momentum control and
  one noise-amplification control; keep WSD, critical batch size, Chebyshev
  schedules, and CG details in exercises/further reading.
- **C16:** track both top-Hessian and gradient-direction curvature in the
  required CPU edge-of-stability study. Use glocal smoothness only as a
  control or paper-audit branch; verify the separate implicit-bias sources
  before making a max-margin connection. Name and adjudicate the KMP
  staircase in the C16/C17 contracts so the tutorial-review lead is not lost.
- **C17:** test rotation and scale transformations, rectangular polar
  factors, Newton–Schulz residuals, parameter routing, state bytes, and
  hardware work. Treat momentum-plus-sign descent as an Adam surrogate, not
  a complete AdamW explanation. Keep QJL/TurboQuant as a paper audit unless
  they fit the matrix-geometry spine without displacement.

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

## Deferred by scope

- C01 and C13–C17 contracts.
- Act III decision after core budget evidence.
- Full Rosetta alias redirects beyond terms actually introduced.
- Full historical harness matrix until immutable publication tags exist; the
  current and immediately previous vendored wheels already run per PR.
