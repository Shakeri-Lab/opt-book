# Style Guide

## Voice

- Begin with a failure, puzzle, or physical constraint.
- Ask for a prediction before revealing the diagnostic.
- Write as a self-contained book, never as a lecture transcript.
- Collaborative book voice is allowed: “we now bound the error.”
- Classroom deixis is not: “we saw this last week.”
- Prefer direct technical prose. Use em dashes sparingly.
- Name the seductive wrong answer when it helps the reader recognize a trap.
- Let one load-bearing carry line stand as its own paragraph when the prose
  has earned it. Do not box, label, decorate, or collect those lines.
- Use no chapter epigraphs. The opening phenomenon performs that job.
- Avoid exclamation points, congratulatory second-person language,
  journey/adventure metaphors, mascots, and ornamental margin devices.

## Chapter architecture

The reasoning order is:

> Problem → Prediction → Instrumentation → Diagnosis → Theory → Solution →
> Audit → Recap

These are obligations, not mandatory visible headings. Each section has one
instructional job, one primary representation, and one check.

Every numbered chapter ends with:

1. one Check yourself box containing questions, not worked answers;
2. a five-slot “Okay, so —” recap: inherited, changed, instrumented,
   established, unresolved;
3. Sources and further reading;
4. Exercises using the canonical three tags.

This Sources-before-Exercises order is inherited from the sibling's current
edition.

The Unresolved slot is always a question. It should state the question that
the next opening phenomenon forces, not append a miniature preview of the
answer.

Every Sources section ends with one concise **Reading order.** sentence that
tells a research-facing reader which source to open first and why. It does not
become a literature survey.

Each act divider is an authored interlude of roughly 120 words. In ledger
voice, it names what the previous act built, what remains impossible, and why
the next lens is needed.

The introduction is unnumbered front matter. A numbered chapter declares the
offset implied by its C-number, so an unwritten earlier chapter never causes a
temporary renumbering.

Below the public thread sigil, show a compact lens ledger in the fixed order
`Geometric · Dynamic · Algorithmic`. Each lens is marked `primary`,
`supporting`, or `quiet`. The chapter contract holds the rationale.

A Prediction box must preserve a live choice. It offers at least two rival
explanations or asks for a named discriminating control, and it never contains
its own answer.

## Terminology

Debranding is show-then-name, not suppression.

- Use the mathematical primitive before a branded family name.
- At the first sanctioned naming point, use a `brand-bridge` aside.
- The bridge states the standard name, scope, variants, and primary source.
- Branded search aliases live in metadata and the Rosetta appendix.
- Every Rosetta row naming a specific published artifact carries that
  artifact's primary citation; generic techniques may instead point to the
  owning section.
- Ordinary English must not trigger the branding linter.

When ingesting statistical-physics theory, explain the diagnostic object
before permitting its standard term:

| Source vocabulary | House diagnostic language |
|---|---|
| susceptibility | fixed-point gain |
| edge of chaos | contraction/expansion boundary for pair separation |
| universality class | shared fixed-point and scaling family |
| effective theory | declared-truncation model |

These are source-theory terms, not de-branded primitives, so they do not gain
Rosetta rows. Once the object is established, the standard term may appear in
Sources or a paper audit for discoverability.

## Mathematics

- State shapes before matrix products.
- Name non-obvious reduction axes and denominators.
- Distinguish identity, theorem, model calculation, approximation, heuristic,
  observation, and research frontier.
- Put assumptions next to the conclusion they support.
- Every theorem block declares `phenomenon_id`.
- The full seven-field theorem ledger lives in the chapter contract; the page
  carries only the statement, assumptions needed there, proof policy, and
  phenomenon link.
- Every bibliographic key in a theorem ledger's `source` field appears in that
  chapter's reader-visible Sources section. Internal labels such as
  `elementary-linear-algebra` remain ledger provenance, not citations.
- Use the committed notation covenant. Never redefine a sibling core symbol.
- Distinguish population variance \(M_2/n\) from the usual unbiased sample
  variance \(M_2/(n-1)\).

## Code

Separate:

1. **Equation:** the mathematical object.
2. **Kernel:** the smallest implementation exposing the mechanism.
3. **Harness:** setup, measurement, checking, and display.

The printed-code contract is: equation; a mechanism kernel of roughly 10–25
lines; two or three interpretation-protecting assertions; and one provenance
strip naming claim ID, seed, dtype, device, estimator, and artifact. Exact
harness activation and content verification run in hidden setup through
`book_support.claims`; the complete implementation remains linked and
collapsible in HTML.

Every learner-visible code block has a compact numbered Plan immediately
before it and bracket-only markers such as `# [1]` or `# [2][4]`. Markers do
not repeat the plan prose. Hide only pure plotting layout.

Every study declares seed, data role, device, dtype, software, estimator,
reduction, denominator, controls, and uncertainty when relevant. Published
numbers come from executed artifacts.

New stochastic studies derive independent seeds from a stable claim or
phenomenon identity using the first 32 bits of SHA-256. Legacy literal seeds
remain immutable with their rolling-draft artifacts and are registered in
`contracts/seeds.yml`; a repeated literal is allowed only when the registry
marks the reuse deliberately. A seed coordinates a random stream, not a claim
of robustness across streams.

## Evidence and claims

Claim classes:

- `a`: laptop-CPU reproducible;
- `b`: CPU-simulable hardware/numerical behavior;
- `c`: pinned accelerator/cluster artifact;
- `external-primary-source`: an exactly located result reported by a primary
  source, never represented as reproduced.

Every book-generated number uses a claim ID. A class-c record also carries a
`phenomenon_id`.

## Figures

Every figure must reveal a mechanism, compare predictions, expose a failure,
make a control inspectable, or summarize a state transition. Captions state:

1. what to inspect;
2. what the figure supports;
3. what it does not establish.

HTML figures require substantive alt text. Color is redundant with labels,
line styles, or position.

The canonical figure palette is the UVA-centered family:

| Role | Hex |
|---|---|
| structural navy | `#232D4B` |
| error or boundary wine | `#9C2F2F` |
| control or accepted green | `#2E7D32` |
| intervention orange | `#E57200` |
| secondary blue | `#5379AA` |
| neutral gray | `#6B6B6B` |

Use alpha, line style, marker, and position before adding a new color. Public
chapter source is checked against this whitelist.

Rendered figure bytes use a deterministic environment: `SOURCE_DATE_EPOCH=0`,
`PYTHONHASHSEED=0`, and a noninteractive Matplotlib backend. Explicit
`savefig` calls must pass empty or fixed metadata rather than current times or
machine identities. A changed frozen figure should therefore signal changed
source, changed dependencies, or a deliberately changed rendering contract.

## Exercises

- **(Pencil.)** derive, prove, predict, or reason.
- **(Code.)** implement, simulate, measure, or profile.
- **(Audit.)** judge a claim, proof-to-code gap, protocol, or paper.

Use `(Code.) Profile:` and `(Audit.) Paper audit:` as named subtypes. Split
mixed work into separately tagged subparts.

Paper audits follow `docs/PAPER-AUTOPSY-PROTOCOL.md`. A chapter exercise uses
only the four to six fields supported by the chapter's trunk; it does not
become a miniature literature review. The full card is reserved for the
capstone or a standalone handout.

Every numbered chapter carries at least five exercises, with at least one
Pencil, one Code, and one Audit item. A Paper audit names the selected fields
from the Paper Autopsy Protocol explicitly.

Exercises 1–3 form the **Core** route, Exercise 4 is normally **Extension**,
and Exercise 5 is normally **Research**; any additional item is labeled
explicitly. State an estimated time, prerequisite chapter or tool, expected
deliverable, and whether a hint is available. C04, C10, and C17 end with a
cumulative Incident Card checkpoint for their act.

The public callout taxonomy is closed: Prediction, Named wrong answer, Field
note, and Check yourself. Do not add Key takeaway, Remember, or decorative
summary boxes.

## Public residue forbidden

The public manuscript must not contain slide or classroom residue such as:

- “as the slide shows,” “on this slide,” or “next slide”;
- “in lecture,” “the lecture,” “in class,” or calendar-relative phrasing;
- “we saw” when it refers to classroom chronology;
- frame-title fragments;
- Beamer commands or overlay artifacts;
- internal filenames, local paths, or “the seed's.”

## Accessibility and cross-format parity

- HTML is canonical; both print and continuous screen PDFs carry the same
  content.
- Headings, links, tables, and callouts are semantic.
- Alt text is substantive.
- PDF tagging is attempted from the first build.
- Untagged PDF is an explicit v0.x fallback after a recorded failed attempt;
  validated tagged structure is required before v1.0.
- Semantic figure text and callout labels receive replacement text where
  needed; decorative icons are artifacts.
- Do not claim PDF/UA conformance without a validator and manual reading-order
  check.
