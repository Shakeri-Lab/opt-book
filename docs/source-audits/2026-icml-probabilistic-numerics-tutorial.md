# Source Audit — ICML 2026 Probabilistic Numerics Tutorial

## Identity and review status

- **Presenters:** Philipp Hennig, Marvin Pförtner, and Tim Weiland
- **Title:** *Probabilistic Numerics — Computation is Machine Learning*
- **Venue:** ICML 2026 tutorial
- **Artifact:** 131-slide PDF
- **Instructor-shelf path:**
  `../Resources/2026-ICML-Probabilistic Numerics — Computation is Machine Learning.pdf`
- **Artifact size:** 11,607,920 bytes
- **SHA-256:**
  `8fc05b6b45fe938ee49ebb25ec995f338cd452abc1adff05f6bce45a2dbf3265`
- **Review completed:** 2026-07-31

All 131 slides were reviewed through extracted text and rendered page contact
sheets. The deck is **external reference-only**. It supplies a useful
interpretive seam and routes the book to primary papers. It is not the sole
support for a probabilistic numerical guarantee, calibration claim, or
historical statement.

The PDF is not copied into this public repository because its redistribution
license has not been established. The path, byte size, and digest close the
local project-knowledge provenance chain without republishing the deck.

## What the tutorial contributes

The transferable idea is not that every numerical algorithm is secretly
Bayesian. It is a disciplined question:

> What information has the computation acquired, what state represents that
> information, and what uncertainty remains because the computation stopped?

Under an explicit Gaussian prior and linear observation model, the tutorial
makes this question exact. Sequential conditioning produces rank-one
posterior covariance updates; choices of observations become computational
policies; particular policies recover familiar decompositions or iterative
linear solvers.

This complements the book's retained-state ledger. C02 asks what a streaming
algorithm must remember. The Probabilistic Numerics perspective asks what an
iterative computation has learned. The seam is useful when kept as an audit
question and dangerous when promoted into an unqualified identity.

## Integration map

| Slides | Contribution | Book destination | Decision |
|---|---|---|---|
| 4 | Error from insufficient computation versus insufficient data | C03 branch exercise | Use as an analogy whose calibration assumptions must be audited; do not conflate deterministic roundoff with posterior uncertainty. |
| 6–15 | Sequential Gaussian conditioning, rank-one covariance downdates, and Gram–Schmidt/QR | C02 branch exercise and C12 callback | Compare state machines explicitly. Do not call Welford Bayesian conditioning: the target, state, sign of the rank-one update, and probability model differ. |
| 16–20 | Observation policy, numerical stability, and conjugate gradients as active computation | C12 | Use CG as a two-lens case: Krylov/spectral dynamics and an information policy under a declared prior and SPD model. |
| 21–35 | Priors, computational uncertainty, and calibration in probabilistic linear solvers | C12 paper audit | Require the prior, observation model, posterior target, stopping rule, and calibration evidence. Do not repeat the tutorial's “zero overhead” slogan. |
| 36–57 | Information-operator framework and quasi-Newton example | C12 further reading | Use Hennig–Kiefel as a branch showing curvature estimation as inference; the chapter trunk remains curvature-object selection and diagnostics. |
| 58–75 | Quadrature and ODE examples | Optional journal club | Off the C01–C17 critical path. |
| 76–115 | PDE information operators and case study | Excluded from the core | Elegant but would require a new mathematical trunk and displace the book's training focus. |
| 117–130 | Primary-source reading map | Shelf and paper menu | Route technical claims to the cited primary papers before public use. |

## Surgical chapter touches

### C02 — State is not automatically belief

The main chapter should remain about centered, mergeable sufficient state.
One Audit exercise compares Welford's
\((n,\mu,M_2)\) with the Gaussian linear-solver state
\((\mu_i,\Sigma_i)\). The comparison must record:

- deterministic target versus latent random quantity;
- observed value and conditioning event;
- whether a prior is present;
- additive centered-moment update versus covariance downdate;
- exact output and uncertainty at early stopping.

The exercise earns the analogy while preventing the sentence “Welford is
Bayesian conditioning” from entering the trunk as an identity.

### C03 — Probabilistic error needs a probability contract

The chapter already distinguishes represented-input error, arithmetic error,
and randomized rounding. A branch exercise should now distinguish:

- a deterministic error bound;
- randomness deliberately introduced by the arithmetic;
- epistemic uncertainty induced by a prior and limited information;
- empirical calibration of an uncertainty statement.

Local unbiasedness of stochastic rounding is not a calibrated posterior over
the exact computation.

### C12 — The seam harvest

C12 is the natural harvest because it already asks which curvature operator
is being estimated. It should contain:

1. one compact CG comparison under two lenses;
2. one paper-audit branch on Gaussian interpretations of quasi-Newton
   updates;
3. a boundary stating that an algebraically identical iterate does not make
   every attached posterior calibrated.

This is enough to make probabilistic linear algebra legible without teaching
the information-operator or PDE apparatus.

## Material deliberately not imported

- Welford and Gaussian conditioning are not presented as the same algorithm.
- “Computation is inference” is not treated as a theorem without a prior,
  information operator, and conditioning model.
- Roundoff, truncation, discretization, and statistical estimation error are
  not collapsed into one undifferentiated uncertainty.
- The “zero overhead” statement for posterior output is not repeated without
  an implementation and state-cost contract.
- The full information-operator formalism, quadrature catalog, ODE material,
  and PDE case study are outside the core arc.
- A probabilistic interpretation is not presented as evidence that the
  resulting uncertainty is calibrated.

## Attribution policy

Public prose credits Hennig, Pförtner, and Weiland for the tutorial's
computation-as-inference framing. Exact linear-solver and quasi-Newton claims
route to Hennig (2015), Hennig and Kiefel (2013), and any later primary paper
used by the destination chapter. The book may claim its own pedagogical
integration—retained state → acquired information → curvature inference—but
not the underlying probabilistic interpretation.

## Revision to-do ledger

### Completed in the current revision

- [x] Review and fingerprint the complete tutorial.
- [x] Classify the material as an internal seam, not a public narrative
  thread or new chapter.
- [x] Add bounded C02 and C03 branch exercises.
- [x] Register the C02→C12 information-policy callback.
- [x] Add the tutorial and Hennig (2015) to public source credit.

### Required when C12 is contracted

- [ ] Read Hennig (2015) and Hennig–Kiefel (2013) in full.
- [ ] State the SPD, prior, observation-policy, and exact-arithmetic
  conditions behind the CG correspondence.
- [ ] Separate posterior algebra from uncertainty calibration.
- [ ] Decide whether the quasi-Newton branch remains an Audit exercise or
  earns one compact field note.
- [ ] Keep the PDE and general information-operator apparatus out of the
  chapter unless the author explicitly changes the v1 arc.
