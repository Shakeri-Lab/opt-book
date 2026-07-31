# Source Audit — C12 Curvature Objects and Information Policies

## Review status

Completed 2026-07-31. Hennig (2015) and Hennig–Kiefel (2013) were read in
full as required by the Probabilistic Numerics intake gate. The curvature
definitions and limitations were cross-checked against Pearlmutter (1994),
Martens (2020), and Kunstner–Balles–Hennig (2019). Public technical claims cite
these primary papers; the ICML tutorials retain credit only for routing and
framing.

| Source | Reviewed artifact | SHA-256 | C12 use |
|---|---|---|---|
| Pearlmutter (1994) | author-hosted 13-page PDF | `18e381e20d4ea7c3858ead0cc9e390053ea858655c65085834d6628fc506f4cb` | exact directional derivative identity and no-materialization HVP |
| Martens (2020) | JMLR 76-page PDF | `b6ac7f19dbc3b8bb8a44708e7fac5cc8d2a270ee0f6468eca09f8796b55aaaf0` | Hessian/GGN decomposition, qualified GGN–model-Fisher equivalence, structured approximations |
| Kunstner, Balles, Hennig (2019) | NeurIPS 12-page PDF | `24794d33b6845c9dbe5802551949119d00565eb2e6a7607d8c29701ce796a8ca` | empirical Fisher is not generally a Monte Carlo estimate of the model Fisher |
| Hennig (2015) | arXiv v2, 25-page PDF | `0ab3db1c6bd8d15c456b532415aada8be0ca5b8415fca0c00ed52c9850fd7131` | SPD linear problem, exact-line-search BFGS/CG correspondence, prior and calibration boundaries |
| Hennig and Kiefel (2013) | JMLR 23-page PDF | `2e5832dca7e4b07b762592043c8242c0613638298dee1b4cae68dfa7d14fe481` | quasi-Newton updates as approximate Bayesian regression under chosen priors |

## Load-bearing qualifications

1. The generalized Gauss–Newton matrix is positive semidefinite only when the
   declared output loss is convex in the variable at which the model is split.
2. GGN equals the model Fisher for compatible likelihood/output
   parameterizations; the equality is qualified, not universal.
3. The empirical Fisher uses observed-label score outer products. It is not in
   general an empirical estimator of the model Fisher, which averages labels
   under the current predictive distribution.
4. Pearlmutter's operator identity avoids dense Hessian storage. “About the
   cost of a gradient” is an algebraic statement, not a hardware timing claim.
5. Hennig's CG correspondence assumes a symmetric positive-definite linear
   problem, exact line searches, and a specific Gaussian matrix prior. An
   algebraically identical point iterate does not establish posterior
   calibration.
6. Hennig–Kiefel show that named quasi-Newton means correspond to approximate
   Bayesian regression under varying prior/likelihood choices; they do not
   prove that arbitrary quasi-Newton state is calibrated curvature belief.

## Instructor-material adjudication

The canonical curvature slides correctly plant the squared-loss
Hessian/covariance bridge and HVP necessity. C12 rejects their broader claims
that a nonlinear trained Hessian generically follows a Marchenko–Pastur law,
that effective rank counts Hessian outliers, that low effective rank certifies
generalization, or that a fixed two-backward-pass factor is a hardware law.
