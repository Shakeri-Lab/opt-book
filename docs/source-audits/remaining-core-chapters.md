# Source audit — C01 and C13–C17

This audit records the source-to-chapter transformation used to complete the
approved C01–C17 core. Slides supplied phenomena and derivation order; prose,
claim boundaries, exercises, and proofs were written for the book. Tutorial
decks are routing sources, not technical authorities.

| Chapter | Instructor source (SHA-256) | Imported into the trunk | Shelved or narrowed |
|---|---|---|---|
| C01 | `meet2_alg_rooflin.tex` (`a0baeb3a03365016a75fad1bf4a4bc8578286cd16ec97f13c54ad7900ff811ba`) | memory hierarchy, arithmetic intensity, two-roof model | hardware slogans replaced by an explicit model/measurement boundary |
| C13 | `meet6_convexII.tex` (`58e96d99aeaed7ee06ab327b8c27386f1a22cbbeaec73b5749af22fd417014ed`) | conditional estimators, noise floor, schedules | optimizer survey, silver steps, and variance-reduction zoo remain branches |
| C14 | `meet13-initialization.tex` (`5a4c78672902ef12710ee807c953de9b30c0b3c89b661d34af0a1cb30156e973`) and handout (`a8ad56ade422f3d481f90483744f2d0e978c316d2a16f5e11ee725fc58b58919`) | variance recursion, depth products, dynamical-isometry question | generic FP16-depth and finite-width kernel claims rejected; scalar criticality is not called trainability |
| C15 | `WW11.tex` (`c36cb989d88fd3ac4ceaae68b11985abeb49a8ba1a98f0588d36f8b307850f6e`) and `2.10-Normalization.tex` (`672cbba5edae627994647911f8861e239ac29c35155fec79e02ebbc68ef9fb43`) | invariance geometry, centered arithmetic, residual placement | “landscape smoothing” retained only as scoped paper evidence |
| C16 | `meet14-normalization.tex` (`40128881627a0c588331a050fd056f6a4fd7d521517bcb40027488b4f443992a`), handout (`5fbe922ffb0638c942b05679f802157b08f22cf0974af93a283241ef69671be0`), and `GD_Stability_Slides.tex` (`47717f2f715b764ec49ca0d99d5b0a8d452c805a61b89430b1a2d8b4a00794a8`) | fixed quadratic control, moving curvature, top/directional diagnostics | flat-minimum/generalization and universal large-step acceleration claims excluded |
| C17 | `meet12c-Muon-Journal-club.tex` (`79f354cafa222b43694f4123b0a556dd1a85904efc649c0ae361695ed6d21a1c`) and `meet12d-QJL-journal-club.tex` (`23373548336ad044b8af81a4fa1e50ea2a0f4ce15cfd9a7aa0cc320ed35a0b93`) | polar update geometry, iteration and routing questions, paper autopsy | external efficiency numbers and method-specific detail remain paper-audit branches |

## Primary-source routing

- C01: Williams, Waterman, and Patterson for the roofline model.
- C13: Bottou, Curtis, and Nocedal for stochastic-optimization assumptions;
  primary heavy-tail evidence for the boundary.
- C14: Schoenholz et al. for mean-field signal propagation and Pennington et
  al. for dynamical isometry.
- C15: original centered and RMS-only normalization papers; Santurkar et al.
  only for its scoped empirical geometry claim.
- C16: Cohen et al. for the edge-of-stability empirical phenomenon; the
  two-parameter witness is the book's independent diagnostic control.
- C17: Bernstein and Newhouse for matrix-norm steepest descent; the original
  Muon technical account and scalable implementation paper for method claims.

## Epistemic decisions

1. No CPU FP16 timing is presented as accelerator performance.
2. No tutorial equation is load-bearing without a derivation or primary
   source.
3. The C16 crown phenomenon is class (a), reproducible on a laptop; scale
   extensions may later be class (c).
4. QJL/TurboQuant, probabilistic numerics, optimizer anecdotes, and edge-of-
   stability staircase variants remain branches unless a future revision
   promotes a specific diagnostic need.
5. Act III remains gated by D02 and is not silently authored as part of the
   core completion.
