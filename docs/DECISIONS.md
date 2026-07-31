# Decision Ledger

**Baseline authorization:** On 2026-07-30 the author instructed the build to
proceed using Build Plan v2 and the phenomenon-first course-book skill. The
plan's recommendations are therefore the working defaults below. A later
author correction supersedes any default.

1. **D01 — Title and subtitle:** Title fixed as *Deep Learning: Making It
   Trainable* with the cover subtitle *Geometry, Dynamics, and the Machine*.
   The DS 6210 affiliation belongs in the colophon, not the cover line.
2. **D02 — v1 scope:** Contract the C01–C17 core first. Keep Act III gated
   until the core budget is known.
3. **D03 — Candidate core arc:** Approved as a contract map, not empty chapter
   stubs.
4. **D04 — Convex baseline depth:** Use a short bridge in C04 plus sibling
   pointers, not a separate mechanics chapter.
5. **D05 — Precision/roofline split:** Sibling Appendix C owns introductory
   mechanics; this volume owns error theory, instrumentation, diagnosis, and
   hardware evidence.
6. **D06 — Public thread count:** Four public threads. Keep memory/retained
   state and orthogonality/scale internal for now.
7. **D07 — Exercise taxonomy:** Exactly Pencil, Code, and Audit. Profile and
   Paper audit are subtypes.
8. **D08 — Debranding strictness:** Use context-aware rules, golden allowed
   and violation fixtures, and sanctioned bridges/metadata.
9. **D09 — Generic model phrase:** Use “deep compositional structure” only
   where composition matters; otherwise use “parameterized model.”
10. **D10 — Pilot:** C02, streaming state and stable variance.
11. **D11 — Harness pin:** Annotated tag plus content-addressed vendored wheel
    and chapter manifest; no live Git dependency.
12. **D12 — Harness audience:** Live-course template repository; the book
    documents the pin without turning package management into content.
13. **D13 — Proof budget:** Mixed act-level policy; full proofs for reusable
    diagnostic machinery.
14. **D14 — Edition budget:** Infer the full budget from the pilot. C02 retains
    its provisional 6,500-word/22-page cap.
15. **D15 — Hardware endpoints:** Every chapter keeps a laptop witness. Use
    cluster artifacts only when scale is scientifically necessary.
16. **D16 — Student work:** Private editorial evidence by default; public reuse
    needs written permission and attribution.
17. **D17 — License:** CC BY-NC-SA 4.0 text/figures and MIT code, subject to
    provenance conflicts.
18. **D18 — Release model:** Rolling HTML and fixed tagged source/PDF releases;
    v0.x drafts and later v1.0.
19. **D19 — Rosetta placement:** Main appendix plus generated high-value term
    redirects.
20. **D20 — Source designation:** Treat the simple Spring 2026 syllabus as the
    current core contract and the longer syllabus as synthesis evidence unless
    the author says otherwise.
21. **D21 — Harness genesis:** Book-first, informed by Spring 2026 notebooks.
    Reopen only if extant course-wide lab code is supplied before the pilot pin.
22. **D22 — Notation covenant:** Approved at
    `contracts/notation-covenant.yml`; inherit and extend without redefinition.
23. **D23 — Sibling reciprocity:** Approved in principle. The sibling anchor
    contract requires explicit sibling-repository write authority; back
    references wait for opt-book v0.2 anchors.
24. **D24 — Accessibility:** Attempt tagged PDF and replacement text from the
    first build. The first attempt did not produce a valid tagged structure,
    so untagged PDF is the explicit v0.x fallback. Validated tagging and
    replacement text are a pre-v1.0 release gate, not an indefinite backlog.
25. **D25 — Unit numbering:** The introduction is unnumbered front matter.
    C01–C17 exclusively own chapter numbers 1–17; an unwritten unit is
    reserved by an explicit chapter offset, never by a public placeholder.
26. **D26 — Lens ledger:** Show one compact three-lens line below the public
    thread sigil. Keep the richer rationale in chapter metadata and contracts.
27. **D27 — Theorem ledger:** Keep theorem statements light on the page.
    Record the full seven-field theorem ledger in the chapter contract and
    expose only fields that help the reader at the point of use.
28. **D28 — C02 handoff:** Register both promises to C03: separate arithmetic
    cancellation from input-representation loss, and make the precision
    contract quantitative.
29. **D29 — Tutorial integration:** Treat both ICML 2026 tutorials as
    external routing sources. Credit their intellectual maps, route
    load-bearing claims to primary papers, and claim only the book's
    phenomenon-first integration as original pedagogy.
30. **D30 — Gradient/noise status:** Keep gradient-dominated versus
    noise-dominated behavior as an internal diagnostic ledger centered on
    C13, not a fifth public thread sigil.
31. **D31 — Probabilistic Numerics status:** Use acquired information and
    computational uncertainty as a light internal seam from C02/C03 to C12.
    Do not call Welford Bayesian conditioning or equate a numerical error with
    a calibrated posterior without an explicit probabilistic model.
32. **D32 — Paper Autopsy Protocol:** Extend the Spring 2026 optimizer card
    with evidence culture, theory resolution, dynamic regime, assumption
    stress, and transfer verdict. Chapter exercises use selected fields; C17
    uses the full card.
33. **D33 — Branch budget:** PL, acceleration variants, glocal implicit bias,
    WSD, Adam-surrogate details, and Probabilistic Numerics examples remain
    exercises, field notes, or further reading unless one becomes necessary
    to resolve a chapter's opening phenomenon.
34. **D34 — Harness publication tags (pending author decision):** Recommended
    forward-only scheme: start annotated source tags with the first wheel
    actually built from a recorded commit/tag pair; do not backfill false
    source identities onto C02–C12. Keep SHA-256 as the identity of those
    eleven rolling-draft wheels.
35. **D35 — Published provenance register:** Consolidate repeated instructor-
    source notes into one unnumbered Provenance and Acknowledgements note.
    Chapter Sources remain bibliographic; local source audits retain the full
    accept/reject record.
36. **D36 — Check-yourself policy:** Pose questions everywhere. Worked answers
    belong in instructor material under D16, not inside the self-check box.
37. **D37 — Closing incident:** Close the core with an unnumbered Coda, not an
    Act III seed. The Coda must use the C01–C17 instruments to diagnose one
    pinned incident and complete the book's opening promise.
38. **D38 — Figure palette:** Use the UVA-centered navy, wine, green, orange,
    secondary-blue, and gray family recorded in `docs/STYLE-GUIDE.md`. A fast
    audit rejects unapproved manuscript hex values.

## Acceptance status

- D01–D28 remain the approved implementation baseline.
- D29–D33 are implemented provisional policies and await explicit author
  ratification; “proceed with revision” is not silently recorded as acceptance.
- D34 is open. No harness tags are created until the author chooses a scheme.
- D35–D38 are adopted working decisions for this revision. They can be
  superseded by an explicit author correction without changing D34 or chapter
  acceptance status.
