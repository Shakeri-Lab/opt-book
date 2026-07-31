# Source Audit — ICML 2026 Optimization Theory Tutorial

## Identity and review status

- **Presenter:** Mark Schmidt, University of British Columbia
- **Title:** *Is numerical optimization theory irrelevant to machine learning
  practice in 2026?*
- **Venue:** ICML 2026 tutorial, not a workshop talk
- **Public artifact:**
  <https://www.cs.ubc.ca/~schmidtm/Documents/2026_ICML_Tutorial.pdf>
- **Artifact:** 211-slide tagged PDF
- **SHA-256:**
  `1d9c0507434d76e9206443837513d00e0a628db9b4bbbc937b5e9afa4908008e`
- **Review completed:** 2026-07-31

The supplied local PDF and the public UBC PDF are byte-identical. All 211
slides were reviewed through extracted text and rendered page contact sheets.

This deck is **external reference-only** under the book's source hierarchy. It
can identify phenomena, useful distinctions, and primary papers to audit. It
is not primary support for a theorem, benchmark endpoint, historical anecdote,
or optimizer recommendation.

## What the tutorial contributes

The tutorial's strongest idea is a hierarchy of optimization questions rather
than a catalog of methods:

1. What does a global one-step bound permit?
2. What changes when curvature is local or the gradient occupies only some
   directions?
3. What changes when the objective, curvature, or gradient-noise distribution
   evolves with the state?
4. What sequence is useful over a finite horizon, even if one step is locally
   non-monotone?

That hierarchy is highly compatible with this book. C04 already supplies the
fixed quadratic control. The tutorial shows exactly how later chapters should
break that control: conditional gradient noise in C13, moving curvature in
C16, and non-Euclidean update geometry in C17.

The tutorial also supplies a useful research posture: simple theory is
valuable when it predicts a discriminating control, exposes a changing
quantity, or explains a practical boundary. That is the book's
phenomenon-first contract stated in optimization language.

## Editorial adjudication after the course-design critique

The critique correctly identifies several gaps, but the book should use a
**trunk / branch / shelf** rule rather than expanding every gap into a
section:

- **Trunk:** the resolution of the optimization question
  (global → local → directional → horizon), the
  gradient-dominated/noise-dominated diagnosis, moving curvature at the edge
  of stability, and update geometry before optimizer branding.
- **Branch:** PL and other convergence conditions, acceleration routes,
  glocal smoothness and implicit bias, WSD, critical batch size, sign-based
  Adam surrogates, and the five proposed deep-network trade-offs. These enter
  as compact Audit exercises, field notes, or one closing table only when the
  chapter's trunk has already supplied the required object.
- **Shelf:** PEP constants, silver-step schedules, coin-betting internals, the
  variance-reduction catalog, optimizer-rejection anecdotes, and benchmark
  rankings.

Four qualifications are load-bearing:

1. The proposed chain
   `bounded below ⊃ invex ⊃ convex ⊃ PL ⊃ strongly convex` is false.
   Strong convexity implies both convexity and the PL inequality, but
   convexity and PL are not nested in either direction. A book figure must be
   a partial relation annotated by conclusions, not an inclusion chain.
2. The heavy-ball stability interval
   \(\alpha<2(1+\beta)/L\) and the Chebyshev rate belong to the exact
   positive-definite quadratic control. They do not transfer unchanged to a
   general nonquadratic objective.
3. The tutorial links separable logistic loss to shrinking local curvature.
   The additional max-margin/implicit-bias connection is a valuable synthesis,
   but it needs its own primary sources and must not be attributed to the
   tutorial as a proved consequence.
4. “Adam is momentum plus sign descent” is a surrogate analysis, not an
   anatomy theorem for AdamW. Scale invariance additionally depends on the
   precise \(\epsilon\), bias-correction, objective-rescaling, and
   \(\beta_1,\beta_2\) contract.

The gradient/noise distinction becomes an **internal diagnostic ledger**, not
a fifth public sigil. D06 deliberately limits the visual vocabulary to four
public threads. C13 will make the distinction central, and later paper audits
will reuse it without turning every chapter into a stochastic-optimization
survey.

## Integration map

| Slides | Diagnostic contribution | Book destination | Decision |
|---|---|---|---|
| 26–36 | Global smoothness, the descent lemma, and one-step step-size bounds | C04 | Keep as background ownership; do not reteach introductory gradient descent. |
| 31–32 | Convergence conclusions under convexity, invexity, PL, strong convexity, and bounded-below assumptions | C04 branch / Paper Autopsy | Use as an assumption-mapping exercise. Reject the false single-chain inclusion diagram. |
| 37–68 | Global versus local curvature, gradient-direction curvature, and finite-horizon step sequences | C04 and C16 | Add the directional line-minimizer boundary to C04; require C16 to compare global edge, local top curvature, directional curvature, and trajectory history. |
| 43–46 | Glocal smoothness and separable logistic regression | C16–C17 paper audit | Use as a local-curvature control. Add max-margin implicit bias only after separate primary-source verification. |
| 59–68 | PEP/silver steps, Chebyshev steps, BB/spectral steps, and a four-level summary | C04/C13 branches | Keep the four questions as a compact paper-reading rubric. Put constants and method details in exercises/further reading. |
| 75–92 | Expected descent under an unbiased stochastic gradient and the gradient-dominated/noise-dominated split | C13 | Make this the causal spine of C13, with assumptions and estimator definitions stated exactly. |
| 94–127 | Schedules, interpolation, averaging, WSD, mini-batching, and increasing-batch alternatives | C13 | Treat as competing repairs selected by the diagnosed regime, not as a method survey. WSD is an Audit branch. Hardware claims require a bytes/time contract. |
| 108–115 | Infinite-variance boundary and clipping bias | C13, harvesting C06 | Require a finite-second-moment check before a variance-only diagnosis; clipping is a bounded-influence repair with bias, not free robustness. |
| 129–144 | Momentum on quadratics, CG, and behavior across stochastic regimes | C13 | Use one exact quadratic momentum control and one noise-amplification audit. Treat Chebyshev steps, heavy ball, and CG as three branches off the same spectral polynomial trunk; do not add a standalone acceleration survey. |
| 145–172 | Coordinate-wise sign updates, norm geometry, rotation dependence, scale behavior, and batch-size controls | C17, with C13 support | Use a simplified update as an instrument for invariance and norm choice. Do not claim that the surrogate explains the full branded optimizer. |
| 173–177 | Matrix-norm steepest descent, polar factors, and matrix-aware updates | C17 | Central bridge from singular-value geometry to a named matrix-aware optimizer. Add rectangular-shape, approximation-error, state, and cost contracts absent from the slides. |
| 178–187 | Hessian, regularized Newton, Gauss–Newton, Fisher, empirical Fisher, and structured preconditioning | C12 and C17 | Make the distinctions explicit before comparing methods. "Second order" is not one mathematical object. |
| 188–197 | Without-replacement sampling, variance reduction, and importance sampling | C13 paper audit | Keep as finite-dataset boundary material unless a later contract gives it a causal role. |
| 198–203 | Coupled signal, curvature, sensitivity, normalization, plasticity, and edge-of-stability trade-offs | Introduction, C14–C16 | Adopt the principle that a repair can move the failure. Treat the five-item list as a research checklist, not a proved taxonomy. |
| 205–211 | Theory/practice synthesis and models with changing features | C17 recap and book conclusion | Use as a terminal audit question: which quantity evolves, which assumption carries the claim, and what control would change practice? |

## Chapter-specific contract revisions

### C04 — Preserve the control and narrow "optimal"

C04's fixed quadratic model is stronger than a generic descent-lemma recap
because it gives the exact multi-step recurrence. It should remain compact.
The revision adds one exact directional calculation:

\[
\alpha_t^{\mathrm{line}}
=
\frac{\lVert g_t\rVert_2^2}
{g_t^{\mathsf T}Q g_t},
\qquad g_t=Qe_t.
\]

This is the one-step minimizer along the current negative-gradient direction.
It separates three claims that are often collapsed:

- \(2/(\lambda_{\max}+\lambda_{\min})\) is the best **fixed minimax**
  scalar step over the full spectral interval;
- \(\alpha_t^{\mathrm{line}}\) is best for the **current direction and one
  step** in the quadratic model;
- neither is automatically best for a changing landscape, stochastic
  estimator, finite horizon, or wall-clock objective.

### C12 — Curvature is an object choice

The chapter contract must distinguish:

- the Hessian of the realized objective;
- the generalized Gauss–Newton matrix;
- the model Fisher;
- the empirical Fisher;
- diagonal, block, or Kronecker approximations.

The opening phenomenon should make two curvature matrices agree in one
controlled setting and disagree in another. The repair is not "use second
order"; it is choosing an operator whose definiteness, approximation error,
state cost, and statistical meaning match the diagnosis.

### C13 — One update, two stochastic regimes

The core witness should hold the objective and nominal step fixed while the
ratio

\[
\mathcal R_t
=
\frac{\lVert \nabla \mathcal L(w_t)\rVert_2^2}
{\mathbb E[\lVert \widehat g_t-\nabla\mathcal L(w_t)\rVert_2^2]}
\]

crosses from gradient-dominated to noise-dominated behavior. For a batch of
independent examples, the denominator's \(1/B\) scaling is a theorem only
under the declared sampling and finite-variance assumptions.

The chapter must compare repairs by mechanism:

- change step size;
- change batch size;
- average iterates or gradients;
- clip the update;
- exploit interpolation when its residual-noise assumption is actually true.

The harness must record the target gradient, conditional estimator, reduction
axes, denominator, batch sampling scheme, tail diagnostic, and uncertainty.
An accelerator throughput claim is separate from a statistical batch-size
claim.

### C14–C15 — Repairs interact

The tutorial's signal-flow/sensitivity/plasticity list is useful as an audit
prompt, not as settled theory. C14 and C15 should require every initialization
or normalization repair to report at least:

- activation scale through depth;
- Jacobian singular behavior;
- parameter-gradient scale;
- precision envelope;
- the axis and denominator of every normalization statistic.

No sentence should imply that controlling one of these quantities controls
all the others.

### C16 — The edge is a coupled trajectory

C16 must compare four instruments:

1. C04's fixed \(\lambda_{\max}(Q)\) control;
2. the local top Hessian eigenvalue
   \(\lambda_{\max}(H_t)\);
3. the gradient-direction Rayleigh quotient
   \(g_t^{\mathsf T}H_tg_t/\lVert g_t\rVert_2^2\);
4. the loss and curvature history over several updates.

The required CPU witness remains full-batch training on a small smooth
network with Hessian-vector-product power iteration. The chapter must ask
whether a loss increase is predicted by the global edge, the active
direction, or neither. A frontier-scale trace is supplementary evidence only.

### C17 — Update geometry before optimizer branding

The opening control should compare a diagonal quadratic with an orthogonally
rotated copy. Euclidean gradient descent is rotation-equivariant; a
coordinate-wise sign update is not. That makes the norm and parameterization
visible before a branded method appears.

The matrix lift then asks what update solves a steepest-descent problem under
Frobenius, nuclear, and operator-norm constraints. The polar factor becomes a
mechanism, followed by the literature bridge to matrix-aware orthogonalized
updates.

C17 must add what the tutorial necessarily compresses:

- rectangular matrices and the correct semi-orthogonality side;
- exact versus Newton–Schulz-approximated polar factors;
- residual and finite-precision diagnostics;
- parameter routing and excluded tensors;
- state bytes, matrix-multiply work, and communication;
- update-spectrum versus weight-spectrum distinction;
- controlled comparison against tuned baselines.

Quantized/sketched updates remain a paper-audit exercise unless they fit the
same causal spine without displacing the matrix-geometry argument.

## Paper Autopsy integration

Bertsekas's two cultures, the four optimization questions, and the two
stochastic regimes become three fields in the course-wide
`docs/PAPER-AUTOPSY-PROTOCOL.md`. They do not replace the existing optimizer
card. They sharpen it:

- Which evidence culture supplies the claim, and where do proof and experiment
  actually meet?
- Is the theory global, local, directional, or trajectory-level?
- Which dynamic regime do the experiments probe?
- Do the assumptions survive infinite global smoothness, heavy tails,
  non-interpolation, and moving features?

The book adds the geometric object, estimator, precision, retained state,
hardware cost, and discriminating control. That integrated protocol is the
book's pedagogy; the source ideas remain credited.

## Material deliberately not imported

- Personal quotations, tweets, rejection history, and unnamed industry
  anecdotes are not evidence for the book.
- Benchmark rankings and "method X beats method Y" claims are excluded until
  the primary protocol, tuning budget, hardware, estimator, and uncertainty
  are audited.
- The tutorial's four “levels” are retained only as four diagnostic questions
  in paper audits. They are not a branded taxonomy or a ranking of methods.
- The five deep-network trade-offs are not presented as an exhaustive or
  proved classification.
- Slide figures and screenshots are not reused. Book figures will be rebuilt
  from controlled experiments or primary-source data with permission.
- The omission of convergence rates is appropriate for a tutorial but does
  not lower the book's proof policy.

## Revision to-do ledger

### Completed in the current revision

- [x] Add the fixed/global versus directional/horizon distinction to C04.
- [x] Register C04→C13 and C04→C16 promises.
- [x] Register the C06 heavy-tail callback required in C13.
- [x] Plant C08→C17's update-spectrum versus weight-spectrum distinction.
- [x] Add the "a repair can move the failure" contract to the introduction.
- [x] Record the deck fingerprint, public source, scope, and reuse boundary.
- [x] Add the four-question resolution and two-phase fields to the Paper
  Autopsy Protocol.
- [x] Keep gradient/noise balance as an internal ledger rather than adding a
  fifth public thread.
- [x] Record the PL partial-order, quadratic-acceleration, implicit-bias, and
  Adam-surrogate corrections.

### Required when the destination chapter is contracted

- [ ] **C12:** audit primary sources for Hessian/GGN/Fisher/empirical-Fisher
  distinctions and design a controlled disagreement witness.
- [ ] **C13:** derive the conditional expected-descent inequality
  independently; validate the regime statistic under finite variance; add a
  heavy-tail failure control and clipping-bias measurement.
- [ ] **C13:** separate statistical batch scaling from accelerator throughput
  and declare the batch-sampling estimator.
- [ ] **C13:** keep WSD and critical-batch calculations as branches selected
  by the regime diagnosis; do not turn schedules into a catalog.
- [ ] **C13:** use one exact heavy-ball quadratic control and one stochastic
  noise-amplification control. Route Chebyshev and CG details to exercises or
  further reading.
- [ ] **C14–C15:** convert the interaction checklist into exact Jacobian,
  reduction-axis, and precision measurements.
- [ ] **C16:** predeclare the local CPU edge-of-stability study and track both
  top and gradient-direction curvature.
- [ ] **C16–C17:** verify primary sources before connecting glocal curvature
  decay on separable logistic regression to max-margin implicit bias.
- [ ] **C17:** test rotation and scale transformations, rectangular polar
  factors, Newton–Schulz residuals, routing, state, and cost before naming
  Muon or related methods.
- [ ] **C17:** treat momentum-plus-sign descent as a controlled Adam
  surrogate; audit AdamW's decoupled decay and scale-invariance qualifiers
  separately.
- [ ] **C17:** keep QJL/TurboQuant as an Audit exercise unless a single
  phenomenon-first spine can accommodate them without becoming a survey.

Each destination contract must replace the tutorial citation with the
appropriate primary papers for load-bearing claims. The tutorial may remain
in Sources as an intellectual map, never as the sole technical authority.
