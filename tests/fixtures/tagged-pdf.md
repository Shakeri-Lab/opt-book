# Tagged-PDF first-build fixture

Toolchain observed on 2026-07-30:

- Quarto 1.10.18
- LuaHBTeX 1.24.0 from Quarto's managed TeX path
- `tagpdf` installed during the attempted render

Attempt:

```tex
\usepackage{tagpdf}
\tagpdfsetup{activate-all,interwordspace=true}
```

Observed blocking error:

```text
Package tagpdf Error: PDF resource management is not active!
(tagpdf) tagpdf will not work.
```

Cause: the PDF management activation needed by the current tagging path must
occur before `\documentclass`; Quarto's ordinary `include-in-header` content
arrives after it.

Acceptance for a future repair:

1. activate PDF management in a version-pinned template before the document
   class;
2. render the complete book;
3. validate the structure tree with a dedicated PDF accessibility validator;
4. manually inspect reading order for title page, chapter text, callouts,
   equations, tables, code, figures, and references;
5. retain clean extraction and correct nonvisual alternatives;
6. do not claim PDF/UA until every applicable check passes.
