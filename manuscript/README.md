# Manuscript

**A Full Complexity Dichotomy for Complex-Valued Boolean Holant Problems**  
Chenghua Liu, Boning Meng, and Juqiu Wang.

This directory preserves the manuscript used for the Lean statement audit:
[arXiv:2610.00081v1](https://arxiv.org/abs/2610.00081v1).

- `paper.pdf` is the unmodified official 83-page PDF.
- `paper.tex` is the unmodified TeX source, renamed from
  `paper2-full-holant-dichotomy.tex` for convenience.
- `paper2-full-holant-dichotomy.bib` is the original bibliography; its name
  is retained because the TeX source refers to it directly.
- `provenance.json` records the official source URLs and SHA-256 hashes.

The PDF, TeX source, and bibliography retain their authors' copyright.
They are excluded from the repository's Apache-2.0 code license; see
[LICENSE](LICENSE).

## Rebuild

With a full TeX Live or MacTeX installation providing `latexmk`, pdfLaTeX,
and BibTeX, run from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```

This produces a local PDF from the unchanged source. The distributed PDF
is the official arXiv rendering and is preserved byte for byte, so a local
build need not have an identical PDF hash. All diagrams are written in
TikZ; no separate image assets are required.

The manuscript's Code Availability section links to the authors'
[original exact-calculation repository](https://github.com/liuchliuch/Full-Holant-Dichotomy).
The Lean development in this repository supplies its own kernel-checked
proofs and does not require those external Python calculations to build.
