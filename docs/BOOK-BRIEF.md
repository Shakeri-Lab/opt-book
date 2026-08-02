# Book Brief

## Identity

**Title:** *Deep Learning: Making It Trainable*
**Subtitle:** *Geometry, Dynamics, and the Machine*

**Course:** DS 6210 — Computation II: Numerical Analysis & Optimization
**Public alias:** Algorithms for Deep Learning
**Author:** Heman Shakeri, School of Data Science, University of Virginia

This is the advanced sibling to *Deep Learning: Making It Learnable*. The
sibling owns first-course model mechanics. This volume owns the mathematical,
dynamic, numerical, and hardware diagnoses that explain why a training
computation succeeds or fails.

## Reader and terminal capability

The reader is a mathematically mature graduate student who knows linear
algebra, probability, Python, and NumPy. A prior deep-learning course is not a
prerequisite. The unnumbered On-Ramp supplies a short diagnostic, three
targeted repair stops in the earlier sibling volume, and one minimal training
loop before Chapter 1.

By the end of the book, the reader can inspect a current paper,
implementation, or training trace and identify:

1. the geometric assumption;
2. the optimization dynamic;
3. the numerical and hardware constraint;
4. the estimator behind the evidence;
5. the regime in which the conclusion is valid;
6. a discriminating control that could falsify the proposed diagnosis.

## Thesis and recurring question

**Thesis:** Training behavior is jointly determined by high-dimensional
geometry, optimization dynamics, and the arithmetic and data movement of the
machine.

**Recurring question:** What mathematical and physical conditions make a
modern learning system trainable, and which diagnostic tells us which
condition failed?

## Pedagogical contract

The native move is:

> Problem → Prediction → Instrumentation → Diagnosis → Theory → Solution →
> Audit → Recap

Definitions arrive when the reader needs them. A theorem earns its place by
naming the phenomenon it explains. Code exposes the mathematical mechanism
before wrapping it in the evolving harness. Familiar branded terms appear
only after the reader owns the primitive and needs a bridge into the
literature.

## Three lenses

- **Geometric:** What does high dimension make typical? Which directions,
  spectra, ranks, or alignments control the arena?
- **Dynamic:** Which modes decay, amplify, oscillate, stall, or cross a
  stability boundary under the update?
- **Algorithmic and systems:** Which state is retained, which bytes move, what
  precision is available, and does the implementation preserve the
  mathematical contract?

One lens may be intentionally quiet in a chapter. The chapter contract must
say so, and the public chapter carries a one-line primary/supporting/quiet
ledger below its thread sigil.

## Core arc

- **Act 0 — The computational arena:** memory traffic, streaming state,
  floating-point behavior, and quadratic control experiments.
- **Act I — Geometry of high dimensions:** concentration, sub-exponential
  boundaries, finite nets, random operators, spectral laws, and effective
  rank.
- **Act II — Dynamics of optimization:** reverse accumulation, curvature,
  stochastic regimes, criticality, normalization, edge of stability, and
  matrix-aware updates.

The numbered v1 core ends with C17. An unnumbered Coda then reopens the loss
spike from the first page and requires the separate instruments to diagnose
one event together. The final appendix hands the blank incident report to the
reader as a reusable instrument. An unnumbered *Beyond This Volume* map routes
the course's architecture-facing synthesis without opening an Act III or
turning the book into an architecture survey.

## Public narrative threads

1. Numerical stability.
2. Random-matrix spectra.
3. Landscape and update geometry.
4. The sub-Gaussian safe zone.

Memory/retained state and orthogonality/scale remain internal cross-cutting
ledgers until evidence shows that six public sigils remain readable.

## Code, evidence, exercises, and hardware

- One `harness/` package grows by chapter. The first package is born with C02.
- Every visible code surface uses numbered Plan → Code markers.
- Printed studies show the equation, a 10–25 line mechanism kernel, critical
  assertions, and a compact provenance strip. Repeated verification machinery
  lives in `book_support/claims.py` and linked source, not learner-visible code.
- Every printed numerical claim has a claim ID and provenance.
- Every chapter keeps a laptop-CPU witness. Accelerator-only endpoints use
  committed, content-addressed artifacts.
- Exercise tags remain exactly **(Pencil.)**, **(Code.)**, and **(Audit.)**.
  Profiling is Code; paper reading is Audit.
- Every research-facing act includes a paper-audit exercise.
- Every numbered chapter carries at least five exercises, including Pencil,
  Code, and Audit work; Check-yourself boxes pose questions rather than print
  their solutions.
- Exercises follow a Core/Extension/Research route with time, prerequisites,
  deliverable, and hint status. C04, C10, and C17 carry cumulative Incident
  Card checkpoints.
- Paper audits use the compact fields in
  `docs/PAPER-AUTOPSY-PROTOCOL.md`. Chapter exercises select only the fields
  activated by the chapter; the C17 capstone uses the full card.

## Refusals

This book is not:

- a harder rewrite of the sibling;
- a conventional neural-network primer or a second architecture survey; the
  On-Ramp owns only the minimum mechanics needed to enter Chapter 1;
- an optimizer or architecture catalog;
- a conventional numerical-analysis encyclopedia;
- a theory book that ignores representation error or data movement;
- a systems book that treats assumptions and spectra as decoration.

## Editions, budget, and publication

HTML is canonical. Two content-equivalent PDFs are derived: a recto-aware
print edition and a continuous screen edition without intentional blank
versos. Differences are limited to layout. C02 has a provisional cap of approximately
6,500 prose words and 22 derived-PDF pages; the complete edition budget will
be set from the measured pilot.

Drafts use `v0.x`; `book-v0.2.0` is the first fixed, annotated public-draft
release; v1.0 is the first complete edition. Text/figures use CC BY-NC-SA 4.0
and code uses MIT, subject to the source audit. Both detached PDFs carry the
rights statement in their text layer.

The introduction is unnumbered front matter. C01–C17 alone own chapter numbers
1–17, including while an earlier chapter remains unwritten.

## Approved planning baseline

The author instructed the build to proceed on 2026-07-30. Recommendations in
Build Plan v2 therefore become the working defaults recorded in
`docs/DECISIONS.md`. Later author instructions explicitly authorized routine
commits and pushes. The author ratified D29–D50 on 2026-08-01; the
publication-readiness pass approves D51–D53, with D54 left open. D34 now uses
a forward-only annotated source-tag contract without inventing identities for
historical rolling-draft wheels.
