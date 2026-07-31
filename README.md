# Deep Learning: Making It Trainable

*Geometry, Dynamics, and the Machine*

Course book for DS 6210 — Computation II: Numerical Analysis & Optimization
(Algorithms for Deep Learning), School of Data Science, University of
Virginia.

The HTML edition is canonical; PDF is derived.

## Local build

```bash
export OPT_BOOK_ENV=/absolute/path/outside/Box/opt-book/.venv
UV_PROJECT_ENVIRONMENT="$OPT_BOOK_ENV" uv sync
QUARTO_PYTHON="$OPT_BOOK_ENV/bin/python" quarto render
```

Run fast audits:

```bash
"$OPT_BOOK_ENV/bin/python" scripts/run_fast_audits.py
```

Project conventions and current state live in `docs/`.
