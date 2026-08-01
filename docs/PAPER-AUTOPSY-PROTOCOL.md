# Paper Autopsy Protocol

## Purpose

This protocol is the book's recurring interface between a mathematical trunk
and a current research paper. It is not a literature-summary template. Its
job is to determine what a claim rests on, what the evidence actually probes,
and which control could make the diagnosis fail.

The protocol combines three sources:

- the Spring 2026 optimizer-card, preregistration, and negative-result
  practices already used by DS 6210 students;
- Bertsekas's contrast between theoretical and experimental optimization
  cultures, as foregrounded in Mark Schmidt's ICML 2026 tutorial;
- Schmidt's distinction among global, local, directional, and
  finite-horizon optimization questions, together with his
  gradient-dominated/noise-dominated diagnostic.

The book's contribution is the integration: every autopsy also carries the
geometric object, estimator, numerical representation, retained state,
hardware cost, and falsifying control required by this course. Credit the
tutorial for its intellectual map and the primary paper for technical claims.
Do not attribute the book's combined checklist to either source.

## The full card

### 1. Claim

Write the strongest claim as one sentence with an active verb. Separate what
is proved, measured, interpreted, and merely proposed.

### 2. Mathematical object

Record shapes, parameterization, objective, update, norm, spectrum, and any
population/sample distinction. A branded method name is not an object.

### 3. Resolution of the theory

Locate the analysis at the finest level it actually supports:

1. a global one-step bound;
2. a local or state-dependent bound;
3. a direction- or geometry-aware bound;
4. a finite-horizon or trajectory-level statement.

These are questions, not a universal hierarchy of method quality. A paper may
answer several, and a higher-numbered question is not automatically better.
For any approximation, also record its small parameter, retained or
truncation order, and order of limits. “Infinite width” is incomplete until
the treatment of depth, sample size, and training horizon is named.

### 4. Dynamic regime

State what phase the argument and experiment probe:

- gradient-dominated or noise-dominated;
- interpolating or persistently noisy;
- light-tailed or outside a finite-second-moment model;
- fixed-feature or feature-learning;
- fixed curvature or moving curvature.

If the paper does not measure the proposed regime, record that as missing
evidence.

### 5. Evidence culture and interface

Identify whether the support is a theorem, derivation, controlled experiment,
benchmark comparison, or mixed argument. Then ask where the theoretical and
experimental parts meet: which measured quantity corresponds to which
assumption or conclusion?

### 6. Estimator and comparison contract

Record the target, estimator, reduction axes, denominator, uncertainty,
sampling scheme, seeds, tuning budget, baseline budget, and number of looks.
Name any nonlinear aggregate for which naive batching changes the target.

### 7. Numerical and hardware contract

Record dtype roles, rounding, scaling, device, retained state, bytes moved,
matrix work, communication, and wall-clock protocol. Do not infer hardware
speed from an iteration count.

### 8. Assumption stress test

Ask which conclusion survives when one load-bearing assumption is changed:

- global smoothness is infinite or grossly conservative;
- the second moment is not finite;
- interpolation fails;
- the active direction avoids the top-curvature direction;
- features, curvature, or the data distribution move;
- the probabilistic prior or calibration model is misspecified.

### 9. Discriminating control

Design the smallest control that could separate the proposed mechanism from
its strongest rival explanation. Predeclare the direction of the result under
both explanations.

### 10. Transfer verdict

Conclude with exactly three lines:

- **Supported:** the strongest claim that survives the audit.
- **Not supported:** the tempting stronger claim.
- **Next test:** the cheapest experiment or derivation that would change the
  verdict.

## Use without turning the book into a survey

A chapter-level paper-audit exercise selects the four to six fields that
activate machinery already earned in that chapter. The C17 capstone and any
standalone handout use the full card. A method that requires substantial new
notation or a detached proof belongs in further reading or an optional
journal-club menu unless it becomes the causal spine of a chapter.

The protocol is therefore a branch interface, not a second table of contents.
