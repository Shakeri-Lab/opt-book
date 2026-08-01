# Source Audit — “Others lectures” Shelf

## Identity and review status

- **Shelf location:** instructor-supplied `Others lectures/` directory
- **Review completed:** 2026-08-01
- **Role:** external reference-only and course-comparison material
- **Decision rule:** enrich the existing C01–C17 trunk only when a source adds a
  missing diagnostic object; otherwise route it to an exercise, Paper audit,
  further reading, or the shelf

The audit covered the complete lecture sequence in each supplied collection:

| Collection | Reviewed lecture units | Group fingerprint |
|---|---:|---|
| Baek, *Numerical Analysis and Optimization* | 10 PDF lecture decks plus the matrices/tensors deck; assignments, midterm, and final-project prompts screened | 37 files; `2bbef07db307332ab7d207ec2ab509064f1fd4cfcda6d94895d262e9297ed027` |
| Daneshmand | 7 PDF lecture decks; companion probability notes screened | 8 files; `96ba292f07c8d3c22ba7f385371414a57a6fffbc08ab69743cb80dcc5b453410` |
| Speicher, *Random Matrices and Machine Learning* | 10 TeX lecture sources | 10 files; `735cda96bdf3d435c37ee9a66947be72108ef9762569e94f24b00b313759b5ca` |
| RY book drafts | 3 TeX chapter sources | 3 files; `9682338860721ca16d44eb02674e0ad1a09c87e2d90d3332c731de80b588acee` |
| Vershynin course files | 42 numbered TeX lectures plus wrapper and plan files | 48 files; `541a687afc5ee59a4fd02b2abdfdb953d4e23212a39386f8330c910caae2957d` |

Each fingerprint is the SHA-256 of a sorted manifest containing the relative
path and SHA-256 of every file in that collection. It identifies the reviewed
shelf state without treating privately supplied files as publishable sources.
The Baek and Daneshmand lecture PDFs were extracted in full; their outlines,
examples, and representative rendered pages were inspected. All numbered TeX
lectures in the other three collections were indexed by section and theorem,
with the parts relevant to C01–C17 read closely. The large Heath textbook and
ancillary readings were indexed rather than reread cover to cover. Assignment
prompts were used only to detect exercise ideas and duplication.

No figure, slide prose, or exercise wording is approved for copying. Public
chapters must cite the appropriate primary or canonical source for a technical
claim. This audit credits the supplied lectures for routing and course-design
ideas.

## Executive verdict

The shelf does **not** justify another chapter or a second mathematical spine.
The book already owns most of its useful numerical-analysis and random-matrix
material. The high-value harvest is deliberately bounded:

1. add three short main-text seams: gradient descent as an explicit
   discretization, nonlinear Gaussian concentration, and the conditioning cost
   of normal equations;
2. add or refine nine exercises whose solutions require diagnosis rather than
   method recall;
3. keep particle optimization, full kernel limits, chaining, semidefinite
   relaxations, constrained optimization, optimizer catalogs, and the full
   numerical-ODE apparatus off the trunk.

The additions strengthen existing callbacks instead of interrupting the arc.
They also prepare C17's paper-reading endpoint: a student meets random
projection, robust estimation, numerical conditioning, and implication audits
as usable instruments before encountering them in a current paper.

## Collection-by-collection adjudication

### Baek — classical numerical analysis as controlled counterexamples

The numerical-error, linear-algebra, eigenvalue, differentiation, ODE, and
optimization decks contain the most directly reusable material. Most of the
trunk is already owned by C02–C04, C08, C11, and C12: cancellation, condition
numbers, power iteration, finite-difference checks, and quadratic dynamics do
not need to be taught twice.

Three ideas survive displacement:

- the stable quadratic-root rearrangement is a compact C03 exercise in forward
  error versus backward residual;
- explicit and implicit Euler applied to one decaying eigenmode make C04's
  stability polynomial visible as a discretization choice;
- Gauss–Newton and least-squares material supplies the clean warning that
  forming \(J^{\mathsf T}J\) squares the condition number.

Root-finding catalogs, quadrature rules, multistep ODE methods, KKT mechanics,
and branded optimization-method surveys remain on the shelf. The introductory
matrices/tensors deck is sibling-volume material. The final-project prompt's
competition and hidden-test emphasis is not imported: this book's assessment
contract rewards a declared estimator, a falsifying control, and a boundary.

### Daneshmand — approximation becomes a geometric lottery

The random-feature lectures contribute one memorable branch: among \(N\)
random directions in dimension \(d\), the best squared alignment is only of
order \(\log N/d\) under the usual isotropic model. Constant alignment therefore
requires exponentially many random trials. This is an excellent exercise
because it forces students to combine a fixed-direction tail with a union
bound, then audit what normalization and independence were assumed.

The later move from fixed random features to adaptive particles is valuable
research context but too large for the core. Kernel universality, Barron-space
development, and the particle/mean-field program belong to a future Paper
audit or Act III decision, not a detour inside Act I. The dimension-free
gradient-descent comparison overlaps C04 and should not be repeated.

### Speicher — a nonlinear extension of the safe zone

The most important missing theorem on the shelf is Gaussian Lipschitz
concentration. C05 currently teaches concentration for linear combinations;
the nonlinear statement explains why a Lipschitz diagnostic of a Gaussian
input can remain concentrated without being a sum on the page. A brief
proof-with-pointer statement belongs in C05, with two boundaries stated next
to it: concentration around a center does not identify the center, and the
Gaussian theorem does not automatically transfer to arbitrary dependent or
heavy-tailed inputs.

Near-orthogonality of many random directions supports the Daneshmand alignment
exercise. The longer Gaussian-rotation, volume, chaining, free-probability,
neural-Gaussian-process, and width-scaling developments remain further reading
unless a later phenomenon creates a precise need.

### RY drafts — use the overclaims as an audit instrument

The mean-field and kernel drafts are most useful pedagogically where their
scalar statements tempt an invalid matrix conclusion. Preserving a variance
recursion, a correlation statistic, or a mean-square Jacobian stretch does not
by itself establish that the full Jacobian is an isometry. Likewise, a dtype
“depth horizon” is not universal unless the analysis declares subnormals,
flush-to-zero behavior, loss scaling, accumulation dtype, and the relevant
directional dynamics.

Rather than importing those claims into C14, the book should turn them into an
implication-graph exercise. Students must prove each proposed arrow or give a
counterexample and name the missing assumption. The NTK and mean-field
developments stay at Paper-audit depth.

### Vershynin files — a routing index, not an authority

The local TeX collection routes cleanly to median-of-means, Johnson–Lindenstrauss,
Gaussian Lipschitz concentration, matrix concentration, Davis–Kahan
perturbation, and Tracy–Widom edge fluctuations. Those routes expose useful
exercise gaps in C05–C10.

The collection is not safe to cite as a technical authority without provenance
and version resolution. It also contains several claims that require repair:

- a Gaussian covariance exercise invokes a bounded-summand matrix-Hoeffding
  interface even though Gaussian outer products are unbounded;
- an “effective rank” lecture uses a half-trace counting statistic that
  conflicts with this book's committed
  \(r_{\mathrm{eff}}(A)=\operatorname{tr}(A)/\lVert A\rVert_{\mathrm{op}}\)
  covenant;
- a spiked-edge exercise leaves its parameterization and threshold ambiguous;
- several stability percentages are presented without the eigengap and norm
  assumptions needed to justify them.

These are useful warnings for the book's Audit exercises. Any theorem promoted
to the manuscript must be independently derived and routed to a stable public
source.

## Main-text seams: the complete proposed trunk change

| ID | Destination | Addition | Why it earns the space | Boundary |
|---|---|---|---|---|
| T1 | C04, immediately after the exact mode recurrence | One paragraph identifying \(e_{k+1}=(I-\alpha Q)e_k\) as explicit Euler applied to \(\dot e=-Qe\); the stability polynomial is \(1-\alpha\lambda\) | Unifies numerical stability and optimization dynamics with an object already on the page | Do not imply that a nonlinear stochastic training trajectory is its continuous gradient flow |
| T2 | C05, after simultaneous sub-Gaussian control | A short proof-with-pointer Gaussian Lipschitz concentration result | Extends the safe zone from sums to nonlinear diagnostics and prepares spectral observables | State the center and distribution assumptions; do not market it as a heavy-tail or dependence theorem |
| T3 | C12, after “Object, representation, solver” | If \(J\) has nonzero singular values, \(\kappa_2(J^{\mathsf T}J)=\kappa_2(J)^2\); forming normal equations changes the numerical contract | Makes solver representation diagnostically consequential and connects C03 precision to curvature | QR/LSQR/matrix-free methods avoid explicit squaring but have their own cost and stopping contracts; damping changes the solved system |

These seams should consume no more than about 1.5 derived-PDF pages in total.
The finite-set projection result needed by C17 is kept as an exercise rather
than becoming a fourth exposition branch.

**Implementation disposition (2026-08-01).** T1–T3 are now on the manuscript
trunk. C04 identifies the fixed-quadratic recurrence as explicit Euler and
states the nonlinear/stochastic boundary. C05 states Gaussian Lipschitz
concentration around the mean as a proof-with-pointer to Vershynin's
second-edition Theorem 5.2.3. C12 derives the full-column-rank
$\kappa_2(J^{\mathsf T}J)=\kappa_2(J)^2$ identity and keeps QR, LSQR,
matrix-free action, damping, cost, and stopping boundaries visible. The
exercise package remains separately gated.

## Exercise enrichment package

Each item is designed as a branch off an object already introduced. New work
should displace a weaker or overlapping exercise if the chapter would exceed
its existing budget.

| ID | Chapter and tag | Proposed task | Learning elevation and acceptance boundary |
|---|---|---|---|
| E1 | C03 — **(Pencil.) (Code.) Stable quadratic roots** | Compare the direct quadratic formula with \(q=-\tfrac12(b+\operatorname{sign}(b)\sqrt{b^2-4ac})\), \(x_1=q/a\), \(x_2=c/q\) across a cancellation regime | Report forward error and polynomial residual separately. Adapt the mathematical idea; do not copy Heath's wording or table |
| E2 | C04 — **(Pencil.) (Code.) One mode, three clocks** | Compare \(e^{-h\lambda}\), explicit Euler \(1-h\lambda\), and implicit Euler \(1/(1+h\lambda)\) | Separate stability, one-step approximation error, and cost per step; “unconditionally stable” must not be confused with exact or free |
| E3 | C05 — **(Pencil.) (Code.) Alignment lottery** | Bound the best alignment among \(N\) independent random normalized directions in \(\mathbb R^d\), then reproduce a finite-\(d\) instance | Show why constant alignment requires exponential \(N\), with normalization, constants, failure probability, and independence declared |
| E4 | C06 — **(Code.) (Audit.) Robust without changing the target** | Compare the mean, a median-of-means estimator, and clipping under a finite-variance heavy tail; add an infinite-variance control | State the finite-variance gate. Clipping changes the estimand; median-of-means changes the estimator. Do not claim a variance guarantee when variance is infinite |
| E5 | C07 — **(Pencil.) (Code.) Finite set, cheaper than a sphere** | Derive a Johnson–Lindenstrauss dimension from fixed-pair concentration plus a union bound over pairs; verify it numerically | End with the C17 QJL handoff, while explicitly refusing to infer a quantization guarantee from an unquantized projection theorem |
| E6 | C08 — refine the existing power-iteration exercise | Add residual-norm stopping and compare it with Rayleigh-quotient stagnation | Diagnose the roles of eigengap and initial alignment; no extra exercise count is needed |
| E7 | C10 — **(Pencil.) (Audit.) Estimation error is not subspace error** | Use a Davis–Kahan bound and construct matrices with matched operator perturbation but different eigengaps | Show that effective rank and covariance error do not determine eigenvector stability by themselves |
| E8 | C12 — **(Code.) (Audit.) Do not square conditioning by accident** | Build a controlled \(J\) with singular values \(1\) and \(\varepsilon\); compare normal equations with QR or LSQR in FP32 | Report residual and forward error, not only convergence. The generated problem and stopping rule are part of the claim |
| E9 | C14 — **(Audit.) Criticality implication graph** | Audit arrows among moment preservation, correlation preservation, mean-square Jacobian stretch, full isometry, and dtype representability | Prove each arrow or give a counterexample and the additional assumption needed. This is the preferred use of the RY material |

## Useful material deliberately left as branches or shelf items

- **C08/C10 branch:** compare the epsilon-net and trace-MGF proof interfaces
  for a matrix deviation bound; focus on what assumptions each interface
  exposes rather than reproducing both proofs.
- **C09 further reading:** Tracy–Widom edge scaling and its finite-size/model
  qualifications. Do not make it a core code exercise before the null model is
  declared.
- **C16 Paper audit:** compare a frozen-kernel control with a moving-feature
  trajectory; do not turn the chapter into an NTK survey.
- **Act III gate:** adaptive particles, Barron spaces, and mean-field limits
  may become a synthesis branch only if D02 opens that act.
- **Shelf:** full chaining, optimal transport, semidefinite relaxation and
  Grothendieck machinery, VC/uniform-convergence sequences, root-finding and
  quadrature catalogs, multistep ODE solvers, constrained-optimization
  mechanics, and optimizer zoos.

## Credit and primary-source routing

The future manuscript should credit a lecture collection only for an
intellectual map or exercise inspiration, subject to the author's permission
and a verified public identity. Load-bearing statements should route as
follows:

- Gaussian Lipschitz concentration and random-direction geometry: a canonical
  high-dimensional-probability source, pinned by edition;
- median-of-means: the original line of work or a modern primary treatment
  with the exact finite-variance statement used;
- Johnson–Lindenstrauss: the original lemma or a canonical proof source;
- subspace perturbation: Davis–Kahan or a precise modern variant;
- least-squares conditioning: a canonical numerical-linear-algebra source;
- mean-field or kernel-limit claims: the relevant primary paper, with the
  infinite-width and time-horizon assumptions on the page.

The current `references.bib` should be checked before implementation so that
edition-sensitive chapter and theorem pointers do not inherit the local
Vershynin files' numbering.

## Implementation order and acceptance gate

1. Implement T1–T3 first and confirm that each creates a callback rather than
   a tangent.
2. Add E1–E5, E7–E9 one chapter at a time; refine rather than append for E6.
3. Re-run each affected chapter's evidence, promise, theorem, thread, and
   dual-edition audits.
4. Enforce the current chapter page budgets by displacement.
5. Record public citations only after primary-source and license verification.

This source audit completes shelf fingerprinting and exercise deduplication.
It does **not** authorize copying, expand Act III, or mark the proposed
manuscript changes as author-accepted.
