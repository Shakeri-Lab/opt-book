# Arc, Seeds, and Harvests

## Chapter status

| Unit | Working transformation | Status |
|---|---|---|
| C01 | Diagnose runtime from bytes and reuse rather than FLOPs alone | Deep-revision witness complete; author review pending |
| C02 | Repair a one-pass variance computation by preserving centered, mergeable state | Pilot accepted; C03 handoff harvested |
| C03 | Predict floating-point failures from a precision contract | Locally complete; author review pending |
| C04 | Read gradient descent mode by mode | Locally complete; machine acceptance audit passed; author review pending |
| C05 | Turn exponential tails into simultaneous control | Locally complete; machine acceptance audit passed; author review pending |
| C06 | Diagnose the two-regime tail created by squares and products | Locally complete; machine acceptance audit passed; author review pending |
| C07 | Turn a fixed-direction tail budget into a uniform finite-cover certificate | Locally complete; machine acceptance audit passed; author review pending |
| C08 | Separate fixed-direction isotropy from adaptive singular edges | Locally complete; machine acceptance audit passed; author review pending |
| C09 | Distinguish asymptotic spectral mass from a finite null verdict | Locally complete; machine acceptance audit passed; author review pending |
| C10 | Replace ambient dimension and parameter count with effective dimension | Locally complete; machine acceptance audit passed; author review pending |
| C11 | Treat reverse derivatives as accumulation and retained-state algorithms | Locally complete; machine acceptance audit passed; author review pending |
| C12 | Name the curvature object, expectation, representation, and matrix action before interpreting a spectrum | Locally complete; machine acceptance audit passed; author review pending |
| C13–C17 | Diagnose stochastic regimes, criticality, normalization, stability, and update geometry | Deep-revision witnesses complete; author review pending |
| Coda | Diagnose the opening loss-spike incident with the complete instrument panel | Locally complete; author review pending |
| Act III | Synthesis through modern primitives | Gated after core budget evidence |

## Public threads

| Thread | Registered seed | Required callbacks | Intended harvest |
|---|---|---|---|
| Numerical stability | C02 | C03, C11, C15, C16, C17 | Stable reductions, normalization arithmetic, and update approximation |
| Random-matrix spectra | C08 | C09, C10, C12, C14, C17 | Jacobian and update spectra |
| Landscape and update geometry | C04 | C12, C13, C14, C15, C16, C17 | Stability and matrix-aware updates |
| Sub-Gaussian safe zone | C05 | C06, C08, C09, C13, C14 | Criticality and its heavy-tail boundary |

Acts before a registered seed are exempt from the silence audit. The seed
chapter itself must declare the `seed` role. From the seed onward, one whole
act may not pass without a meaningful callback.

The Coda harvests all four threads in one incident report: it rules out a
precision-scale explanation, evaluates the local curvature boundary, audits
the estimator target, compares update and weight spectra, and checks repeated
normalization state before assigning cause.

## Internal cross-cutting ledgers

| Ledger | First object | Later payoffs |
|---|---|---|
| Memory wall and retained state | C01 bytes; C02 state \((n,\mu,M_2)\) | C11 checkpointing, all-pairs tiling, online normalizers, scan |
| Orthogonality and scale | C04 eigendirections; C08 singular values | C14 isometry, C16 curvature filtering, C17 update geometry |
| Gradient signal versus estimator noise | C04 additive-noise control; C06 moment boundary | C13 regime diagnosis, C16 schedule/stability audit, C17 optimizer paper autopsy |
| Information retained and acquired | C02 state machine and branch exercise | C12 linear/curvature information policy, C17 state and approximation audit |

The last two rows remain internal. Gradient/noise balance is too concentrated
in Act II to justify a fifth public sigil, and “computation is inference” is
only exact under an explicit probabilistic model. The internal ledgers retain
the useful callbacks without increasing the reader-visible thread vocabulary.

## ICML 2026 optimization-theory integration

The complete source audit is
`docs/source-audits/2026-icml-optimization-theory-tutorial.md`. The tutorial
is an external routing source, not primary evidence. It sharpens four future
chapter obligations:

| Unit | Added diagnostic obligation |
|---|---|
| C12 | Harvested: the Hessian/GGN/model-Fisher/empirical-Fisher disagreement witness, action-only probe, bounded CG two-lens seam, and structured-approximation boundary are now on the page. |
| C13 | Harvested with executable controls: online regime crossing, batch variance scaling, exact quadratic momentum, stochastic noise amplification, and infinite-variance clipping bias are on the page. |
| C16 | Harvested: fixed control, local top curvature, gradient-direction curvature, finite-horizon history, and a matched stochastic trajectory are compared in laptop-reproducible witnesses. |
| C17 | Harvested: dual-norm geometry, polar approximation, update and weight spectra, parameter routing/scale boundaries, and the literature bridge are on the page. |

C04 now plants the distinction between its best fixed minimax step and the
best one-step move in the current gradient direction. C08 now plants the
update-spectrum versus weight-spectrum distinction. The machine-readable
obligations live in `contracts/promises.yml`.

The author-supplied peer critique recorded in
`docs/source-audits/2026-icml-course-design-critique.md` adds a trunk/branch
distinction:

- the four optimization questions and the C13 regime diagnosis stay on the
  trunk;
- PL assumptions, acceleration families, WSD, glocal implicit bias, and
  Adam-surrogate details become exercises, field notes, or further reading;
- PEP constants, silver-step schedules, coin-betting internals, and optimizer
  rankings remain off the critical path.

The exact adjudication, including corrections to the proposed PL chain and
quadratic-only acceleration interval, lives in the source audit.

## ICML 2026 Probabilistic Numerics seam

The complete source audit is
`docs/source-audits/2026-icml-probabilistic-numerics-tutorial.md`.
Probabilistic Numerics is not a new chapter or public thread. It contributes
one internal question:

> What information has this computation acquired, what state records it, and
> what uncertainty remains when it stops?

C02 and C03 carry bounded Audit exercises. C12 harvests the seam through
conjugate gradients under two lenses and a quasi-Newton paper audit. Welford
is not described as Bayesian conditioning, and probabilistic uncertainty is
not inferred from local unbiasedness alone.

## C02 seed obligations

C02 must:

- inherit the memory-wall question without pretending C01 is already written;
- seed numerical stability publicly;
- plant the retained-state ledger using the state machine
  \(h_{t+1}=F(h_t,x_{t+1})\);
- plant exact-arithmetic associativity versus floating-point reduction order;
- point forward to C03 precision, C15 normalization arithmetic, and eventual
  parallel scan without prematurely teaching those topics.

The C02→C03 handoff is contractual:

- C03 must distinguish information lost during arithmetic from distinctions
  already lost when inputs were represented.
- C03 must make unit roundoff, local spacing, range, and the
  storage/compute/accumulation contract quantitative.

Both obligations are harvested in C03. The machine-readable fulfillment lives
in `contracts/promises.yml`.

## Promise ledger

The public book promises:

- every numbered chapter begins with an inspectable phenomenon;
- every theorem names the phenomenon it explains;
- every visible code surface has Plan → Code parity;
- every book-generated number has provenance;
- every numbered chapter ends with Check yourself, five-slot recap, Sources,
  and canonical exercises;
- HTML figures have substantive alt text;
- the HTML edition is canonical and the PDF content-equivalent.

Machine ownership of these promises lives in `contracts/promises.yml`.
Cross-chapter fulfillments must now cite executable claim evidence or an
explicit prose-fulfillment flag; an owner declaration alone is insufficient.

## C04 and C05 obligations

C04 seeds landscape/update geometry with the exact mode multiplier
\(1-\alpha\lambda_k\). C16 must use the fixed quadratic boundary as a control
when curvature becomes dynamic.

C05 seeds the sub-Gaussian safe zone through an MGF proxy, independent-sum
closure, and simultaneous \(\sqrt{\log m}\) control. C06 harvests that
obligation: a square moves from global \(\psi_2\) control to local
\(\psi_1\) control, and Bernstein's constrained optimizer exposes the
quadratic-to-linear transition. C07 must now show how a finite tail budget
pays for a cover of a continuous set.

C07 harvests that obligation with a volumetric covering bound and a
deterministic interpolation rule. C08 then harvests C07's adaptive-direction
promise: fixed row projections are controlled before the matrix is observed,
while its singular vectors are selected afterward.

C08 seeds the random-matrix spectra thread with two singular edges and the
internal orthogonality/scale ledger with the criterion that an isometry has
every singular value equal to one. C09 must add the spectral mass between the
edges and a finite-size null before an outlier is called signal.

C09 harvests that obligation with an empirical spectral measure, the
Marchenko--Pastur bulk under a consistent scaling convention, an independently
seeded finite largest-eigenvalue null, and a model-specific spiked alternative.
C10 harvests C09's ambient-dimension debt with effective rank, keeps stable
rank distinct, exposes the Gaussian fourth-moment mechanism, and refuses to
turn one spectral scalar into a compression or generalization theorem.

C11 opens Act II by importing chain-rule mechanics from the sibling and owning
the systems consequence: cotangents add at fan-out, local pullbacks require
retained primal state, and uniform checkpointing makes the memory/replay trade
explicit. Its numerical-stability callback returns C02's reduction-order
lesson inside the gradient engine. C12 must compose forward and reverse
products into curvature probes without materializing a dense Hessian; C14 must
return to the product of local Jacobians across depth.
