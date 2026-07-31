# Arc, Seeds, and Harvests

## Chapter status

| Unit | Working transformation | Status |
|---|---|---|
| C01 | Diagnose runtime from bytes and reuse rather than FLOPs alone | Contract pending |
| C02 | Repair a one-pass variance computation by preserving centered, mergeable state | Pilot accepted; C03 handoff harvested |
| C03 | Predict floating-point failures from a precision contract | Locally complete; author review pending |
| C04 | Read gradient descent mode by mode | Locally complete; acceptance audit passed |
| C05 | Turn exponential tails into simultaneous control | Locally complete; acceptance audit passed |
| C06 | Diagnose the two-regime tail created by squares and products | Locally complete; acceptance audit passed |
| C07 | Turn a fixed-direction tail budget into a uniform finite-cover certificate | Locally complete; acceptance audit passed |
| C08 | Separate fixed-direction isotropy from adaptive singular edges | Locally complete; acceptance audit passed |
| C09 | Distinguish asymptotic spectral mass from a finite null verdict | Locally complete; acceptance audit pending |
| C10 | Replace ambient dimension and parameter count with effective dimension | Arc approved; contract pending |
| C11–C17 | Diagnose optimization dynamics and modern update claims | Arc approved; contracts pending |
| Act III | Synthesis through modern primitives | Gated after core budget evidence |

## Public threads

| Thread | Registered seed | Required callbacks | Intended harvest |
|---|---|---|---|
| Numerical stability | C02 | C03, C11, C14, C15 | Stable reductions and normalization arithmetic |
| Random-matrix spectra | C08 | C09, C10, C12, C14 | C16–C17 curvature and update geometry |
| Landscape and update geometry | C04 | C12, C13, C14 | C16–C17 stability and matrix-aware updates |
| Sub-Gaussian safe zone | C05 | C06, C08, C09, C13 | C14 initialization and its heavy-tail boundary |

Acts before a registered seed are exempt from the silence audit. The seed
chapter itself must declare the `seed` role. From the seed onward, one whole
act may not pass without a meaningful callback.

## Internal cross-cutting ledgers

| Ledger | First object | Later payoffs |
|---|---|---|
| Memory wall and retained state | C01 bytes; C02 state \((n,\mu,M_2)\) | C11 checkpointing, all-pairs tiling, online normalizers, scan |
| Orthogonality and scale | C04 eigendirections; C08 singular values | C14 isometry, C16 curvature filtering, C17 update geometry |

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
C10 must now replace C09's ambient dimension in covariance estimation with
effective rank and explain why trace mass can be much smaller than parameter
count.
