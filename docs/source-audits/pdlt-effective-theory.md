# Source Audit — *The Principles of Deep Learning Theory*

## Identity and review status

- **Work:** Daniel A. Roberts and Sho Yaida, *The Principles of Deep
  Learning Theory: An Effective Theory Approach to Understanding Neural
  Networks*, with contributions by Boris Hanin
- **Public versions:** arXiv:2106.10165v2 (2021); Cambridge University Press
  (2022), DOI `10.1017/9781009023405`
- **Reviewed artifact:** 470-page arXiv v2 PDF on the instructor resource shelf
- **Artifact SHA-256:**
  `6ab6379a4e5ed670ca4b5c7e8714903bf4b96a11078a9cc5fa71603d85e33874`
- **Review completed:** 2026-08-01
- **Role:** derivational companion and routing source, not sole technical
  authority for a load-bearing manuscript claim

The arXiv record lists Roberts, Yaida, and Hanin as authors. The published
book lists Roberts and Yaida as authors and “with contributions by Boris
Hanin.” The bibliography must match the version cited rather than silently
mixing the two forms.

The review covered the complete contents and framing; Chapters 0, 3–5, 9–11,
the opening and relevant conclusions of *The End of Training*, Appendix B,
and the corresponding references were read closely. The single-input,
two-input, fluctuation, finite-angle, frozen-kernel, representation-learning,
and residual-criticality pages were extracted in full. Representative pages
containing the two susceptibilities, the finite-angle asymptotics, and the
normalized four-point law were also inspected as rendered pages rather than
only through text extraction.

The local PDF already satisfies the request to place arXiv:2106.10165v2 in
project knowledge. It should remain a fingerprinted instructor resource, not
be copied into the public repository.

## Executive verdict

PDLT should not become a second theoretical spine. Its best contribution is a
four-rung diagnostic ladder inside C14:

1. a one-input moment asks whether magnitude survives;
2. a two-input map asks whether distinctions between inputs survive;
3. a Jacobian spectrum asks whether derivative directions survive;
4. a depth-to-width ratio asks whether the limiting calculation itself can be
   trusted.

This ladder extends the chapter's existing thesis without turning the book
into a kernel-limit survey. Two new laptop witnesses earn trunk space, but
both need corrections from the proposed form:

- the ReLU two-input witness should show preserved norm alongside collapsing
  pair separation at the critical scale; changing only the zero-bias ReLU
  weight scale does **not** create three different normalized-correlation
  regimes;
- the finite-width witness should show an exact finite-\(n\) control and the
  small-\(L/n\) tangent; it should not present linear
  growth as valid after the perturbative parameter stops being small.

The remaining material belongs in short interpretations, strengthened
exercises, the existing *Beyond This Volume* map, or the shelf. PDLT's deepest
transferable habit is not its physics vocabulary. It is the rule that a clean
approximation must name its small parameter, retained order, and order of
limits.

## What PDLT actually establishes in the relevant model

### One input and two inputs are different contracts

PDLT Chapter 5 first evolves a diagonal kernel component and then decomposes a
two-input kernel into magnitude and separation perturbations. Its general
criticality conditions are two slope conditions,

\[
\chi_{\parallel}(q_\star)=1,
\qquad
\chi_{\perp}(q_\star)=1.
\]

The first controls perturbations of the one-input magnitude. The second
controls infinitesimal pair separation and is the factor that reappears in the
backward chain-rule calculation. They coincide for the scale-invariant
piecewise-linear family, but they are not generically the same derivative.
That distinction repairs the tempting slogan that forward criticality
automatically proves gradient preservation.

For zero-bias ReLU, \(q_{\ell+1}=\sigma_w^2q_\ell/2\), so
\(\sigma_w^2=2\) preserves the one-input moment. For two equal-norm inputs
with normalized correlation \(c_\ell\), however, homogeneity cancels the
weight scale:

\[
c_{\ell+1}
=\frac{\sqrt{1-c_\ell^2}
 +(\pi-\arccos c_\ell)c_\ell}{\pi}.
\]

Thus the three weight scales already used in C14 produce three magnitude
stories but the same normalized-correlation map. At the critical ReLU scale,
the diagonal moment stays fixed while the finite angle tends toward alignment.
PDLT's finite-angle analysis gives angle \(\psi_\ell\asymp 1/\ell\), hence
pair-separation energy of order \(1/\ell^2\). The memorable house sentence is
therefore valid in a corrected form:

> The structure kept every norm and slowly lost the difference between its
> inputs.

This is a power-law failure, not the proposed below/critical/above three-phase
picture. An ordered/chaotic three-regime comparison requires a different
activation-and-bias family, such as a carefully tuned smooth saturating model,
and would cost more theory than this chapter needs.

### The depth-to-width law has an exact control

C14's ReLU model admits a particularly clean calculation that should precede
any Monte Carlo panel. Let

\[
q_\ell=\frac1n\sum_{i=1}^n (h_i^{(\ell)})^2
\]

and use independent Gaussian weights of variance \(2/n\), zero bias, and ReLU.
Conditional on the current layer,

\[
\frac{q_{\ell+1}}{q_\ell}
=R_\ell
=\frac2n\sum_{i=1}^n (Z_i)_+^2,
\qquad Z_i\overset{\mathrm{iid}}\sim\mathcal N(0,1).
\]

The multiplier has
\(\mathbb E R_\ell=1\) and \(\operatorname{Var}(R_\ell)=5/n\). Independent
layers therefore give the exact model calculation

\[
\operatorname{Var}\!\left(\frac{q_L}{q_0}\right)
=\left(1+\frac5n\right)^L-1.
\]

Consequently,

\[
\operatorname{Var}(q_L/q_0)
=5L/n+O((L/n)^2)
\]

only while \(L/n\) is small; in the simultaneous limit with
\(L/n\to r\), the same control approaches \(e^{5r}-1\), not a line. This
recovers the ReLU coefficient in PDLT's normalized four-point calculation and
turns the proposed witness into a falsifiable model calculation plus a seeded
finite-width check.

The preferred figure is therefore
\(\operatorname{Var}(q_L/q_0)\) against \(r=L/n\), with the exact finite-\(n\)
curves, the \(e^{5r}-1\) double-scaling control, and the \(5r\)
small-\(r\) tangent. A plot of \(n\operatorname{Var}(q_L/q_0)\) against
\(L\) is acceptable only in a predeclared perturbative window.

### Finite width and feature movement require a scaling clause

PDLT's frozen tangent kernel is the leading infinite-width object in its
parameterization. The first feature-moving terms enter through finite-width
kernel differentials, with their normalized effect scaling like \(L/n\) in
the analyzed families. This is a useful mechanism for the book's
lazy-versus-feature-learning branch, but not a width-only law. Different
parameterizations and simultaneous limits can retain feature movement.

The safe statement is:

> Under the declared tangent-kernel scaling and time horizon, the limit that
> makes training linearized also suppresses feature movement; finite-width
> corrections restore it at the order carried by the expansion.

This belongs in *Beyond This Volume*, with a short C14 boundary pointer, not as
a new C16 explanation of edge-of-stability behavior.

### Residual paths reallocate rather than remove the tuning problem

The proposed residual seam does have a direct PDLT route: Appendix B analyzes
residual multilayer perceptrons. Its conclusion is more useful than the
unqualified claim that an identity path automatically restores criticality.
The identity coefficient and residual-branch variance jointly determine the
critical family; an identity coefficient of one with a nonzero branch can
itself break the moment condition.

C15 already has the exact Jacobian distinction
\(J_{\mathrm{pre}}=I+J_FJ_N\) versus
\(J_{\mathrm{post}}=J_N(I+J_F)\). The right callback is one sentence:

> The identity summand changes the criticality budget; it does not abolish
> the need to control the residual branch.

An empirical claim that this improves trainability should still route to a
primary residual-initialization source.

## H1–H10 adjudication

| ID | Verdict | Exact disposition |
|---|---|---|
| H1 | **Adopt after rewrite — C14 trunk** | Add one two-input correlation witness at the ReLU critical scale. Preserve the “kept norms, lost distinction” phenomenon. Reject the three-weight-scale angle story because the zero-bias normalized ReLU map is scale independent. Keep tanh ordered/chaotic comparisons in an exercise or reading branch. |
| H2 | **Adopt after rewrite — C14 trunk** | Add the exact multiplier calculation and one seeded verification. Plot against \(L/n\), show the exact curve and the small-parameter tangent, and label \(O(L/n)\) as a perturbative prediction rather than a universal line. |
| H3 | **Adapt — paragraph plus Pencil exercise** | Derive \(\chi_\parallel\) and \(\chi_\perp\) separately. Ask when they coincide. Do not call one generic “same fixed-point slope” for forward and backward propagation. |
| H4 | **Adapt — named wrong answer plus exercise** | Keep “every activation has its critical initialization” as the wrong answer. Avoid a two-family taxonomy: PDLT distinguishes scale-invariant, zero-fixed-point, half-stable, and no-critical cases. The page needs only representative counterexamples; the full taxonomy is reading guidance. |
| H5 | **Adopt at branch depth** | Put the frozen-feature mechanism in *Beyond This Volume* and add a C14 boundary pointer. Keep it out of the C16 trunk and attach the parameterization/time-horizon clause. |
| H6 | **Adopt in corrected form** | Add the one-sentence C14→C15 callback above. PDLT Appendix B is a valid derivational route, contrary to the preliminary claim that PDLT treats only plain MLPs; use a primary source for empirical superiority. |
| H7 | **Adopt and strengthen** | The field note should say: “An approximation names its small parameter, retained order, and order of limits.” Add \(L/n\) as the fourth worked example and use the note to sharpen the Paper Autopsy Protocol's existing theory-resolution field. |
| H8 | **Adopt privately** | Add the ingestion vocabulary to `docs/STYLE-GUIDE.md`: susceptibility → fixed-point gain; edge of chaos → contraction/expansion boundary for pair separation; universality class → shared fixed-point/scaling family; effective theory → declared-truncation model. Explain first, then permit the standard term. No Rosetta rows. |
| H9 | **Shelve** | Bayesian/GP inference, dNTK/ddNTK machinery, algorithm projectors, optimal-aspect-ratio prescriptions, information-theoretic generalization, and RG metaphors remain Paper-audit or further-reading material. |
| H10 | **Adopt with bibliographic repair** | Cite the published book as Roberts and Yaida, with contributions by Boris Hanin. Replace “carried to all orders” by “developed systematically through leading finite-width corrections.” Point first to Chapter 5 §§5.1, 5.4, and 5.5. |

## Additional high-value harvests

### P1 — Criticality is a ladder, not a label

Add a compact C14 table with four rows: moment, pair geometry, Jacobian
spectrum, and finite-width trust parameter. For each row name the observable,
what it can certify, and the next failure it cannot exclude. This table is the
chapter's synthesis object and keeps the new witnesses from becoming two new
theoretical branches.

### P2 — Equal parameter steps need not mean equal function steps

PDLT Chapter 9 asks for comparable contributions to the tangent kernel across
layers and parameter groups. The branded prescription is not needed, but the
diagnostic is valuable in C17: an update-routing table should compare induced
function-space contribution, not only parameter-space norm. Upgrade C17
Exercise 4 so that students measure each block's contribution to a Jacobian
Gram or output change under equal nominal learning rates. Keep this at
exercise depth.

### P3 — A local critical slope can miss a finite-angle effect

ReLU's infinitesimal perpendicular gain is one at criticality, yet its
finite-angle pair separation decays polynomially. This is an excellent
extension of the existing C14 implication-graph Audit exercise: students must
locate the step where an infinitesimal conclusion is transferred to a finite
perturbation and state the smoothness or uniformity assumption that is
missing.

### P4 — The order of limits is part of the claim

“Infinite width” and “large depth” are incomplete regime descriptions.
Fixed \(L\) followed by \(n\to\infty\) removes effects that survive when
\(L,n\to\infty\) with \(L/n\to r\). Add “small parameter, truncation order,
and order of limits” as a subprompt inside the existing **Resolution of the
theory** field of the Paper Autopsy Protocol rather than creating another
field.

## Credit and primary-source routing

PDLT should be credited for the derivational map and the disciplined
depth/width bookkeeping. Load-bearing public claims should also route to:

- Poole et al. (2016) and Schoenholz et al. (2017) for two-input signal
  propagation and the ordered/chaotic boundary;
- Yaida (2020) and Hanin–Nica (2019/2020) for finite-width non-Gaussian and
  tangent-kernel corrections;
- Jacot et al. (2018), Lee et al. (2019), and Chizat–Oyallon–Bach (2019) for
  frozen/linearized training and the scaling dependence of lazy behavior;
- Hanin–Rolnick (2018) or another exact residual-initialization primary source
  before attaching an empirical trainability claim to the residual callback.

The Sources sentence should read approximately:

> For a derivational companion to the moment and pair-correlation recursions,
> and for a systematic leading finite-width expansion whose trust parameter is
> depth over width, see Roberts and Yaida (2022), with contributions by Boris
> Hanin; begin with Chapter 5 §§5.1, 5.4, and 5.5.

## Build bill and acceptance gate

If approved, the bounded implementation is:

1. restructure C14 around the four-rung ladder rather than append two detached
   sections;
2. add one correlation claim and one depth/width fluctuation claim, both class
   (a), each with deterministic controls before seeded evidence;
3. add two small harness functions, tentatively
   `relu_correlation_trace` and `relu_moment_fluctuation_control`;
4. replace or absorb overlapping C14 prose so the chapter grows by no more than
   four derived-PDF pages;
5. upgrade the C14 implication-graph exercise, C17 Exercise 4, the C15 residual
   callback, the continuation map, and one Paper Autopsy subprompt;
6. add only the bibliography entries actually cited on the page.

The existing `ch-14` wheel is immutable. The executable pass must not overwrite
it. It therefore needs either D34's forward-only revision-tag scheme or an
explicit revision pin such as `ch-14-r2`, with a new wheel digest and preserved
historical artifact.

## Proposed decision

The author's proposed number D43 is already occupied by the prerequisite-route
decision. The next available entry is:

**D50 — PDLT ingestion scope.** Adopt corrected H1 and H2 as a restructured
C14 trunk; H3, H4, H7, H10, and P1/P3/P4 at paragraph, table, or exercise
depth; H5 in *Beyond This Volume*; H6 as the corrected C15 callback; H8 as a
private style rule; P2 as a C17 exercise refinement; and H9 on the shelf.
Require a forward-only C14 revision pin before executable manuscript changes.

**Recommendation:** approve D50. It preserves the existing chapter's
instrument-first authority while importing PDLT's most valuable mathematical
habit: a limit is only useful when its failure parameter remains visible.

**Author disposition (2026-08-01): approved for implementation.** The
forward-only executable revision is `ch-14-r2`; D34 remains independently
open.
