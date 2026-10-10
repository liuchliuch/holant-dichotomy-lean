# Verification

This repository separates three checks: Lean proof checking, comparison with
independently stated formal specifications, and correspondence with the
manuscript. Each checks a different part of the formalization.

## Build the proof library

From the repository root:

```sh
lake exe cache get
bash scripts/build.sh
```

The toolchain and dependency revisions are pinned. The build uses the bundled
Paper 1 dependency sources and the public `Paper2` entry point. It also builds
the challenge and solution modules separately. The mathematical proof library
does not import the challenge's intentionally unproved specification lemmas.

Successful compilation establishes that the Lean kernel accepts the declared
proofs. The printed axiom dependencies of the public results are restricted to
`propext`, `Classical.choice` and `Quot.sound`. The development includes
nonfatal unused-variable, tactic-style and deprecation warnings; a successful
build is not a claim that every dependency is warning-free.

After the build, check the source inventory and every mapped declaration:

```sh
python3 scripts/check.py
```

The checker performs static source and ledger checks, asks Lake to rehash and
validate the existing build without rebuilding, then compiles one generated
Lean probe that checks the exported declaration types and axiom dependencies.
Use `python3 scripts/check.py --static-only` for source checks before a build.
Generated probe files and diagnostics remain under `.lake/verification/`.

## Compare statements independently

[Verification/Challenge.lean](../Verification/Challenge.lean) states the three
main theorem specifications: manuscript Theorems 1.1, 9.1 and 9.2.
[Verification/Solution.lean](../Verification/Solution.lean) gives proofs with
the same declaration names using the public theorems. Their separate modules
allow the specifications to be inspected without reading the proof bodies.

The challenge contains exactly three intentional `sorry` placeholders. They
stand for the proofs demanded by the specification. They are confined to the
challenge; the solution and its proof dependencies must supply actual proofs.

The [Lean comparator](https://github.com/leanprover/comparator) compares the
solution against the challenge, recursively checking dependent definitions
and replaying the solution proof through the kernel. Its role goes beyond a
comparison of printed declaration names or formatted type strings. The tool
and comparison configuration are pinned in
[Verification/tools.json](../Verification/tools.json) and
[Verification/comparator.json](../Verification/comparator.json).

On Linux, the default sandboxed execution requires an unprivileged user,
Landlock ABI 6 or later, no effective capabilities, and a working systemd user
session and bus. A distribution name alone does not establish those conditions.
Run:

```sh
python3 scripts/comparator.py
```

For trusted local sources on macOS, use:

```sh
python3 scripts/comparator.py --trusted-local
```

To exercise the rejection tests as well, append `--negative-test`. These tests
check that a changed conclusion, an added premise and an extra axiom are
rejected. Trusted-local mode is intended for source you already trust. It
replays the proof through the Lean kernel without an OS sandbox. Linux CI checks
the secure mode and rejection controls in a separate job,
using the verified build from the same workflow run.

Comparison establishes agreement between the formal challenge and the proved
solution. Whether that challenge captures the intended mathematics is a
separate source-review question. The comparison covers these three main
statements; it does not claim an independently written challenge for every
numbered auxiliary result.

## Check source correspondence

[STATEMENTS.md](STATEMENTS.md) gives the human-readable index;
[STATEMENT_LEDGER.json](STATEMENT_LEDGER.json) records all 99 numbered
manuscript environments and every mapped declaration. Its `scope` field
distinguishes the 85 required entries from twelve expository remarks and the
two deferred external CSP references.

The ledger preserves exact source numbering, titles, LaTeX labels, references
and source locations. It distinguishes direct statements, stronger results
and proved component chains. In particular, a stronger theorem may establish
one allowed terminal outcome of a printed disjunction without separately
providing every alternative construction. The mapping notes record those
limits.

Reviewing a correspondence means checking the actual Lean hypotheses,
quantifier order, definitions and conclusion against the manuscript. Shared
basis matrices, ordered ports, scalar factors, zero/nullary cases, finite
languages and computational encoding conventions are part of that comparison.
The manuscript is the pinned arXiv v1 source; its provenance is recorded with
the manuscript files.

## Continuous integration

GitHub Actions builds all retained project sources on Ubuntu 24.04 using four
build workers, then checks the 179 mapped and public Comparator declarations.
A separate job runs the pinned official Comparator and all three rejection
controls. It verifies the source commit and SHA-256 hashes of the shared build
before using it. The complete build starts without project compilation products;
only pinned third-party dependency caches are reused.

The standard public runner has 16 GB RAM. The workflow adds up to 32 GiB swap,
subject to available disk space. These are execution settings, not minimum
hardware requirements or measured peak memory usage.

Reports under `.lake/verification/ci/` record the commit, source fingerprint,
commands, exit codes and log hashes. Workflow artifacts contain the reports,
declaration audit and Comparator logs. Generated reports and build products
are excluded from the repository. The workflow badge links to actual run
results; successful compilation alone does not establish Comparator acceptance.

The build and declaration audit execute trusted repository sources. Comparator's
build and export subprocesses run under Landrun with the systemd AF_UNIX guard;
preflight checks verify filesystem and network restrictions. The shared project
objects come from this workflow's clean build. This reproduces verification of
this repository and is not a service for arbitrary untrusted submissions.
Comparator replays the proof dependencies of the three specified theorems using
the default Lean kernel. No additional external kernel is enabled.
