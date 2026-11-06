# Manuscript

**A Full Complexity Dichotomy for Complex-Valued Boolean Holant Problems**  
Chenghua Liu, Boning Meng, and Juqiu Wang.

This directory pins the STOC 2027 submission source exported from the authors'
[Overleaf project](https://www.overleaf.com/project/6ad8d34ce8b959257628193d)
on **6 November 2026 at 14:23 UTC**. It contains the short paper, shared
bibliography, full paper, and TikZ figure in one self-contained source file.
The associated preprint is [arXiv:2610.00081](https://arxiv.org/abs/2610.00081).

- `paper.tex` is the byte-for-byte exported `stoc2027-HOL.tex`, renamed for the
  repository's stable manuscript path. Its SHA-256 is
  `0cbcd66f3790e5a74fed14fb51294385cda202acedea4c169d093c4492289e93`.
- `paper.pdf` is the 98-page local rendering of that exact source.
- `provenance.json` records the export time, source archive and file hashes,
  build and visual-review results, and the historical arXiv v1 provenance.

The current main statements are short-paper Theorem 1.1 and full-paper
Theorems F.1.1, F.10.1, and F.10.3. Full-paper numbers carry the `F.` prefix;
page numbering restarts at `F-1` after the shared references. Statement maps
must distinguish the short paper from the full paper.

The previous arXiv v1 source, 83-page PDF, and separate bibliography remain
available in Git history. They are not the current audited snapshot. The
external bibliography is no longer needed because this source embeds it.

The manuscript files retain their authors' copyright and are excluded from
the repository's Apache-2.0 code license; see [LICENSE](LICENSE).

## Rebuild

With TeX Live or MacTeX providing `latexmk` and pdfLaTeX, run from the
repository root:

```sh
mkdir -p .lake/manuscript-build
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=.lake/manuscript-build manuscript/paper.tex
```

The output is `.lake/manuscript-build/paper.pdf`; the matching `.aux` file
records all printed theorem numbers. No BibTeX run or additional source,
bibliography, or image file is required. The checked build used pdfTeX
1.40.26 from TeX Live 2024 and finished with no reference or box warnings.
PDF metadata can make rebuilt PDF bytes differ even when the source matches.

The manuscript's Code Availability section links to the authors'
[original exact-calculation repository](https://github.com/liuchliuch/Full-Holant-Dichotomy).
The Lean development in this repository supplies its own kernel-checked
proofs and does not require those external Python calculations to build.
