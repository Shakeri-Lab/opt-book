# Build Plan v2

## *Deep Learning: Making It Trainable*

**Course:** DS 6210 — Computation II: Numerical Analysis & Optimization
**Public course alias:** Algorithms for Deep Learning
**Author:** Heman Shakeri, School of Data Science, University of Virginia
**Repository:** `Shakeri-Lab/opt-book`
**Status:** Approved implementation baseline; C02 pilot locally built and under acceptance audit
**Prepared:** 2026-07-30

**Revision from v1:** incorporates author review R1–R9, establishes the harness as a
book-born system unless undiscovered course code is supplied, adds the sibling
notation covenant and reciprocal anchor contract, preclassifies chapter phenomena,
makes thread and branding audits viable from day one, fixes the pilot budget, tunes
CI cost, and makes tagged-PDF accessibility an explicit first-commit decision.

## Plan gate

This document establishes the book contract, ownership boundaries, candidate arc,
and production architecture. On 2026-07-30 the author authorized the build to
proceed. The recommendations in D01–D24 are recorded as the working decisions in
`docs/DECISIONS.md`; later author corrections supersede those defaults.

The plan is based on:

- the DS 6210 course vision and reusable course-book authoring contract;
- the local Spring 2026 course archive, with `my_lectures/` treated as
  instructor-canonical;
- the two local syllabus proposals, the Spring 2026 lecture sequence, journal-club
  decks, project materials, midterm, and the legacy LaTeX book;
- the current resource shelf and outside lecture collection, treated as
  reference-only until provenance is established;
- the live v1.2 edition of
  [*Deep Learning: Making It Learnable*](https://shakeri-lab.github.io/dl-book/),
  its representative Chapter 9, its experiment interlude, Appendix C, and the
  sibling source repository at commit `bd4e06f` (2026-07-29).

### Local orientation findings

- The course archive is not itself a Git repository. The intended `opt-book`
  repository exists as an empty private GitHub repository and has now been cloned
  locally.
- `my_lectures/` contains 235 files. It includes a coherent Spring 2026 sequence
  through roofline analysis, streaming state, precision, convex baselines,
  concentration, random matrices, backpropagation, saddle geometry, Muon, QJL,
  initialization, normalization, and edge-of-stability material.
- `old/DS6210_Book/` contains two distinct legacy strata: a lecture-shaped
  sixteen-unit draft and a later six-chapter refinement. The refined PDF is 58 pages
  and covers dimensional motivation, roofline/all-pairs computation, streaming
  state, finite precision, convex surrogates, and convergence costs. This is
  recoverable material, not the new book's structure or prose.
- The legacy sixteen-unit draft contains useful examples and cross-thread ideas, but
  it still exposes classroom residue such as “lecture,” “week,” and slide-derived
  transitions. It must not be promoted wholesale.
- The local shelf contains 46 files under `Resources/`, 115 under
  `Others lectures/`, and 49 under `course projects/`. Student projects and zipped
  submissions require an explicit permission decision before any public reuse.
- The Spring 2026 project work already embodies the desired terminal capability:
  optimizer cards, separation of curvature/spatial/trajectory spectra, cost and
  state accounting, invariance checks, evidence audits, preregistration, negative
  results, and wall-clock honesty.

### Decisive architectural finding: the harness is not yet a codebase

No course-wide Evolving Training Harness implementation was found anywhere in the
reviewed tree. The archive contains lecture code, laboratory ideas, experiments, and
student project infrastructure, but not one package that can be migrated under the
§5 versioning scheme.

The working assumption for Plan v2 is therefore explicit:

> The harness is being born with the book. Spring 2026 notebooks and any later
> author-supplied lab code inform its design, but the §5 capability table is a
> **genesis roadmap**, not a migration map.

This is not a reason to postpone immutability. Tags, digests, vendored wheels, the ban
on mutable imports, compatibility shims, and byte-identical historical stdout begin
with the first package. The C02 pilot needs only a small honest package, likely five
public operations: an observation/seed ledger, naïve moments, stable online moments,
an associative state merge, and a comparison audit. It does not need a prematurely
general training framework.

If a course-wide harness exists outside the reviewed tree, D21 changes this genesis
assumption and the code must enter the materials handoff before the pilot contract is
approved.

---

## 1. Book identity

### Working identity

**Title:** *Deep Learning: Making It Trainable*

The title completes the family move:

> *Making It Learnable* asks what should be learned, built in, and reused.
> *Making It Trainable* asks what lets the resulting computation survive geometry,
> dynamics, arithmetic, and hardware.

The recurring question promised by the title is:

> What mathematical and physical conditions make a modern learning system trainable,
> and which diagnostic tells us which condition failed?

### Reader contract

The intended reader is a mathematically mature graduate student preparing to read or
produce research in optimization and modern machine learning. The book assumes
linear algebra, probability, Python, NumPy, PyTorch, and the mechanics of first-course
deep learning. It does not assume prior mastery of random matrix theory, numerical
stability, accelerator performance models, or modern optimization research.

By the end, the reader should be able to inspect a paper, implementation, or training
trace and identify:

1. the geometric assumption;
2. the optimization dynamic;
3. the numerical and hardware constraint;
4. the estimator behind the evidence;
5. the regime in which the conclusion is valid;
6. a discriminating measurement or control that could falsify the proposed
   diagnosis.

### Difference from the sibling

The sibling's native move is **show, then name**: construct a mechanism, make the
right component learnable, and test what the architectural choice buys.

This volume's native move is **break, diagnose, repair**: expose a failure or
constraint, ask the reader to predict its cause, introduce the smallest theory that
separates competing explanations, and derive a repair whose boundary can be audited.

The difference is not “more equations.” It is a different promise:

| Dimension | *Making It Learnable* | *Making It Trainable* |
|---|---|---|
| Primary reader | First deep-learning course | PhD-track numerical/optimization reader |
| Organizing question | What is learned, built in, reused? | What makes training possible, stable, and efficient? |
| Default exposition | Show the mechanism, then name it | Show the failure, diagnose it, then repair it |
| Mathematical depth | Derive the mechanics needed to build | Prove or precisely source the diagnostic consequence |
| Code role | Construct and compare models | Instrument, stress, distinguish, and audit mechanisms |
| Hardware role | Practical appendix and selected applications | One of the three load-bearing explanatory lenses |
| Endpoint | Build and understand modern model families | Critically read a current systems/optimization paper |

### What this book refuses to be

- It is not a clone of the sibling's voice with harder mathematics inserted.
- It is not a re-teaching of backpropagation mechanics, convolutional assembly,
  transformer assembly, or first-course training loops.
- It is not a survey of named architectures or optimizers.
- It is not a numerical-analysis encyclopedia that completes a conventional topic
  list without changing what the reader can diagnose.
- It is not a theory text that treats representation error and data movement as
  implementation details.
- It is not a systems text that treats spectra, estimators, and assumptions as
  decoration.
- It does not imply that an asymptotic random-matrix law is a finite-width identity,
  that loss decrease proves a mechanism, or that a favorable FLOP count predicts
  runtime.

### Title decision record

The author fixed the family title in the kickoff brief:

> **Deep Learning: Making It Trainable**

Plan v2 therefore drops the alternative-title exercise. The optional subtitle
**Geometry, Dynamics, and the Machine** remains a later cover/metadata decision; it
does not reopen the title.

---

## 2. Ownership map versus the sibling

### Cross-book rule

The two books form a sequence, not a duplicated pair.

- A stable sibling URL may supply assumed mechanics.
- This book may give a short recap that establishes notation and then point outward.
- A recap may not reproduce the sibling's derivation, code path, exercise, or model
  assembly.
- A chapter contract must name its sibling dependency before drafting.
- If the sibling already owns the learner transformation, the topic does not earn a
  second chapter here.
- Cross-book links target stable section or chapter anchors, not page numbers in the
  rolling live PDF.
- Releases may additionally cite a fixed sibling version when page-precise references
  are needed.

### Stable sibling anchors to treat as public interfaces

- [Backpropagation mechanics](https://shakeri-lab.github.io/dl-book/chapters/part1/05-backpropagation.html#sec-05-backpropagation)
- [Experiment discipline](https://shakeri-lab.github.io/dl-book/chapters/interludes/learning-by-experiment.html#sec-learning-by-experiment)
- [Kernel regression](https://shakeri-lab.github.io/dl-book/chapters/part4/12-kernel-regression.html#sec-12-kernel-regression)
- [Attention mechanics](https://shakeri-lab.github.io/dl-book/chapters/part4/13-attention.html#sec-13-attention)
- [Transformer assembly](https://shakeri-lab.github.io/dl-book/chapters/part4/14-self-attention-transformer.html#sec-14-self-attention-transformer)
- [Modern CNNs and normalization seed](https://shakeri-lab.github.io/dl-book/chapters/part2/09-modern-cnns-transfer.html#sec-09-modern-cnns-transfer)
- [Precision and hardware efficiency](https://shakeri-lab.github.io/dl-book/chapters/appendices/a3-precision-performance.html#sec-a3-precision-performance)

The source/provenance ledger will retain the sibling release and commit used when an
anchor is admitted into the public interface.

### Reciprocal public-anchor contract

The interface cannot be protected only from `opt-book`. The sibling repository must
also promise not to move these seven anchors silently.

Immediate contract, gated by D23:

1. add `docs/public-anchors.md` to `Shakeri-Lab/dl-book`, listing the seven exact
   URLs, owning source labels, semantic purpose, and first dependent consumer;
2. add a sibling CI fixture that renders or inspects the built site and fails if an
   anchor disappears or resolves to a different semantic target;
3. make anchor replacement a deprecation: retain the old anchor or ship an explicit
   redirect and update both ledgers;
4. link the two books reciprocally in their colophons once `opt-book` is public.

Deferred reciprocal patch:

- when `opt-book` reaches approximately v0.2 and its own collision-surface anchors are
  stable, prepare a sibling v1.2.x point release with forward pointers from Appendix
  C, the experiment interlude, Chapter 5, Chapter 9's normalization seed, and
  Chapters 12–14;
- each pointer states the split: mechanics remain in the sibling; theory,
  diagnostics, or hardware evidence continue here;
- do not add forward pointers before stable targets exist.

Until the sibling contract is committed, `opt-book` link CI detects movement but
cannot prevent it. The two-repository ledger is the durable interface.

### Provisional core chapter ownership map

The following is a candidate arc, not an approved table of contents. “Own” means the
new volume is responsible for the stated transformation. “Import” means the sibling
owns the mechanics and this book uses a recap-then-pointer. “Collision” marks a
boundary that must be tested during chapter contracting.

| Unit | Provisional transformation and opening phenomenon | Ownership here | Sibling interface / explicit split |
|---|---|---|---|
| **Act 0 — The computational arena** ||||
| C01. FLOPs are not time | Diagnose why an operation with modest arithmetic runs slowly by accounting for bytes and reuse | **Own:** memory hierarchy as a quantitative diagnostic; machine balance; operational intensity; measured versus upper-bound rooflines | **Collision:** sibling Appendix C owns the introductory roofline explanation and FlashAttention preview. Here: derive and measure a diagnostic roofline, include cache/regime boundaries, and make the evidence contract central. |
| C02. One pass, two failures | Repair a variance calculation that exceeds memory or becomes negative | **Own:** sufficient streaming state; Welford/Chan derivations; conditioning of alternative formulas; parallel merge invariant | **Collision:** Appendix C owns simple rounding examples. Here: backward-error/conditioning analysis and the same state as a systems and stability repair. Recommended pilot. |
| C03. When algebra becomes execution | Predict overflow, underflow, update disappearance, cancellation, and grid collapse from a precision contract | **Own:** error model, unit roundoff, conditioning versus stability, accumulation policies, quantization error, stochastic rounding as an estimator | **Collision:** Appendix C owns format anatomy, mixed-precision roles, and introductory examples. Here: mathematical error analysis, failure envelopes, and training diagnostics; recap the format table only by link. |
| C04. The control experiment | Read gradient descent mode by mode and predict speed, oscillation, noise floor, and preconditioner effect | **Own:** exact quadratic dynamics, stability region, condition-number tax, stochastic perturbation baseline | **Import:** linear/logistic mechanics and first-course SGD from sibling Chapters 1–4. Convex-surrogate mechanics receive only a short bridge or an appendix pointer. |
| **Act I — Geometry of high dimensions** ||||
| C05. The sub-Gaussian safe zone | Explain why a billion random coordinates can still produce predictable norms and activation scales | **Own:** MGF method, equivalent sub-Gaussian characterizations, Hoeffding-type consequences, Orlicz diagnostic language | No sibling collision beyond basic probability prerequisites. |
| C06. Squaring breaks the safe zone | Diagnose why squared norms, covariance entries, and gradient magnitudes need two tail regimes | **Own:** sub-exponential variables, products/squares, Bernstein regimes, clipping boundary, heavy-tail counterexamples | Sibling imports only for the model context that produces gradients. |
| C07. Replacing a sphere by witnesses | Turn a continuous operator-norm question into finitely many concentration events | **Own:** covering numbers, epsilon nets, union bound plus Lipschitz bridge, approximation debt | No substantive sibling ownership. |
| C08. Vectors become operators | Predict worst-direction amplification from a random matrix rather than entrywise scale | **Own:** operator versus Frobenius norms, two-sided singular-value bounds, matrix concentration as diagnosis | Sibling Appendix A may supply SVD mechanics; this chapter owns probabilistic operator control. |
| C09. Bulk, edges, and signal | Decide whether a spectrum is null bulk, finite-sample fluctuation, or structured signal | **Own:** Marchenko–Pastur law, finite-size caveats, covariance estimation, spectral null hypotheses | The sibling uses spectra descriptively; this book owns the law, assumptions, edge diagnostics, and falsifying controls. |
| C10. Dimension that counts | Replace parameter count with effective/stable rank and audit overparameterization claims | **Own:** effective rank, stable rank, covariance complexity, compression/generalization diagnostic limits | **Collision:** sibling Chapters 6, 9, and 17 discuss generalization, transfer, and low-rank adaptation. Here: spectral capacity measures and exact scope; no repeat of architecture or adaptation mechanics. |
| **Act II — Dynamics of optimization** ||||
| C11. Reverse accumulation under a memory budget | Explain why a gradient can be cheap in arithmetic yet expensive in retained state | **Own:** VJPs/JVPs as linear-operator primitives, adjoint view, checkpointing/recomputation schedules, precision propagation | **Import:** [sibling Chapter 5](https://shakeri-lab.github.io/dl-book/chapters/part1/05-backpropagation.html#sec-05-backpropagation) owns chain-rule/backprop mechanics and a tiny autograd engine. No second MicroGrad tutorial unless used only as a harness compatibility test. |
| C12. Curvature and the crowded landscape | Distinguish minima, saddles, flat plateaus, and Gauss–Newton structure spectrally | **Own:** Hessian/GGN/Fisher distinctions, Hessian-vector products, index, saddle geometry, RMT diagnostic limits | Sibling supplies model/loss mechanics only. |
| C13. Noise is not one thing | Separate optimization noise, sampling noise, heavy-tail exploration, and estimator error | **Own:** stochastic dynamics regimes, diffusion versus jump intuition with scoped mathematics, clipping and schedule consequences | **Import:** sibling experiment discipline for fair runs; do not recreate its experimental-method interlude. |
| C14. Training before the first step | Derive when depth preserves or destroys signal before optimization begins | **Own:** variance recursions, criticality, Jacobian products, dynamical isometry, precision-dependent depth budget | **Collision:** sibling Chapter 5 owns introductory initialization and Chapter 9 shows normalization effects. Here: full depth/spectral theory and failure envelopes. |
| C15. Controlling scale during motion | Diagnose which axis is normalized and what curvature or precision consequence follows | **Own:** normalization Jacobians, axis/reduction contracts, preconditioning interpretation, cancellation/stability consequences | **Import:** sibling Chapter 9 owns BatchNorm mechanics and Chapter 14 owns transformer placement/assembly. Branded variants appear only at the show-then-name bridge. |
| C16. The edge that moves | Explain progressive sharpening and non-monotone loss beyond the fixed quadratic picture | **Own:** classical versus dynamical stability, top-curvature tracking, edge-of-stability evidence, large-step curvature filtering, theorem boundaries | No sibling duplication; use primary papers and the current instructor handout as canonical sources. |
| C17. Updates with geometry | Audit a matrix-aware, orthogonalized, quantized, or sketched update by its norm, spectrum, state, and hardware cost | **Own:** update geometry, Newton–Schulz as a numerical kernel, parameter routing, update-scale contracts, Muon/QJL-style paper audits | Named methods are capstones after primitives. The terminal job is not “teach Muon” but identify its assumptions, approximations, and evidence boundary. |

### Candidate synthesis extension, not in the core commitment

The older syllabus and legacy book propose an Act III. It is intellectually valuable,
but Spring 2026 was staged primarily as Acts 0–II. These units remain gated by
author decision rather than silently inflating v1:

| Candidate unit | Ownership boundary |
|---|---|
| S01. Frozen-feature control limit | Own NTK/lazy-regime dynamics and their diagnostic boundary; import kernel mechanics from sibling Chapter 12. |
| S02. Similarity-weighted aggregation at scale | Own concentration scaling and saturation; import attention and transformer assembly from sibling Chapters 13–14. |
| S03. Exact all-pairs computation without the matrix | Own IO complexity, online normalizers, tiling invariants, and recomputation; explicitly split from sibling Appendix C's concise FlashAttention treatment. |
| S04. A bounded state for history | Own approximation-theoretic retained state; avoid architecture survey language. |
| S05. Associativity under finite precision | Own parallel scan work/depth analysis and non-associative error audit. |
| S06. Alignment and finite-width feature learning | Own the departure from the frozen-feature limit and close the spectral/update threads. |

### Collision protocol

For every collision surface, the chapter contract must contain:

1. the exact sibling anchor;
2. the mechanics assumed from that anchor;
3. the new diagnostic transformation owned here;
4. a duplication budget, normally no more than one compact recap plus notation;
5. a “delete if duplicated” test during editorial audit.

The largest collision surfaces are:

- Appendix C versus C01/C03/S03;
- the experiment interlude versus every empirical chapter;
- sibling Chapter 5 versus C11;
- sibling Chapters 12–14 versus the synthesis extension;
- sibling Chapter 9's normalization seed versus C15.

---

## 3. The de-branding apparatus

### Principle

De-branding is **show-then-name**, not name suppression. A branded term is withheld
until the reader owns the mathematical primitive. At that point the conventional
name, variants, and primary source are supplied so the reader can enter the
literature.

### Rosetta appendix

Create a sanctioned appendix titled **Rosetta: From Mathematical Primitive to
Literature Name**. Each row has:

| Field | Contract |
|---|---|
| Primitive used in this book | The mechanism-first phrase |
| Standard name and aliases | Exact branded/search vocabulary |
| First mechanism chapter | Stable anchor in this book |
| Sibling anchor | Stable URL where mechanics are already taught, when applicable |
| Primary citation | Original or definitive source, not a secondary blog unless the blog is itself the primary release |
| Scope note | What variants share, and what the alias does not imply |
| Notation | Canonical symbol(s), including any de-branded or literature alias; nonstandard choices are explicit |
| Search terms | Singular/plural, spelling, acronym, and common implementation names |

Initial families include:

- deep compositional structure → neural network / MLP, when the generic class is
  meant;
- coordinate-wise or token-wise normalization → LayerNorm / RMSNorm;
- batch-and-spatial coordinate normalization → BatchNorm;
- variance-preserving initialization → Xavier/Glorot, He/Kaiming;
- diagonal moment preconditioning → Adam / AdamW;
- similarity-weighted aggregation → attention / self-attention;
- IO-aware exact all-pairs aggregation → FlashAttention;
- matrix-aware or orthogonalized update → Muon, Shampoo, SOAP, related variants;
- quantized random projection/update sketch → QJL, TurboQuant;
- optimal finite-state history projection → HiPPO;
- structured state-space realization → named state-space variants such as Mamba;
- low-rank adaptation of frozen parameters → LoRA;
- frozen tangent-feature dynamics → NTK / lazy training.

### First-use bridge

At the first sanctioned naming point, use a semantic `brand-bridge` aside:

> **Literature bridge.** The primitive developed above is commonly called
> **LayerNorm** in the literature. The name identifies a family; the axis, centering,
> epsilon placement, and precision contract remain part of the algorithm.

Implementation:

- HTML: a true `aside` on wide screens, inline after the relevant paragraph on narrow
  screens;
- PDF: a margin note when it fits, otherwise an inline bridge callout;
- both editions contain the same words and link/citation;
- subsequent use may use the standard name only when it reduces ambiguity in a
  paper-audit context.

### Search and alias strategy

Branded queries must find the site without letting branding organize the exposition.

1. Put every alias in the Rosetta appendix.
2. Add a `search-aliases` metadata field to relevant chapters.
3. Generate an accessible, non-duplicative alias block for the site search index from
   that metadata.
4. Add redirect pages only for high-value external entry points, such as
   `/layernorm.html`, whose visible content immediately routes to the mechanism
   chapter and Rosetta row.
5. Test search queries in CI: `LayerNorm`, `AdamW`, `attention`, `He initialization`,
   `Muon`, `QJL`, and `FlashAttention` must each return an intended chapter or
   Rosetta result in the top two.

### Context-aware CI tripwire and allowlist

Implement `scripts/audit_branding.py`. It scans learner-facing prose after removing
code, raw citations, bibliography blocks, and HTML comments.

The vocabulary is committed as data. Each entry is a
`(term, context_regex, severity)` triple rather than a context-blind word:

| Term family | Context that activates the rule | Default severity |
|---|---|---|
| `neural network`, `MLP` | model/architecture/composition use | error |
| `LayerNorm`, `RMSNorm`, `BatchNorm` | any prose use outside literal API/code | error |
| `He`, `Kaiming`, `Xavier`, `Glorot` | within a bounded window of `initialization`, `initialize`, or `init` | error |
| `Adam`, `AdamW` | optimizer, update, moment, parameter-group, or preconditioner context | error |
| `attention` | `attention mechanism`, `head`, `layer`, `weights`, `scores`, `matrix`, `block`, or `self-attention` context | error |
| `Transformer` | model, architecture, block, layer, encoder, or decoder context | error |
| `FlashAttention`, `Muon`, `Shampoo`, `SOAP`, `QJL`, `TurboQuant`, `HiPPO`, `Mamba`, `LoRA`, `NTK` | exact named-method use | error |
| ambiguous plain-language use | no activating context | report only |

This prevents ordinary English from becoming a build failure: “pay attention,” the
pronoun “He,” an electrical transformer, and an author named Adam are not branded
method use. Citations are parsed structurally rather than excused by capitalization.

Allowed locations:

- the Rosetta appendix;
- `Sources and further reading`;
- citation titles and bibliographic metadata;
- `brand-bridge` asides;
- explicit `paper-audit` blocks after the primitive has been introduced;
- YAML `search-aliases`;
- literal code/API names when unavoidable.

Every allowlisted occurrence is still counted in a generated report. The linter fails
on unmarked prose use, a bridge that precedes the mechanism anchor, or an alias with
no primary citation.

Commit two linter fixtures from day one:

- a **golden allowed-sentences file** containing ordinary-language, author-name,
  citation-title, API, Rosetta, bridge, and paper-audit cases that must pass;
- a **golden violation file** containing real branded contexts that must fail at the
  declared severity.

CI runs the fixtures before scanning the manuscript. A vocabulary change that
creates false positives must fix the rule or fixture, not mute the audit. The rule
data and its golden corpus are versioned together.

---

## 4. Chapter skeleton and conventions specification

### Reasoning spine

Every numbered chapter follows:

> **Problem → Prediction → Instrumentation → Diagnosis → Theory → Solution → Audit
> → Recap**

These are obligations, not mandatory visible headings. A compact chapter may combine
Instrumentation with the opening witness, or Solution with Audit. It may not omit
the causal chain.

### Recurring apparatus

| Apparatus | Action | Specification |
|---|---|---|
| Visible failure or puzzle | **Invent for this volume** | Opens the chapter before definitions; small enough to see or inspect. |
| Prediction pause | **Adapt** | Reader writes a directional prediction and names one competing explanation before the reveal. |
| Symptom card | **Invent** | Records observable trace, dtype/device, scale, and what has not yet been inferred. |
| Instrument panel | **Invent** | Names the minimum diagnostic quantity: bytes, ULP, tail proxy, spectrum, curvature, angle, or retained state. |
| Problem → Diagnosis → Theory → Solution spine | **Invent relative to sibling; inherit from course vision** | Causal structure is mechanically audited in chapter metadata. |
| Three-lens ledger | **Invent** | Chapter front matter marks Geometric, Dynamic, and Algorithmic/Systems as primary, supporting, or intentionally quiet. |
| Thread sigils and callback | **Invent** | Margin/inline sigils identify callbacks without replacing prose. |
| Numbered Plan → Code panels | **Inherit** | At most six numbered plan steps; matching bracket-only `# [n]` markers; visible code is executed code. |
| Equation / kernel / harness separation | **Inherit and strengthen** | Mathematical object, mechanism-bearing kernel, and experimental harness remain distinguishable. |
| Trap/tip/note callouts | **Inherit** | Trap names a tempting wrong answer; tip carries a repair or coding hygiene; note defines or scopes. |
| Check yourself | **Inherit** | Exactly one retrieval box near the end of every numbered chapter. |
| “Okay, so —” recap | **Adapt** | Answers: inherited, changed, instrumented, established, and unresolved. |
| Sources and further reading | **Inherit** | Human-readable sources; internal file provenance stays private. |
| Exercises | **Inherit** | Follow Sources, matching the sibling's actual v1.2 ordering. |
| Named wrong answers | **Inherit and expand** | At least one where a central distinction is commonly confused. |
| Sealed endpoints and seed panels | **Inherit** | Required when model selection, stochastic evidence, or a claimed comparison appears. |
| Pinned JSON evidence | **Inherit and generalize** | Required for any published endpoint not produced on the page. |
| Paper audit | **Invent as a recurring Audit exercise** | At least one per act; every later research-facing chapter ends with one. |
| Field notes | **Invent** | Short boundary note: what this diagnosis looks like in a real trace and what else can mimic it. |

### Exercise taxonomy

**Recommendation: retain exactly three formal tags.**

- **(Pencil.)** derive, prove, predict, or reason.
- **(Code.)** implement, simulate, measure, or profile.
- **(Audit.)** judge a claim, theorem-to-implementation gap, protocol, or paper.

Do not add `(Profile.)`: profiling is a Code exercise with a hardware contract.
Do not add `(Paper.)`: paper reading is an Audit exercise with a named paper-audit
contract. This preserves family continuity while serving the terminal capability.

Required wording patterns:

- `(Code.) Profile:` for a roofline/kernel measurement;
- `(Audit.) Paper audit:` for assumption/evidence analysis;
- mixed work is split into separately tagged subparts.

### Paper-audit contract

A paper audit must ask the reader to record:

1. mathematical object and shapes;
2. geometric assumption;
3. dynamic claim;
4. numerical/hardware contract;
5. state, compute, memory, and communication cost;
6. estimator, denominator, comparison budget, and seeds;
7. strongest supported claim;
8. seductive overclaim;
9. one discriminating control.

This adapts the Spring 2026 optimizer-card practice into the book. It is not an
aspirational endpoint: the Spring 2026 projects already demonstrated that students
can preregister comparisons, write optimizer cards, retain negative results, and
name the assumptions behind a claim. The recurring audit turns that demonstrated
practice into a course-wide capability.

### Thread tracking

Use four public narrative threads unless the author approves six:

- **Numerical stability**
- **Random-matrix spectra**
- **Landscape and update geometry**
- **The sub-Gaussian safe zone**

Maintain **memory wall and retained state** plus **orthogonality and scale** as
cross-cutting seed/harvest ledgers. They can become public sigils if the author
chooses the six-thread model.

Each public thread receives:

- an accessible textual label plus a redundant sigil;
- a thread index page with seed, callback, transformation, and harvest locations;
- an explicit registered seed chapter and chapter metadata, for example
  `threads: [numerical-stability: callback, spectra: seed]`;
- a generated act-by-thread matrix;
- a seed-aware CI audit: acts strictly before a thread's registered seed are exempt;
  the seed chapter must declare `seed`; from that point onward the audit fails if the
  thread receives no meaningful callback in an entire act;
- a qualitative callback audit, not only a word count: the callback must identify
  what changed since the last appearance.

`scripts/audit_threads.py` checks metadata, anchor existence, act coverage, and the
presence of a nearby callback sentence. A raw keyword count is reported but never
accepted as proof of continuity. A callback before the registered seed is an error,
and an unregistered thread cannot claim the pre-seed exemption. Thus Act 0 does not
fail because spectra, landscape, and the sub-Gaussian safe zone have not yet been
seeded.

### Chapter contract file

Before prose, every chapter gets a private contract with:

- thesis and student transformation;
- opening phenomenon and prediction;
- competing explanations;
- diagnostic instrument;
- minimal theory and proof mode;
- repair and falsifying control;
- three-lens ledger;
- sibling dependency and duplication budget;
- source/evidence ledgers;
- seed/harvest obligations;
- representation and figure plan;
- harness capability and pin;
- hardware provenance class;
- length budget and what new material displaces.

### Notation covenant with the sibling

Notation is a cross-book public interface, not a chapter-local style choice.

**Core inheritance.** Copy the sibling's canonical core table verbatim into a
machine-readable covenant, including:

- italic scalars;
- `\vect{}` for bold vectors and `\matr{}` for bold matrices or batched arrays, with
  declared shape carrying the final type distinction;
- $\vect{x}$ for a feature/input vector, $\vect{w}$ for parameters, and hats for
  predictions or estimates where the local role agrees;
- $\loss=\mathcal{L}$ for an aggregate objective and $\ell_i$ for a local/per-example
  loss;
- $\E$, $\var$, $\cov$, $\norm{\cdot}$, $\argmin$, $\argmax$, $\R$, and $\dd$;
- $=$ for equality, $:=$ for definition, $\approx$ for approximation, and
  $\leftarrow$ for an algorithmic update;
- dimensions before matrix products, named reduction axes, and the sibling's
  column-vector-on-paper / row-batch-in-code convention.

**Additive extension.** This volume adds, without redefining the core:

- operator and Frobenius norms, with
  $\norm{\matr{A}}_{\mathrm{op}}=\sigma_{\max}(\matr{A})$ only when the equality's
  assumptions and object are clear;
- singular values, eigenvalues, spectral edges, condition number, stable rank, and
  effective rank;
- $\psi_2$ and $\psi_1$ Orlicz norms and explicit random-variable/population/sample
  distinctions;
- machine precision, unit roundoff, ULP, floating-point evaluation, and error symbols;
- Hessian, generalized Gauss–Newton, Fisher, Jacobian, VJP, and JVP symbols that may
  not be conflated merely because implementations share products;
- optimizer-state, update-angle, retained-state, and hardware-cost notation.

Every extension in the public notation appendix carries a **New in this volume**
marker and a source/first-use anchor. The Rosetta appendix's Notation column records
where a de-branded primitive uses symbols that differ from common literature.

**No redefinition.** A symbol or macro in the core covenant may not acquire an
incompatible global meaning here. Local reuse is allowed only when the chapter
defines it and the covenant marks the symbol as locally polymorphic. If a genuine
conflict arises, introduce a new symbol rather than silently forking the family.

**Committed source of truth.** Use
`contracts/notation-covenant.yml` for the inherited and additive symbol records.
Generate:

- the notation appendix table;
- the shared MathJax and LuaLaTeX macro checks;
- a cross-book compatibility report.

`scripts/audit_notation_covenant.py` fails when a core record is removed or redefined,
when HTML/PDF macros diverge, when the rendered appendix differs from the covenant,
or when a notation-appendix diff lacks the corresponding covenant change. D22
approves both the covenant and this file location.

---

## 5. Evolving Training Harness architecture

### Genesis status

The harness does not yet exist as a recoverable course package. It is being designed
book-first unless D21 reveals author-held code outside the reviewed tree.

Accordingly:

- the module and capability lists below are a roadmap, not an inventory;
- Spring 2026 notebooks are evidence about useful diagnostics and learner
  difficulties, not an API that must be preserved automatically;
- the pilot begins with the smallest package that carries its causal argument;
- no empty modules are created merely to make the final tree look complete.

The first `harness@ch-02` artifact is expected to expose roughly five public
operations: ledger construction, naïve moments, stable online moments, state merge,
and comparison audit. Plot styling and general training abstractions do not belong in
that first API. The full immutability contract nevertheless applies from this first
small wheel.

### Architectural decision

Use one Python package at `harness/`, versioned in the same repository. The harness is
not a collection of chapter scripts. It is a stable diagnostic API whose capabilities
grow while earlier contracts remain executable.

Proposed layout:

```text
harness/
  pyproject.toml
  src/trainable_harness/
    ledger.py
    numerics.py
    timing.py
    roofline.py
    streaming.py
    tails.py
    spectra.py
    autodiff.py
    curvature.py
    flow.py
    optim.py
    io.py
    scan.py
    _buildinfo.py
  tests/
artifacts/
  harness/
    ch-01/
      trainable_harness-0.1.0-py3-none-any.whl
      manifest.json
    ch-02/
      ...
environment/
  chapters/
    ch-01.lock
    ch-02.lock
```

### Chapter pins

Each executable chapter declares an immutable harness dependency:

```yaml
harness-ref: ch-02
harness-wheel-sha256: <digest>
harness-api: "0.2"
```

At the end of a chapter:

1. create an annotated tag `harness-ch-02-v1`;
2. build the wheel from that exact tagged source;
3. record tag, commit SHA, wheel SHA-256, Python version, and dependency lock in
   `artifacts/harness/ch-02/manifest.json`;
4. vendor the small pure-Python wheel so historical chapter execution never depends
   on a mutable branch or live network;
5. make the notebook bootstrap verify the manifest before importing.

“`harness@ch-N`” therefore means a tag, commit, lock record, and content-addressed
wheel, not merely a human-readable version string.

### Compatibility rule

- Public functions used by a published chapter cannot be removed or silently change
  semantics.
- Refactors add a new API and retain a deprecation shim for old signatures.
- A shim emits a repository-test warning, not a learner-visible warning during the
  pinned historical chapter.
- Behavior changes require a new chapter pin or tag revision and a provenance note.
- Old tests remain in the suite.
- A public-symbol and behavioral-invariant ledger is generated at every tag.
- Earlier frozen stdout must remain byte-identical unless the experiment is
  intentionally revised and every dependent claim is re-audited.

### Notebook self-containment contract

This volume knowingly amends the sibling's “zero undeclared repo-local dependency”
invariant:

> A chapter notebook is self-contained given its declared environment lock, committed
> input artifacts, and immutable `harness@ch-N` wheel.

It may not:

- import the mutable `harness/` working tree;
- depend on a later chapter's tag;
- download data at render time;
- read mutable chapter prose as data;
- infer seeds, dtype, device, estimator, or hardware from ambient state.

It must:

- print/assert its harness tag and content digest;
- declare random streams separately;
- state shapes and reductions;
- include a small CPU witness even if the endpoint result is a cluster artifact;
- transclude only outputs produced by the pinned environment.

### CI contract

`scripts/audit_harness_pins.py` fails when:

- an executable chapter has no pin;
- a pin points to a nonexistent tag, wheel, or manifest;
- the wheel digest differs;
- a chapter imports the mutable source tree;
- a chapter references a future tag;
- a tag lacks compatibility tests for all earlier public APIs;
- an unchanged historical chapter's stdout moves.

CI placement is cost-aware:

1. **Per pull request:** install and test the current harness tag and the immediately
   previous tag, execute the touched chapter smoke witness, and run pin/digest/static
   compatibility audits. This stays O(1) in book length.
2. **Weekly scheduled:** run the full historical-tag matrix, checking out every
   harness tag and running its cumulative suite; also perform clean chapter execution
   without freeze caches.
3. **Release gate:** run the full historical-tag and clean-execution matrices again,
   regardless of the most recent scheduled result.

A changed compatibility layer may opt into additional affected tags on a pull
request. The default pull-request matrix does not grow to O(N²) as chapters accrue.

### Capability growth

The expected additions are a design roadmap:

| Stage | Harness capability |
|---|---|
| C01 | device/dtype/seed ledger, synchronized timing, bytes moved, operational intensity |
| C02 | stable streaming moments and associative merge checks |
| C03 | ULP/range/cancellation/quantization diagnostics |
| C04 | quadratic eigendirection and stochastic-noise simulator |
| C05–C06 | empirical tails, QQ diagnostics, concentration and clipping audit |
| C07–C10 | nets, operator norms, spectra, condition/stable/effective-rank analyzers |
| C11 | VJP/JVP/checkpointing teaching utilities |
| C12 | HVP and top-eigenvalue estimation |
| C13 | gradient-noise and regime recorder |
| C14 | activation, gradient, and Jacobian-flow recorder |
| C15 | normalization axes and precision audit |
| C16 | curvature/loss edge-of-stability recorder |
| C17 | update norm, angle, spectrum, state, and routing recorder |
| Synthesis | retained-state, IO-aware kernel, and scan correctness/ordering audits |

---

## 6. Hardware contract

### Provenance classes

Every book-generated numerical claim receives exactly one hardware provenance:

- **(a) Laptop-CPU reproducible:** executed in the chapter under a bounded runtime and
  pinned software environment.
- **(b) CPU-simulable:** the phenomenon is reproduced through explicit dtype,
  quantization, memory-traffic, or reduced-scale simulation; the prose states which
  hardware behavior is simulated rather than measured.
- **(c) Pinned artifact only:** the endpoint comes from a declared GPU/cluster study
  and is committed as machine-readable evidence with full run provenance.

No book-generated number appears without a claim ID that resolves to one of these
classes. A number quoted only to audit a primary paper receives an
`external-primary-source` claim record with exact table/figure/page and is labeled as
reported evidence, not reproduced evidence. It cannot substitute for the chapter's
opening witness or for a result asserted by this book.

### Act-opening classifications

| Act | Opening phenomenon | Class | Contract |
|---|---|---|---|
| Act 0 | A low-arithmetic operation is slower than expected because it moves too many bytes | **(a)** | Reproduce on laptop CPU with a measured local roofline. Any HBM/A100/H100 comparison is separate class (c) evidence. |
| Act I | Norms and angles become more predictable as ambient dimension grows | **(a)** | Seeded NumPy/PyTorch CPU experiment plus exact finite-dimensional calculation. |
| Act II | Signals/gradients disappear or explode across depth before useful learning begins | **(b)** | Explicit dtype casts and controlled compositions on CPU. Do not present CPU FP16 timing as accelerator performance. |
| Candidate Act III | An exact all-pairs kernel with the same mathematical output changes runtime by changing data movement | **(c)** | CPU code supplies correctness and online-normalizer witnesses; performance endpoint comes from a pinned accelerator artifact. |

### Core chapter phenomenon preclassification

This table shapes budgets before chapter contracts are written. A later contract may
make a class cheaper, but it may not silently demote a laptop witness to
pinned-artifact-only.

| Unit | Marquee phenomenon | Primary class | Scale-extension rule |
|---|---|---|---|
| C01 | Arithmetic count fails to predict runtime when byte movement dominates | **(a)** | Accelerator roofline panel may be (c); local measured roofline remains. |
| C02 | Naïve variance is memory-heavy or numerically wrong; one stable state repairs both | **(a)** | No class (c) endpoint planned. |
| C03 | Overflow, underflow, cancellation, update loss, and grid collapse follow from a precision contract | **(b)** | Exact format facts and integer checks may be (a); accelerator throughput is not part of the opening claim. |
| C04 | Quadratic modes decay, oscillate, stall, or hit a noise floor at predictable rates | **(a)** | No scale endpoint needed. |
| C05 | Norms and sums become predictable in the sub-Gaussian safe zone | **(a)** | No scale endpoint needed. |
| C06 | Squaring/products create a two-regime tail and expose clipping boundaries | **(a)** | Small seeded CPU samples plus exact distribution checks. |
| C07 | A finite net controls a continuous worst-direction question | **(a)** | No scale endpoint needed. |
| C08 | Random operators have controlled singular-value behavior despite many entries | **(a)** | Optional larger spectra remain CPU unless a hardware claim is added. |
| C09 | Null spectra form a bulk with edges; finite-size signal must be distinguished from fluctuation | **(a)** | Any trained-frontier spectrum is supplementary (c), never the sole witness. |
| C10 | Effective/stable rank changes while parameter count does not | **(a)** | Model-scale example may be external-source or (c), with a small CPU construction retained. |
| C11 | Reverse accumulation saves arithmetic while retained state creates a memory cost | **(a)** | Checkpointing scale panel may be (c); the VJP/recomputation witness remains CPU. |
| C12 | Small-network curvature spectra distinguish minima, saddles, and Gauss–Newton structure | **(a)** | Autograd HVP/Lanczos or power iteration on a small network; larger spectra are optional (c). |
| C13 | Gradient noise changes regime and cannot be diagnosed by variance alone | **(a)** | External large-model tail studies are paper audits, not replacements. |
| C14 | Signal and Jacobian scales vanish or explode before the first useful update | **(b)** | Explicit casts and reduced compositions; optional accelerator depth panel is (c). |
| C15 | Normalization axis and arithmetic alter curvature and precision behavior | **(b)** | Mathematical/Jacobian checks may be (a); production-kernel timing is optional (c). |
| C16 | Progressive sharpening drives $\lambda_{\max}(H)$ toward the discrete-time stability boundary | **(a)** | Required CPU study: full-batch gradient descent on a small network/data subset with top-Hessian eigenvalue tracked by autograd HVP power iteration in minutes. A frontier-scale trace is supplementary (c) only. |
| C17 | Matrix-aware/quantized updates change norm, spectrum, routing, state, and cost | **(a)** for small kernel/invariant witnesses | Muon/QJL published endpoints are `external-primary-source`; any original scale comparison is (c). No borrowed endpoint is presented as reproduced. |

Plan v2 does not yet estimate GPU-hours row by row; D15 authorizes that work at
chapter-contract time. This classification makes clear that the signature C16
phenomenon is locally reproducible.

### Artifact schema

Every class (c) result uses committed JSON with at least:

```json
{
  "claim_id": "c16-progressive-sharpening-001",
  "phenomenon_id": "phen-c16-progressive-sharpening",
  "chapter": "c16",
  "hypothesis": "...",
  "commit": "...",
  "harness_ref": "ch-16",
  "config_sha256": "...",
  "seeds": [6210, 6211, 6212],
  "data_roles": {"development": "...", "sealed_endpoint": "..."},
  "hardware": {"cluster": "Rivanna", "gpu": "...", "count": 1},
  "scheduler": {"job_ids": ["..."], "allocation": "..."},
  "software": {"python": "...", "pytorch": "...", "cuda": "..."},
  "dtype_contract": {"storage": "...", "compute": "...", "accumulation": "..."},
  "metric": "...",
  "estimator": "...",
  "denominator": "...",
  "uncertainty": "...",
  "result": {},
  "source_artifacts": [],
  "artifact_sha256": "..."
}
```

Cluster runs additionally retain configuration, stdout/stderr, failure accounting,
stopping rule, job matrix, GPU-hour estimate, and compact reduced artifacts. Large
raw outputs remain on managed storage under a retention policy; the book never
depends on a live cluster path.

### Hardware-claim boundary

- A roofline is an upper bound, not a stopwatch.
- A CPU simulation can demonstrate a mathematical failure but not an accelerator
  throughput claim.
- Do not present CPU FP16 timing as accelerator performance.
- A dtype label does not fully specify storage, multiplication, accumulation, output,
  or optimizer-state precision.
- A performance comparison reports warmup, synchronization, transfer inclusion,
  sample count, central tendency, spread, and machine state.
- Hardware model/specification numbers are dated and sourced to official
  documentation; measured numbers are artifacts.

---

## 7. Slide-to-chapter conversion protocol

### Source hierarchy

For each chapter:

1. approved chapter contract;
2. current instructor-created slides, handouts, notes, code, and explanations;
3. current assignments and observed student difficulties;
4. primary scholarly and official technical sources;
5. legacy DS 6210 book as recoverable examples/figures only;
6. outside lectures and textbooks as reference-only cross-checks.

### What survives

- the opening phenomena and prediction questions;
- derivation order when it expresses the instructor's causal logic;
- original small examples and numerical witnesses after recomputation;
- figures whose instructional job survives the medium change;
- theorem choices and literature bridges after source verification;
- cross-lecture callbacks that become book-level seed/harvest obligations;
- assignment failure modes that can be converted into non-overlapping exercises.

### What is rewritten from scratch

- all prose;
- slide transitions, pacing language, and classroom directions;
- telegraphic bullets;
- claims that depend on an off-page demonstration;
- every figure caption and alt text;
- code narration and experimental protocol;
- proof exposition;
- recaps, field notes, audits, and Sources sections.

Mechanical TeX-to-Quarto conversion is allowed only as an extraction aid for
equations, TikZ, and citations. Its output never becomes the prose skeleton.

### Pipeline

1. Designate canonical slide `.tex`, compiled PDF, handout/notes, and code.
2. Snapshot them into a private provenance area with checksum and reuse status.
3. Extract a slide ledger: phenomenon, prediction, derivation, figure, code,
   citation, callback, exercise candidate.
4. Build the chapter contract and sibling ownership split.
5. Re-derive mathematics and recompute hand-checkable numbers independently.
6. Prototype the smallest discriminating experiment before writing claims.
7. Draft prose from the contract and instructor explanation, not from converted
   bullets.
8. Rebuild or redraw figures for HTML/PDF accessibility.
9. Execute with the pinned harness/environment and freeze evidence.
10. Run residue, provenance, math, code, apparatus, accessibility, and length audits.
11. Render HTML and PDF; inspect changed pages and responsive layouts.

### Residue tripwires

`scripts/audit_public_voice.py` scans visible prose for:

- `as the slide shows`, `on this slide`, `the slide`, `next slide`;
- `in lecture`, `the lecture`, `this lecture`, `the lectures`;
- `in class`, `our class`, `today we`, `this week`, `next week`, `last week`;
- `we saw`, `we discussed`, `we covered`, `we will cover`, `we'll see later` when
  they refer to classroom chronology rather than a stable chapter;
- `as I showed`, `as I said`, `on the board`, `pause here`;
- `the seed's`, `seed notes`, internal `.tex` paths, and draft filenames;
- frame-title fragments or headings with no finite verb;
- `\pause`, `\only`, `\uncover`, `\onslide`, `\visible`, `\frametitle`,
  `\begin{frame}`, Beamer overlay specifications, and speaker notes;
- first-person-plural classroom deixis.

Collaborative “we” remains allowed when the book itself performs the action:
“we now bound the operator norm” is book voice; “we saw this last Tuesday” is
classroom residue.

### Pilot chapter

**Recommendation: C02, “One pass, two failures: streaming state and stable
variance.”**

**Provisional displacement budget:** approximately 6,500 prose words and no more
than 22 pages in the derived PDF. This is a pilot cap, calibrated to the sibling's
median chapter scale, not a target to fill. Material that does not serve the
chapter's causal chain is moved to an exercise, appendix, later callback, or source
pointer. The clean laptop-CPU execution budget is recorded in the chapter contract
before implementation.

Why it is the right pilot:

- small and self-contained;
- opens with an observable failure;
- exercises memory, numerical stability, and parallel-reduction threads;
- requires the first nontrivial harness pin and compatibility rule;
- supports laptop-CPU evidence;
- forces an explicit Appendix C ownership split;
- has recoverable local figures and a refined legacy chapter, so the conversion
  protocol can be tested against both useful material and residue risk;
- closes a loop inside the chapter while planting later normalization and parallel
  scan callbacks.

Pilot acceptance criteria:

- one complete Problem → Diagnosis → Theory → Solution → Audit causal chain;
- full Welford and merge-invariant derivations checked independently;
- exact sibling boundary;
- first `harness@ch-02` immutable artifact;
- class (a) evidence only;
- Plan → Code parity;
- HTML/PDF equivalence and accessibility checks;
- conversion-residue audit with zero findings;
- no more than approximately 6,500 prose words or 22 derived-PDF pages without an
  explicit displacement decision;
- bootstrap `contracts/promises.yml` with the pilot's first front-matter/apparatus
  promises, their owning checks, scope, and status, so invariant (f) is exercised
  before the front matter hardens;
- page, word, and clean-execution budgets reported before moving to the next chapter.

### Materials request — one consolidated checklist

Please provide or designate the following as a single handoff. Items already present
locally need only a canonical-version confirmation.

- [ ] **Slide sources:** canonical Spring 2026 `.tex` files **and their compiled
  PDFs**, including any speaker notes or live-demo code that changes the explanation.
  The local tree contains many candidate/current/old variants; mark which files are
  authoritative rather than resending duplicates.
- [ ] **Spring 2026 syllabus and assignments:** identify the authoritative syllabus
  (`my_lectures/Syllabus_simple.tex` appears current), and provide/designate all
  homework prompts, notebooks, rubrics, take-home material, and nonpublic solutions
  that may inform but must not leak into public exercises.
- [ ] **Existing harness code:** the actual Spring 2026 lab/training harness,
  environment files, notebooks, benchmark scripts, seeds, and any cluster artifacts.
  No course-wide harness implementation was found in the reviewed tree. If one
  exists elsewhere, provide it before the pilot so D21 can adjudicate recovery
  against book-first design; otherwise confirm book-first genesis.
- [ ] **Student feedback:** anonymized surveys, muddiest-point notes, office-hour
  patterns, assignment postmortems, and corrections. State what may be quoted,
  paraphrased, or used only as private editorial evidence.
- [ ] **Resource shelf:** confirm that the current local `Resources/`,
  `Others lectures/`, and `course projects/papers/` directories are the intended
  shelf; identify priority sources and any licensing/permission limits, especially
  for student projects and copied lecture material.

---

## 8. Infrastructure and edition policy

### Repository and stack

Use the confirmed repository:

> `Shakeri-Lab/opt-book`

Inherit the sibling's proven stack:

- Quarto book;
- canonical HTML with MathJax;
- derived PDF using LuaLaTeX;
- Python 3.12, PyTorch, NumPy, Matplotlib, and small supporting libraries;
- committed freeze artifacts for publication;
- GitHub Pages from `gh-pages`, generated from `main`;
- source/provenance, figures, data, artifacts, filters, scripts, and durable docs
  separated in the repository;
- text/figure and code licenses recorded separately.

Add a fully resolved Python lock and exact Quarto/TinyTeX expectations from the first
commit. The virtual environment stays outside Box; GitHub is the source of truth.

### Minimum first-commit structure

```text
.github/workflows/
chapters/
docs/
  BOOK-BRIEF.md
  STYLE-GUIDE.md
  ARC-SEEDS.md
  CONTINUING.md
  NEW-CHAT-PROMPT.md
  BACKLOG.md
  BUILD-PLAN-v2.md
contracts/
  notation-covenant.yml
  promises.yml
  threads.yml
  branding-vocabulary.yml
harness/
artifacts/
figures/
scripts/
sources/                 # governed snapshots only
private-ledgers/         # excluded from public render
_quarto.yml
index.qmd
CITATION.cff
CHANGELOG.md
README.md
```

Create these only after the plan is approved; do not scaffold chapters from the
candidate table prematurely.

### Canonical-edition statement

The colophon and index contain, from the first public commit:

> The HTML edition is canonical; the PDF is a derived, content-equivalent print
> conversion. Differences are limited to pagination, float placement, line breaking,
> and other presentation requirements.

The statement appears exactly once in the front matter and is mechanically audited.

### Accessibility posture

**Recommendation: attempt a tagged PDF from the first commit, rather than inheriting
the sibling's retrofit backlog.**

The HTML remains canonical and must satisfy semantic-heading, keyboard, contrast,
link-name, table-header, and substantive figure-alt-text checks. The derived PDF
starts with LuaLaTeX's current `tagpdf` path enabled and is tested for:

- a document structure tree with headings, paragraphs, lists, tables, links, and
  figures in a coherent reading order;
- meaningful alternative descriptions for figures;
- `/ActualText` for figure-embedded text that is not otherwise represented,
  mathematical substitutions when extraction would be misleading, and semantic
  callout labels; purely decorative callout icons are marked as artifacts or receive
  empty replacement text rather than polluting the text layer;
- artifact, link, language, title, and author metadata;
- readable extraction without NUL/replacement characters or missing glyphs.

“Tagged” is not presented as “PDF/UA conformant” unless an external validator and a
manual reading-order sample both pass. Use a version-pinned `tagpdf`/LuaLaTeX
fixture from the first commit so regressions are caught while the book is small.

If the toolchain blocks a valid render, the fallback is explicit rather than silent:
retain HTML accessibility, alt text, clean extraction, and every feasible
`/ActualText` annotation; commit the smallest failing fixture and toolchain log;
record the unsupported semantic structures, owner, and review date in
`docs/BACKLOG.md`; and keep tagged output as a release gate under active review.
D24 chooses this first-commit attempt versus knowingly accepting sibling parity.

### Edition and citation policy

- `v0.x`: draft editions; anchors may move, but releases are fixed and citable.
- `v1.0`: first stable complete book.
- patch releases correct errors without changing the arc;
- minor releases add or materially revise instructional units;
- a release attaches its source archive and PDF;
- the live site may advance beyond the latest stable release, and says so plainly.

Suggested citation block:

> Shakeri, Heman. 2026. *Deep Learning: Making It Trainable*. Version X.Y.
> School of Data Science, University of Virginia.
> https://shakeri-lab.github.io/opt-book/

`CITATION.cff`, colophon, index, release tag, and attached PDF version must agree.

### Label namespace

Use one explicit unit ID per numbered chapter, interlude, appendix, and epilogue.
Figures, tables, listings, exercises, and equations derive their prefixes from that
unit in both formats. Interlude/epilogue equations may not silently inherit the
previous numbered chapter.

Implement one unit-prefix metadata field and a Lua filter that produces the same
prefix in MathJax/HTML and LuaLaTeX/PDF. Add fixture units to CI on day one; do not
wait for the first interlude.

### CI invariants active from first commit

| Invariant | Enforcement |
|---|---|
| PDF text contains no U+0000 or U+FFFD | `pdftotext -enc UTF-8` scan |
| LuaLaTeX reports no `Missing character` | retained-log scan |
| No slide/classroom/public-source residue | `audit_public_voice.py` |
| Every Equation/Figure/Exercise reference resolves | source label graph plus built HTML/PDF unresolved-reference scan |
| One unit namespace for figures **and equations** in both editions | HTML DOM and extracted-PDF fixture tests |
| Every front-matter promise is auditable and audited | promise registry with script/test owner |
| Every executable chapter has an immutable harness pin | `audit_harness_pins.py` |
| No suspicious per-page dictionary-word ratio | page-separated PDF extraction and threshold/report, with technical-token allowlist |
| Every HTML figure has substantive alt text | DOM audit; reject filename-only or caption-duplicate placeholders |
| PDF structure and nonvisual equivalents are intentional | tagged-PDF fixture, structure-tree/reading-order checks, `/ActualText` audit, and validator report; apply the documented fallback only under D24 |
| Every visible code surface has Plan → Code mapping | adapted sibling audit |
| Exercise tags are canonical | manuscript audit |
| De-branding rules hold without ordinary-language false positives | context-regex/severity linter plus allowed-sentence and violation golden files |
| Thread callbacks do not go silent after their registered seed | seed-aware `audit_threads.py`; pre-seed acts are exempt |
| Core notation is not redefined and extensions are declared | `audit_notation_covenant.py` against `contracts/notation-covenant.yml` |
| Every theorem names the phenomenon it explains | theorem metadata audit |
| Every printed number has provenance | claim-ID and artifact/source audit |
| Frozen outputs agree with executed outputs | scheduled clean execution audit |
| Source links and external anchors are healthy | link audit, with failures reported even if transient links are not publication-blocking |
| Cross-book public interfaces remain reciprocal | opt-book link audit plus the sibling's `docs/public-anchors.md` contract once D23 is approved |

#### Dictionary-word-ratio scan

Split extracted PDF text by form feed and compute, per page:

- alphabetic tokens;
- dictionary-recognized tokens;
- mathematical/code/identifier tokens admitted by an allowlist;
- recognized-word ratio and longest run of unrecognized alphabetic tokens.

Fail only on a calibrated low ratio **and** a suspicious run, so a theorem-heavy page
does not fail merely for notation. The primary target is figure-embedded text lacking
a ToUnicode map. Store the report as a CI artifact and raster-inspect flagged pages.

#### Cross-reference integrity

Source audit:

- every reference target exists;
- every label is unique;
- target kind matches the reference kind;
- no reference points to a future placeholder;
- every exercise pointer resolves to an actual numbered exercise.

Build audit:

- no Quarto/Pandoc unresolved-reference warnings;
- no literal `@fig-`, `@eq-`, `@exr-`, `??`, or missing-link placeholder survives
  in HTML/PDF;
- unit prefixes agree across editions.

### Workflow separation

1. **Fast pull-request contract audit:** prose, branding, labels, apparatus, Python
   parsing, harness pins, artifact schemas, plus the current and immediately previous
   harness tags. Touched chapters run their smoke witnesses; the default matrix stays
   O(1) in chapter count.
2. **Render audit:** canonical HTML plus derived PDF, glyph/text/accessibility checks,
   including the tagged-PDF fixture.
3. **Weekly scheduled clean execution:** delete freezes, install every historical
   chapter pin in clean environments, run the full tag matrix and every executable
   unit.
4. **Release audit:** repeat the full historical matrix and clean execution, then
   check version/citation parity, full visual diff, links, artifacts,
   source/provenance, and live deployment verification.

Publishing remains an explicit authorized action; a local successful render is not a
deployment claim.

---

## 9. Proof policy

### Proof modes

Every theorem-like entry declares:

- **Phenomenon explained**
- **Assumptions**
- **Conclusion**
- **Proof mode**
- **Diagnostic corollary**
- **Boundary**
- **Source**

Allowed proof modes:

1. **Full proof:** all load-bearing steps appear in the book.
2. **Proof with pointer:** the book proves the diagnostic step and gives a precise
   source for machinery whose full development would derail the arc.
3. **Diagnostic corollary:** the upstream result is stated and scoped; the usable
   finite consequence is derived exactly.
4. **Model calculation:** exact only inside a declared simplified model; never styled
   as a general theorem.

Every theorem must answer “what observable failure or regularity does this explain?”
CI rejects theorem blocks with no phenomenon anchor.

### Act-level policy

| Act | Default proof mode | Full-proof commitments | Pointer/corollary commitments |
|---|---|---|---|
| Act 0 | Full derivation and model calculation | Welford/Chan invariants; floating-point local error examples; exact quadratic mode dynamics; stability intervals; operational-intensity arithmetic | Hardware behavior sourced to standards/official docs; detailed error-analysis results pointed to Higham-style primary texts where needed |
| Act I | Mixed full proof and proof-with-pointer | Chernoff method for core scalar bounds; sub-Gaussian equivalences at usable granularity; products/squares consequences; epsilon-net bridge; finite operator-norm bounds in representative form | Marchenko–Pastur convergence, advanced matrix Bernstein, and sharp covariance-estimation results use precise pointers to Vershynin/Wainwright/Bach or primary papers; finite diagnostic corollaries are exact |
| Act II | Full proof in tractable models; primary-paper pointers for modern phenomena | Quadratic/local linear stability; Jacobian variance recursions in declared models; normalization Jacobians where load-bearing; Newton–Schulz kernel invariant and convergence regime | Saddle complexity, dynamical isometry generality, edge-of-stability results, heavy-tail optimization, and modern optimizer claims use primary-paper statements with exact assumptions; book derives the diagnostic consequence |
| Candidate Act III | Algorithm-invariant proofs plus research pointers | Online softmax invariant; tiling equivalence; scan associativity in exact arithmetic; finite-precision order counterexample | NTK limits, HiPPO approximation results, and finite-width feature-learning theory use proof-with-pointer and exact diagnostic corollaries |

### Source targets

- Act I: Vershynin, Wainwright, Bach, and primary random-matrix/concentration papers.
- Act II: primary papers for saddle geometry, dynamical isometry, normalization
  mechanism, edge of stability, matrix-aware optimizers, and quantized/sketched
  training.
- Standards and official technical documentation for numeric formats and hardware
  contracts.

Secondary texts may help triangulate a proof but do not silently become the public
source of a load-bearing theorem.

### Proof audit

For each numbered equation and theorem:

1. re-derive independently;
2. check dimensions and reduction axes;
3. identify deterministic versus probabilistic claims;
4. state finite/asymptotic status;
5. test one small numerical witness;
6. verify the cited theorem's assumptions and numbering against the actual edition;
7. ensure the prose does not enlarge the source's conclusion.

---

## 10. Shelf audit plan

### Goal

Turn the resource shelf into a provenance-aware source map, not a bibliography dump.
Every retained source must serve a chapter claim, proof, figure, diagnostic, or
exercise. Every candidate exercise must be deduplicated against this book and the
sibling.

### Source classes

| Class | Local examples | Default use |
|---|---|---|
| Instructor-canonical | `my_lectures/`, syllabus, handouts, journal clubs, project specifications | Primary source for voice, order, examples, and intended transformations |
| Primary scholarly/official | original papers, IEEE/format docs, hardware vendor docs | Load-bearing theorem, historical, algorithm, or hardware claims |
| External reference-only | `Others lectures/`, outside textbooks/notes | Cross-check, omission detection, alternative proof route; never hidden prose skeleton |
| Legacy draft | `old/DS6210_Book/`, older lecture variants | Recoverable figure/example/idea after re-verification |
| Generated/frozen evidence | notebooks, JSON, figures, cluster summaries | Numerical claims with hashes and protocol |
| Student work | `course projects/` archives and reports | Private evidence of confusion/possibility unless explicit reuse permission exists |

### Audit phases

1. **Inventory and fingerprint**
   - path, size, checksum, file type, page count, extractability;
   - duplicate and near-duplicate detection;
   - archive contents listed without execution.
2. **Bibliographic normalization**
   - title, authors, year, venue, DOI/arXiv/official URL, edition;
   - primary/secondary status;
   - license and public-reuse status.
3. **Chapter mapping**
   - candidate unit;
   - load-bearing claim/proof/figure/exercise role;
   - exact page/section/theorem;
   - evidence status.
4. **Exercise mining**
   - concept tested;
   - tempting wrong answer;
   - acceptance criterion;
   - whether it overlaps graded Spring 2026 work;
   - whether it duplicates a sibling exercise.
5. **Deduplication**
   - normalize exercise signatures by object, requested action, dataset, and intended
     misconception;
   - compare against both books' exercise ledgers;
   - merge, redirect, or reject collisions.
6. **Gap report**
   - chapters with no primary source;
   - claims supported only by lecture slides;
   - missing editions/pages;
   - licensing or permission blockers;
   - exercise modes or terminal capabilities not yet represented.

### Shelf-ledger outputs

Private:

- `private-ledgers/sources.csv`
- `private-ledgers/source-chapter-map.csv`
- `private-ledgers/exercise-candidates.csv`
- `private-ledgers/permissions.csv`
- `private-ledgers/duplicate-report.md`

Public:

- chapter `Sources and further reading`;
- repository provenance/licensing summary;
- third-party notices where required.

### Initial routing priorities

1. Act 0 textbooks/official documents: numerical optimization, numerical linear
   algebra, machine-learning systems, format/hardware specifications.
2. Act I: Vershynin, Bach, Wainwright-compatible sources, and primary
   concentration/random-matrix papers.
3. Act II: Roberts–Yaida plus primary papers on saddles, dynamical isometry,
   normalization, edge of stability, Muon/Shampoo/SOAP, and QJL/TurboQuant.
4. Spring 2026 project papers: evidence-discipline and optimizer-card exercise
   candidates.
5. Candidate synthesis sources only after the Act III scope decision.

### Shelf acceptance rule

A source enters a chapter contract only if its exact role is named. “Good background”
is not a role.

---

## Author-decision queue

Items marked **resolved by author** record explicit decisions in the refinement
brief; none were resolved by editorial assumption. Open items retain a recommendation
so the author can approve, revise, or reject them directly.

1. **D01 — Title and subtitle.**
   **Title resolved by author:** *Deep Learning: Making It Trainable*. Decide whether
   the public title carries the optional subtitle *Geometry, Dynamics, and the
   Machine*.
   **Recommendation:** retain the family title alone on the cover and use the phrase
   as descriptive metadata only if discovery testing shows it helps.

2. **D02 — v1 scope.**
   Decide whether v1 ends with the Acts 0–II research-paper capstone (C17) or includes
   the six-unit synthesis extension.
   **Recommendation:** contract and pilot the 17-unit core first; keep Act III in the
   arc ledger until the core page/runtime budget is known.

3. **D03 — Candidate core arc.**
   Approve the provisional C01–C17 transformations as a planning basis, with chapter
   count still adjustable by merging.
   **Recommendation:** approve as contracts, not as empty chapter stubs.

4. **D04 — Convex baseline depth.**
   Decide whether convex surrogates receive a short unnumbered bridge inside C04 or a
   numbered chapter.
   **Recommendation:** bridge plus sibling pointers; the new ownership is dynamics,
   conditioning, and diagnostic control, not first-course loss mechanics.

5. **D05 — Precision/roofline split with the sibling.**
   Approve the rule that Appendix C owns introductory mechanics while this volume owns
   error theory, instrumentation, quantitative diagnosis, and hardware-evidence
   contracts.
   **Recommendation:** approve and enforce a one-recap duplication budget.

6. **D06 — Public thread count.**
   Choose four public threads from the kickoff brief or all six from the longer course
   vision.
   **Recommendation:** four public sigils; retain memory/retained-state and
   orthogonality/scale as internal cross-cutting ledgers until the pilot shows whether
   six remain readable.

7. **D07 — Exercise taxonomy.**
   **Resolved by author:** keep exactly `(Pencil.)`, `(Code.)`, `(Audit.)`; use
   “Profile” and “Paper audit” as named subtypes. No fourth formal tag.

8. **D08 — De-branding strictness.**
   Approve the context-aware `(term, context_regex, severity)` vocabulary, its golden
   allowed/violation sentences, and the rule that standard names appear only in
   Rosetta, Sources, first-use bridges, paper audits, search metadata, and unavoidable
   APIs.
   **Recommendation:** approve, then add fixtures rather than muting a noisy rule.

9. **D09 — Generic phrase for model class.**
   Confirm whether “deep compositional structure” should replace “neural network” in
   all generic prose or only where composition is the property under study.
   **Recommendation:** use it where mathematically accurate; use “parameterized
   model” elsewhere rather than forcing one phrase beyond its scope.

10. **D10 — Pilot chapter.**
    **Resolved by author:** C02, streaming state and stable variance, is the first
    authored pilot, under the provisional 6,500-word/22-page cap and acceptance
    criteria in §7.

11. **D11 — Harness pin implementation.**
    Approve annotated tags plus committed content-addressed wheels and per-chapter
    manifests, rather than a live Git dependency.
    **Recommendation:** approve for offline reproducibility and historical execution.

12. **D12 — Harness API audience.**
    Decide whether students install the package directly or receive a course template
    repository that already pins it.
    **Recommendation:** template repository for the live course; the book documents
    the pin and mechanism, not package-management ceremony.

13. **D13 — Proof budget.**
    Approve the act-level proof modes and identify any theorem that must receive a
    full proof regardless of length.
    **Recommendation:** approve the mixed policy; reserve full proofs for reusable
    diagnostic machinery.

14. **D14 — Edition size budget.**
    Set target word/page/runtime budgets before chapter drafting.
    **Recommendation:** decide after the pilot by extrapolating its canonical HTML
    word count, derived PDF pages, and clean execution time. The pilot itself already
    has a provisional displacement cap so this deferral does not suspend discipline.

15. **D15 — Hardware endpoint policy.**
    Approve laptop witnesses for every chapter and pinned cluster artifacts only when
    scale is necessary.
    **Recommendation:** approve the one-row-per-chapter preclassification in §6;
    predeclare GPU-hour budgets study by study, keeping C12 and the required C16
    signature witness class (a).

16. **D16 — Student-work reuse.**
    Decide whether student projects may inform exercises privately, be cited with
    permission, or be excluded from publication.
    **Recommendation:** private editorial evidence by default; public reuse only with
    explicit written permission and attribution.

17. **D17 — License family.**
    Decide whether to inherit sibling licensing: CC BY-NC-SA 4.0 for text/figures and
    MIT for code.
    **Recommendation:** inherit unless a source/provenance review identifies a
    conflict.

18. **D18 — Release model.**
    Approve rolling HTML plus fixed tagged source/PDF releases with `v0.x` drafts and
    a later `v1.0`.
    **Recommendation:** approve.

19. **D19 — Public Rosetta placement.**
    Decide whether Rosetta is an appendix in the main reading route or a standalone
    reference page outside the numbered arc.
    **Recommendation:** appendix plus generated per-term redirects.

20. **D20 — Canonical Spring 2026 source designations.**
    Resolve current-versus-old variants in the five-item materials checklist,
    especially `Syllabus_simple.tex` versus the older `Later/Syllabus_v6.tex`.
    **Recommendation:** treat `Syllabus_simple.tex` as the current course contract
    unless the author designates otherwise; use `Syllabus_v6.tex` as a source for the
    candidate synthesis extension.

21. **D21 — Harness genesis.**
    Decide between book-first design informed by the Spring 2026 notebooks and
    recovery/refactor of any course-wide lab code held outside the reviewed tree.
    **Recommendation:** book-first design. Provide any extant harness code in the
    materials handoff before the pilot; if none exists, confirm that the small
    `harness@ch-02` package is the harness's genesis.

22. **D22 — Notation covenant with the sibling.**
    Approve inherit-and-extend notation, the ban on redefining sibling core symbols,
    “new in this volume” markers for additive notation, and the machine-checked
    covenant at `contracts/notation-covenant.yml`.
    **Recommendation:** approve the covenant and file location.

23. **D23 — Reciprocal cross-book interface.**
    Approve committing `docs/public-anchors.md` to `dl-book` now with its own anchor
    CI, and gate the five-surface back-reference patch plus mutual colophon pointers
    on stable opt-book anchors at approximately v0.2.
    **Recommendation:** approve both halves; publish the later back-reference patch
    as a sibling v1.2.x point release only after the opt-book targets are stable.

24. **D24 — Accessibility posture.**
    Decide between attempting tagged PDF plus `/ActualText` from the first commit and
    carrying PDF semantics as a sibling-parity retrofit backlog.
    **Recommendation:** attempt it from the first commit, without claiming PDF/UA
    conformance until validation passes; use the documented fixture-and-backlog
    fallback only if the version-pinned toolchain blocks a valid render.

---

## Implementation authorization

The author authorized implementation on 2026-07-30. The durable project memory,
contracts, accessibility fixture, CI skeleton, C02 chapter contract, five-operation
harness genesis, provenance records, and pilot manuscript now exist locally. The
pilot remains unpublished until its source commit, annotated harness tag, and
release checks exist; those publication steps require separate authorization.
