# Full complex Boolean Holant dichotomy in Lean

A Lean formalization of *A Full Complexity Dichotomy for Complex-Valued Boolean
Holant Problems* by Chenghua Liu, Boning Meng and Juqiu Wang,
[arXiv:2610.00081](https://arxiv.org/abs/2610.00081). The pinned manuscript is
the **STOC 2027 submission snapshot exported from Overleaf on 6 November 2026**,
including both the short paper and the embedded full paper. Its exact source
hash and historical arXiv provenance are recorded in
[manuscript/provenance.json](manuscript/provenance.json).

The public main theorem classifies the ordinary and native-X Holant problems
for every valid finite language of algebraic signature tables. It includes
actual effective recognizers, polynomial-time evaluation in the tractable
cases and polynomial-time Turing reductions establishing hardness otherwise.
The theorem requires no unary resource, assumed classification provider or
supplied recognition machine.

[![Lean checks](https://github.com/liuchliuch/holant-dichotomy-lean/actions/workflows/verify.yml/badge.svg)](https://github.com/liuchliuch/holant-dichotomy-lean/actions/workflows/verify.yml)

## Build

Install [Elan](https://github.com/leanprover/elan), then run from the repository
root:

```sh
lake exe cache get
bash scripts/build.sh
```

The toolchain is pinned to Lean **4.34.1** and mathlib to revision
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The manifest pins the remaining Lean
dependencies. The needed Paper 1 sources are included under `Holant/`; no
separate local Paper 1 checkout is required.

The build script limits concurrent Lean processes to two by default. On a
machine with less memory, use `PAPER2_BUILD_THREADS=1 bash scripts/build.sh`.
The repository contains a large proof development, so the first source build
can take substantial time and memory even with the mathlib cache available.

## Use the theorems

```lean
import Paper2

#check Paper2.STOC2027.full_dichotomy
#check Paper2.STOC2027.mountain_dichotomy
#check Paper2.STOC2027.native_dichotomy
#check Paper2.STOC2027.mountain_construction
#check Paper2.STOC2027.eo_output_hardness
#check Paper2.STOC2027.endpoint_normalization
#check Paper2.SourceFaithful.SourceStatements.OddDihedralSixPort.source_A_1
```

These entry points match short Theorem 1.1 / full Theorem F.1.1, full
Theorems F.10.1 and F.10.3, short Lemmas 3.1 and 5.1, and full Lemma F.9.11,
respectively. Earlier numbered API names remain available for compatibility;
their numbers refer to the historical arXiv v1 manuscript.

The main result covers the original graph semantics, including zero, nullary,
repeated and mixed-arity signatures. Complexity bounds fix the signature
language before varying the graph. Recognition is effective as the language
varies; no polynomial-time bound for that varying-language recognition problem
is asserted. The separate mountain theorem retains its printed even-arity,
membership and high-height divisibility assumptions.

## Read and check the statements

- [Manuscript](manuscript/paper.pdf) and its [TeX source](manuscript/paper.tex).
- [Statement guide](docs/STATEMENTS.md): the numbered source-to-Lean map and its
  exact scope qualifications and changes from the previous source.
- [Machine-readable ledger](docs/STATEMENT_LEDGER.json): all 94 numbered source
  environments, including 86 required proof/definition entries.
- [Verification guide](docs/VERIFICATION.md): independent statement comparison,
  proof checking and release validation.

The scope comprises **81 mathematical result occurrences and five definitions**;
the short paper repeats results proved in the full paper. Eight expository
remarks are indexed separately. Some source conclusions are covered by stronger
theorems or by several proved components, as recorded in the ledger. The checker
verifies the inventory directly against the current TeX, including full-paper
and appendix prefixes, source lines, titles, labels and referenced labels.

The three main statements are also separated into a trusted
[challenge](Verification/Challenge.lean) and a proved
[solution](Verification/Solution.lean). The
[Lean comparator](https://github.com/leanprover/comparator) checks the solution
against the challenge, including dependent definitions. To compare local
trusted sources on macOS:

```sh
python3 scripts/comparator.py --trusted-local
```

Trusted-local comparison replays proofs through the Lean kernel without an OS
sandbox. GitHub Actions runs the official Comparator in a Linux sandbox and retains
verification reports as downloadable artifacts. See the verification guide
for the checks and their scope. The challenge has three intentional proof
placeholders and is never imported by the proof library or solution.

## Layout

| Path | Contents |
| --- | --- |
| `Paper2.lean`, `Paper2/` | Public interface and its proof dependencies |
| `Holant/` | Bundled Paper 1 proof dependencies |
| `Verification/` | Independent statement challenge, solution and comparison configuration |
| `manuscript/` | Pinned manuscript, source and provenance |
| `docs/` | Statement correspondence and verification documentation |
| `scripts/` | Build and verification commands |

## License

The Lean code and repository tooling are licensed under
[Apache-2.0](LICENSE). The manuscript remains under its authors' copyright;
see [manuscript/LICENSE](manuscript/LICENSE). Third-party Lean dependencies
retain their own licenses.
