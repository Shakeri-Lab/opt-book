# Backlog

## Build-blocking

- Obtain author acceptance of the locally complete C03–C09 chapters.
- Pin the C02–C09 harness wheels to real source commits and annotated tags
  after commit authority is granted. Their content-addressed wheels are
  already vendored; only publication identities are intentionally absent.
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

## Deferred by scope

- C01 and C10–C17 contracts.
- Act III decision after core budget evidence.
- Full Rosetta alias redirects beyond terms actually introduced.
- Full historical harness matrix until immutable publication tags exist; the
  current and immediately previous vendored wheels already run per PR.
