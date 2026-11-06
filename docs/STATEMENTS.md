# Manuscript statements

The [ledger](STATEMENT_LEDGER.json) maps all **94 numbered environments** in
the November 6, 2026 Overleaf source snapshot: three in the short paper and
91 in the embedded full paper. The proof scope contains **81 mathematical
results and five definitions**; eight explanatory remarks are indexed
separately. The source SHA-256 is
`0cbcd66f3790e5a74fed14fb51294385cda202acedea4c169d093c4492289e93`.
See [manuscript provenance](../manuscript/provenance.json) for the export and
artifact hashes.

The 86 required rows contain 199 declaration mappings and 173 distinct Lean
declarations. A row is a correspondence record, not a claim that every printed
environment has one identically worded Lean theorem. The ledger retains
`legacy_number` and `legacy_source` for reused arXiv-v1 rows. Those fields record
history; current numbers, source lines, labels, titles and references come from
the new snapshot. Full-paper numbers include `F.`; its appendix is `F.A.1` through
`F.A.9`. Unprefixed `1.1`, `3.1` and `5.1` refer only to the short paper.

## Reading the correspondence

- **Direct:** a source statement, or a closed proved interface realizing it.
- **Stronger:** a proved result whose conclusion covers the source claim under
  weaker assumptions, possibly by establishing one permitted disjunct.
- **Components:** the source claim is represented by proved constituent results
  or proved input records; the ledger states their exact scope.
- **Definition:** a concrete definition, with the displayed equivalences where
  applicable.

The table links one primary declaration for each required row. The ledger
contains every mapped declaration, exact source title, source label, referenced
label, file and scope qualification. Long citation annotations in source titles
are omitted from the table for readability, but retained verbatim in the ledger.
Historical numbers in Lean declaration names remain compatibility names;
they are not the current manuscript numbering.

## Current interfaces and scope

`Paper2.STOC2027.full_dichotomy` is the ordinary-coordinate statement of short
Theorem 1.1 and full Theorem F.1.1. It projects the ordinary recognizer,
evaluation and hardness clauses from the previously proved combined
classification. It applies to every valid finite language of algebraic tables,
without a unary, classification-provider or recognition-machine assumption.
Evaluation and hardness bounds fix the language before varying the graph.
Recognition over a varying input language is effective; no polynomial recognition
bound is asserted. The original graph semantics retain zero and nullary
signatures, repeated rows, mixed arities and tensor decompositions.

`Paper2.STOC2027.mountain_dichotomy` is Theorem F.10.1. All original signatures
have even arity, the specified mountain belongs to the language, and
whole-language half-charge divisibility is required at heights at least three.
`Paper2.STOC2027.native_dichotomy` is Theorem F.10.3 and includes an effective
native recognizer. Its criterion `Tract (kImage L)` is the literal new notation
`Tract(KF)`; the old `Tract_K` abbreviation denoted the same predicate.

The short paper removes zero and nullary signatures before its auxiliary
lemmas (source lines 491–493), as does the full paper (lines 2035–2043).
The new closed `mountain_construction` interface covers short Lemma 3.1 and
full Lemma F.5.2, including divisibility on the entire language after adjoining
the mountain. The new `eo_output_hardness` interface covers short Lemma 5.1 and
full Theorem F.4.13. Their lower-level reduction providers are instantiated
internally, and their conclusions use the strict public exact-output semantics.

For F.6.1, F.6.12, F.6.16, F.6.23, F.6.31 and F.6.32, the stronger unconditional
native dichotomy proves the permitted current-language terminal outcome.
The narrower height-one, irreducible-signature and stable-stage constructions
remain secondary mappings at their stated scopes. These rows do not assert
separate standalone proofs of every specified strict-successor, same-coordinate
closure or proper-factor alternative. The same distinction applies to F.6.29
and F.4.17. The F.4.19 entry combines the complexity conclusion with a
constructive root-of-unity anchor clause.

The F.4.2, F.4.6 and F.4.12 source interfaces include proved reduction programs
and output conversions internally. Generic lower-level lemmas may take named
input records, but their public instances use proved implementations. Appendix
F.A.2 is represented by support-level components; coefficient factorization is
not inferred solely from the support shape. Appendix F.A.3 now explicitly
documents the manuscript's dependence on external Z3 UNSAT answers. The existing
Lean coefficient-classification proof establishes the same arbitrary-complex
statement through the kernel and does not assume those answers.

## Changes from the arXiv-v1 correspondence

The new full paper separates preliminaries, the tractability criterion,
auxiliary reductions and mountain construction into Sections F.2–F.5. Height
one is Section F.6, height two F.7, height three F.8, height at least four F.9,
and synthesis F.10. The three principal old numbers `1.1`, `9.1` and `9.2`
therefore become `F.1.1`, `F.10.1` and `F.10.3`. The short paper restates the
main theorem and adds two summary lemmas with explicit source bridges.

The changes do not alter the seven tractability alternatives or the main
classification. The manuscript now calls tensor-prime signatures
“irreducible,” uses “variables” for ports, and writes `D(t) = diag(1,t)`
consistently. In Lemma F.9.11 the normalizing matrix is consequently written
`s D(s^(-2))`. `Paper2.STOC2027.endpoint_normalization` proves equality with
the earlier `diag(s,s^(-1))`, together with the literal tensor normalization
and exact preservation of the X edge; no projective scalar is discarded.

The height-one statements F.6.12, F.6.16 and F.6.23 replace repeated strict-update
conditions with a reference to Definition F.6.10. The finite descent and fixed
number-field conditions remain. Height two still follows from the eight-vertex
classification. Height three retains the loop and two-copy arrays. Heights at
least four retain normalization, common-phase recovery and reconstruction,
including the height-four Reed–Muller exception. The source has shortened some
numbered conclusions: F.9.8 stops at matching-product reconstruction and F.9.13
at Bell simulation; their former appended hardness consequences remain proved
in Lean. F.4.14 states its unary adjoin reduction explicitly instead of speaking
of membership in a retained enlarged set.

The following historical environments have no standalone numbered counterpart
in the new source. Their old ledger rows are not counted as current coverage;
useful underlying Lean declarations remain proof dependencies where needed.

| Historical number | Historical environment | Previous scope |
| --- | --- | --- |
| 2.10 | Effective algebraic transformability witnesses | Required lemma |
| 2.15 | Quaternary eight-vertex boundary | Required theorem |
| 2.16 | Even-degree counting CSP | Deferred external theorem |
| 2.17 | Degree-multiple counting CSP | Deferred external theorem |
| 3.11 | Scope of the literature inputs | Expository remark |
| 3.12 | Simultaneous transformation of the edge and signature | Expository remark |
| A.2 | Scope of the odd-dihedral certificate | Expository remark |
| A.5 | Scope of the six-port certificate | Expository remark |

There are no deferred numbered environments in the current ledger. Removing
the historical external CSP rows does not assert that their full classifications
have newly been proved here.

## Required statements

| Current number | Historical number | Source title | Correspondence | Primary Lean declaration |
| --- | --- | --- | --- | --- |
| [1.1](../manuscript/paper.tex#L460) | — | Full dichotomy | Direct | [`STOC2027.full_dichotomy`](../Paper2/STOC2027.lean) |
| [3.1](../manuscript/paper.tex#L596) | — | Mountain construction | Direct | [`STOC2027.mountain_construction`](../Paper2/STOC2027/SourceBridges.lean) |
| [5.1](../manuscript/paper.tex#L878) | — | An EO output in the ambient set | Direct | [`STOC2027.eo_output_hardness`](../Paper2/STOC2027/SourceBridges.lean) |
| [F.1.1](../manuscript/paper.tex#L1755) | 1.1 | Full dichotomy theorem | Direct | [`STOC2027.full_dichotomy`](../Paper2/STOC2027.lean) |
| [F.3.2](../manuscript/paper.tex#L2450) | 2.7 | Transformability | Definition | [`Tractable.CommonTransformable`](../Paper2/Tractable/CommonTransform.lean) |
| [F.3.3](../manuscript/paper.tex#L2535) | 2.8 | The predicate `EOTract` | Definition | [`Tractable.EOTract`](../Paper2/Tractable/Criteria.lean) |
| [F.3.5](../manuscript/paper.tex#L2648) | 2.18 | Recognition and evaluation | Direct | [`Paper1ProvedRecognition.uniform_recognition`](../Paper2/Paper1ProvedRecognition/Source.lean) |
| [F.4.1](../manuscript/paper.tex#L2679) | 2.11 | Weighted Eulerian orientations | Components | [`Paper1Proved.eoProvider`](../Paper2/Paper1ProvedEOProvider.lean) |
| [F.4.2](../manuscript/paper.tex#L2687) | 2.14 | Tensor-factor extraction | Direct | [`SourceFaithful.SourceStatements.FactorExtraction.source_2_14`](../Paper2/SourceFaithful/SourceStatements/FactorExtractionStatement.lean) |
| [F.4.3](../manuscript/paper.tex#L2719) | 2.19 | Factor closure | Components | [`exists_prime_decomposition`](../Paper2/PrimeFactorization.lean) |
| [F.4.4](../manuscript/paper.tex#L2758) | 2.20 | Preservation under taking subsets | Direct | [`Tractable.downward_inheritance`](../Paper2/Tractable/Downward.lean) |
| [F.4.5](../manuscript/paper.tex#L2768) | 2.21 | `GO(X)`-invariance of tractability | Direct | [`Tractable.goX_tract_invariance`](../Paper2/Tractable/Conformal.lean) |
| [F.4.6](../manuscript/paper.tex#L2794) | 3.1 | Binary interpolation | Direct | [`SourceFaithful.SourceStatements.BinaryInterpolation.source_3_1`](../Paper2/SourceFaithful/SourceStatements/BinaryInterpolationStatement.lean) |
| [F.4.7](../manuscript/paper.tex#L2819) | 2.13 | Odd-arity Holant | Components | [`Paper1Proved.OddResidue.oddProviderOfUnary`](../Paper2/Paper1ProvedOddResidueUnaryReduction.lean) |
| [F.4.8](../manuscript/paper.tex#L2852) | 3.2 | Reduction with at most one `Delta`-vertex | Components | [`Paper1Proved.universalPair`](../Paper2/Paper1ProvedUniversalPairProvider.lean) |
| [F.4.9](../manuscript/paper.tex#L2874) | 3.3 | Single-occurrence replication | Direct | [`SourceFaithful.SourceStatements.Replication.theorem_3_3_literal`](../Paper2/SourceFaithful/SourceStatements/ReplicationStatement.lean) |
| [F.4.10](../manuscript/paper.tex#L2965) | 3.4 | Dichotomy with a nonzero unary | Direct | [`Paper1Proved.OddUnary.UnaryProvider.native_classification`](../Paper2/Paper1ProvedOddUnaryComplete.lean) |
| [F.4.11](../manuscript/paper.tex#L2981) | 3.5 | Higher equality supplies unaries | Direct | [`SourceFaithful.SourceStatements.EqualityPins.corollary_3_5`](../Paper2/SourceFaithful/SourceStatements/EqualityPinsStatement.lean) |
| [F.4.12](../manuscript/paper.tex#L3047) | 3.6 | Replacing vertices by fixed gadgets in a larger signature set | Direct | [`SourceFaithful.SourceStatements.RelativeEOAmbient.source_3_6`](../Paper2/SourceFaithful/SourceStatements/RelativeEOAmbientStatement.lean) |
| [F.4.13](../manuscript/paper.tex#L3090) | 3.7 | Hardness from an EO signature outside `B_ARS` | Direct | [`STOC2027.eo_output_hardness`](../Paper2/STOC2027/SourceBridges.lean) |
| [F.4.14](../manuscript/paper.tex#L3105) | 3.8 | Quaternary EO CP signatures supply a unary | Components | [`SourceFaithful.RelativeEO.complementary_supplies_pins`](../Paper2/SourceFaithful/RelativeEO/WeightedComplementaryExit.lean) |
| [F.4.15](../manuscript/paper.tex#L3176) | 3.9 | Projective ARS or hardness | Stronger | [`SourceFaithful.RelativeEO.realized_isARSProduct`](../Paper2/SourceFaithful/RelativeEO/Terminal.lean) |
| [F.4.16](../manuscript/paper.tex#L3319) | 3.10 | Hardness outside `B_ARS` under projective ARS | Components | [`SourceFaithful.RelativeEO.ars_relative_terminal`](../Paper2/SourceFaithful/RelativeEO/ARSTerminal.lean) |
| [F.4.17](../manuscript/paper.tex#L3464) | 3.13 | Dichotomy from a transformed quaternary equality | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.4.18](../manuscript/paper.tex#L3485) | 3.14 | Dichotomy with a generalized equality | Stronger | [`SourceFaithful.generalized_equality_relative_terminal`](../Paper2/SourceFaithful/GeneralizedEqualityTerminal.lean) |
| [F.4.19](../manuscript/paper.tex#L3500) | 3.15 | Dichotomy from a CP factor in Walsh coordinates | Stronger | [`SourceFaithful.SourceStatements.TwoPointWalsh.source_3_15`](../Paper2/SourceFaithful/SourceStatements/TwoPointWalshStatement.lean) |
| [F.5.1](../manuscript/paper.tex#L3574) | 2.3 | Mountain | Definition | [`IsMountain`](../Paper2/Mountain.lean) |
| [F.5.2](../manuscript/paper.tex#L3593) | 4.1 | Producing the gcd-height signature or both pinning signatures | Direct | [`STOC2027.mountain_construction`](../Paper2/STOC2027/SourceBridges.lean) |
| [F.6.1](../manuscript/paper.tex#L3783) | 5.1 | Dichotomy with a height-one mountain | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.6.2](../manuscript/paper.tex#L3803) | 2.23 | Binary-equality `K`-Holant dichotomy | Direct | [`ExactInput.Recognition.literalEqualityDichotomyWithRecognition_2_23`](../Paper2/ExactInput/Recognition/NativeComplete.lean) |
| [F.6.5](../manuscript/paper.tex#L3894) | 5.3 | Bounded torsion | Direct | [`HeightOne.GroupSplit.provedBoundedTorsion`](../Paper2/HeightOne/GroupSplit/Paper1Proved.lean) |
| [F.6.6](../manuscript/paper.tex#L3923) | 2.1 | Finite projective binary groups | Direct | [`SourceFaithful.SourceStatements.FiniteGroups.proposition_2_1`](../Paper2/SourceFaithful/SourceStatements/FiniteGroupStatements.lean) |
| [F.6.7](../manuscript/paper.tex#L3941) | 2.2 | Finite projective-group facts | Direct | [`SourceFaithful.SourceStatements.FiniteGroups.lemma_2_2`](../Paper2/SourceFaithful/SourceStatements/FiniteGroupStatements.lean) |
| [F.6.8](../manuscript/paper.tex#L4003) | 5.4 | Weighted equality or an odd cyclic or dihedral group | Direct | [`SourceFaithful.SourceStatements.WeightedEqualityStage.theorem_5_4`](../Paper2/SourceFaithful/SourceStatements/WeightedEqualityStage.lean) |
| [F.6.9](../manuscript/paper.tex#L4218) | 2.22 | Invariants under adding signatures and changing basis | Direct | [`SourceFaithful.SourceStatements.NormalizationLedger.source_2_22_natural`](../Paper2/SourceFaithful/SourceStatements/NormalizationLedgerInfinite.lean) |
| [F.6.10](../manuscript/paper.tex#L4309) | 5.5 | Equivalent updates with strict progress | Definition | [`SourceFaithful.HeightOne.PrimeStage`](../Paper2/SourceFaithful/HeightOneProgress.lean) |
| [F.6.11](../manuscript/paper.tex#L4348) | 5.6 | Termination of the strict updates | Direct | [`HeightOne.GroupSplit.no_infinite_fixed_field_updates`](../Paper2/HeightOne/UniformBound/Progress.lean) |
| [F.6.12](../manuscript/paper.tex#L4445) | 5.8 | Finite recursive contraction and factor extraction | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.6.13](../manuscript/paper.tex#L4605) | 5.9 | Phase-pencil relation | Components | [`HeightOne.PhaseCards.provedPhasePencil`](../Paper2/HeightOne/PhaseCards/Paper1Pencil.lean) |
| [F.6.14](../manuscript/paper.tex#L4624) | 5.10 | Walsh parity from contractions | Direct | [`SourceFaithful.SourceStatements.TypeParityStatement.lemma_5_10`](../Paper2/SourceFaithful/SourceStatements/TypeParityStatement.lean) |
| [F.6.15](../manuscript/paper.tex#L4716) | 5.12 | Quaternary classification under phase contractions | Direct | [`SourceFaithful.SourceStatements.PhaseProductParity.source_5_12_literal`](../Paper2/SourceFaithful/SourceStatements/PhaseProductParityLiteralCyclic.lean) |
| [F.6.16](../manuscript/paper.tex#L4770) | 5.7 | The odd-dihedral case | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.6.17](../manuscript/paper.tex#L4849) | 5.11 | Closure of `P_N` under contractions | Direct | [`SourceFaithful.SourceStatements.source_5_11`](../Paper2/SourceFaithful/SourceStatements/PhaseProductContractionStatement.lean) |
| [F.6.18](../manuscript/paper.tex#L4922) | 5.13 | Dihedral quaternary classification | Direct | [`SourceFaithful.SourceStatements.PhaseProductParity.source_5_13_conditionC`](../Paper2/SourceFaithful/SourceStatements/PhaseProductParityFactorCondition.lean) |
| [F.6.19](../manuscript/paper.tex#L5023) | 5.14 | Arity-six factorization from contractions | Direct | [`SourceFaithful.SourceStatements.SixPortBinary.source_5_14`](../Paper2/SourceFaithful/SourceStatements/SixPortBinaryStatement.lean) |
| [F.6.20](../manuscript/paper.tex#L5107) | 5.15 | Three matching products on a line | Stronger | [`SourceFaithful.SourceStatements.source_5_15`](../Paper2/SourceFaithful/SourceStatements/ThreeMatchingLineStatement.lean) |
| [F.6.21](../manuscript/paper.tex#L5145) | 5.16 | Phase-independent matching and common factors | Stronger | [`SourceFaithful.SourceStatements.DihedralRuling.source_5_16`](../Paper2/SourceFaithful/SourceStatements/DihedralRulingStatement.lean) |
| [F.6.22](../manuscript/paper.tex#L5183) | 5.17 | A binary factor from contractions | Stronger | [`SourceFaithful.SourceStatements.DihedralRuling.source_5_17`](../Paper2/SourceFaithful/SourceStatements/DihedralRulingStatement.lean) |
| [F.6.23](../manuscript/paper.tex#L5298) | 5.18 | The odd-cyclic case | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.6.24](../manuscript/paper.tex#L5376) | 5.19 | Phase-independent matching | Components | [`SourceFaithful.SourceStatements.CyclicCardFactorBridge.root_card_data`](../Paper2/SourceFaithful/SourceStatements/CyclicCardFactorBridge.lean) |
| [F.6.25](../manuscript/paper.tex#L5441) | 5.20 | Every variable pair has a nonzero phase contraction above arity four | Stronger | [`SourceFaithful.SourceStatements.CyclicCardFactorBridge.root_card_data`](../Paper2/SourceFaithful/SourceStatements/CyclicCardFactorBridge.lean) |
| [F.6.26](../manuscript/paper.tex#L5502) | 5.21 | Rank-one diagonal restrictions | Components | [`HeightOne.PhaseCards.provedDiagonalSlices`](../Paper2/HeightOne/PhaseCards/Paper1Diagonal.lean) |
| [F.6.27](../manuscript/paper.tex#L5525) | 5.22 | The minimum nonbinary arity is four in the cyclic case | Stronger | [`SourceFaithful.SourceStatements.CyclicMinimumStatement.source_5_22`](../Paper2/SourceFaithful/SourceStatements/CyclicMinimumStatement.lean) |
| [F.6.28](../manuscript/paper.tex#L5654) | 2.24 | Irreducible quaternary `K`-Holant dichotomy | Direct | [`ExactInput.Recognition.primeQuaternaryDichotomyWithRecognition_2_24`](../Paper2/ExactInput/Recognition/NativeComplete.lean) |
| [F.6.29](../manuscript/paper.tex#L5666) | 2.25 | Eight-vertex `K`-Holant dichotomy | Stronger | [`PublicDichotomy.theorem_9_2`](../Paper2/PublicNativeClassification.lean) |
| [F.6.30](../manuscript/paper.tex#L5708) | 5.23 | Attaching cyclic binary representatives to four variables | Direct | [`SourceFaithful.SourceStatements.CyclicDressing.source_5_23`](../Paper2/SourceFaithful/SourceStatements/CyclicDressingStatement.lean) |
| [F.6.31](../manuscript/paper.tex#L5751) | 5.24 | The quaternary odd-cyclic case | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.6.32](../manuscript/paper.tex#L5952) | 5.25 | Hardness, tractability, or a strict update | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [F.7.1](../manuscript/paper.tex#L6064) | 6.1 | Dichotomy with a height-two mountain | Components | [`SourceFaithful.HeightTwo.mountain_classification`](../Paper2/SourceFaithful/HeightTwo.lean) |
| [F.8.1](../manuscript/paper.tex#L6086) | 7.1 | Height-three mountain dichotomy | Components | [`SourceFaithful.HeightThree.theorem_7_1`](../Paper2/SourceFaithful/HeightThree/Complete.lean) |
| [F.8.2](../manuscript/paper.tex#L6139) | 7.2 | A matching-product central restriction yields a quaternary signature | Direct | [`TransversalCube.exists_native_gadget_WT18a`](../Paper2/TransversalCube.lean) |
| [F.8.3](../manuscript/paper.tex#L6232) | 7.3 | Loop and two-copy contractions of an arity-six mountain | Definition | [`HeightThree.loopSignature_array`](../Paper2/HeightThree/LoopGeometry.lean) |
| [F.8.4](../manuscript/paper.tex#L6289) | 7.4 | Support forced by arity-six contractions | Direct | [`Certificates.Q6.joint_deck_support`](../Paper2/Certificates/Q6JointDeck.lean) |
| [F.8.5](../manuscript/paper.tex#L6311) | 7.5 | A quaternary EO output outside `B_x` from an arity-six mountain | Direct | [`HeightThree.nonmatching_mountain`](../Paper2/HeightThree/NonMatching.lean) |
| [F.9.1](../manuscript/paper.tex#L6377) | 8.1 | Mountain dichotomy at every height at least four | Components | [`SourceFaithful.HighHeight.classification_ge_four`](../Paper2/SourceFaithful/HighHeightCompleteTerminal.lean) |
| [F.9.3](../manuscript/paper.tex#L6481) | 8.3 | Vanishing pair contractions | Direct | [`CommonPhase.vanishing_pair_contractions_weight`](../Paper2/CommonPhase/ZeroLoops.lean) |
| [F.9.4](../manuscript/paper.tex#L6498) | 8.4 | Propagation of `X`-matching products | Direct | [`MatchingPropagation.x_line_propagation_source`](../Paper2/MatchingPropagation.lean) |
| [F.9.5](../manuscript/paper.tex#L6583) | 8.5 | Normalization by binary attachments at every arity at least eight | Components | [`SourceFaithful.HighHeight.finite_port_normalization`](../Paper2/SourceFaithful/HighHeightCompleteNormalization.lean) |
| [F.9.6](../manuscript/paper.tex#L6667) | 8.6 | A common phase for EO contractions | Stronger | [`CommonPhase.common_phase_algebraic`](../Paper2/CommonPhase.lean) |
| [F.9.7](../manuscript/paper.tex#L6708) | 8.7 | Shao--Cai matching-product reconstruction | Stronger | [`HighHeightReconstruction.reconstruct_ge_ten`](../Paper2/HighHeightReconstruction/Source.lean) |
| [F.9.8](../manuscript/paper.tex#L6753) | 8.8 | A shared edge forces a matching product | Direct | [`Certificates.Q8.Atlas.matching_deck_of_collision`](../Paper2/Certificates/Q8AlgebraicReconstruction.lean) |
| [F.9.9](../manuscript/paper.tex#L6779) | 8.9 | Translation form of the matching family | Components | [`Certificates.Q8.Atlas.collision_free_translation`](../Paper2/Certificates/Q8AtlasUnnormalized.lean) |
| [F.9.10](../manuscript/paper.tex#L6871) | 8.10 | The matching family determines the Reed--Muller central restriction | Direct | [`Certificates.Q8.Atlas.collision_free_deck_reedMuller_algebraic`](../Paper2/Certificates/Q8AlgebraicReconstruction.lean) |
| [F.9.11](../manuscript/paper.tex#L6955) | 8.11 | Normalizing the endpoint coefficients | Direct | [`STOC2027.endpoint_normalization`](../Paper2/STOC2027/SourceBridges.lean) |
| [F.9.13](../manuscript/paper.tex#L7057) | 8.12 | The Reed--Muller Bell reduction | Direct | [`SourceFaithful.BellTerminal.bell_reduction`](../Paper2/SourceFaithful/BellTerminal.lean) |
| [F.10.1](../manuscript/paper.tex#L7230) | 9.1 | Dichotomy for sets containing a mountain | Direct | [`STOC2027.mountain_dichotomy`](../Paper2/STOC2027.lean) |
| [F.10.2](../manuscript/paper.tex#L7258) | 2.12 | Single-layer K-Holant | Components | [`Paper1Proved.singleWeightHard`](../Paper2/Paper1ProvedSingleWeightProvider.lean) |
| [F.10.3](../manuscript/paper.tex#L7271) | 9.2 | Structural classification in `K`-coordinates | Direct | [`STOC2027.native_dichotomy`](../Paper2/STOC2027.lean) |
| [F.A.1](../manuscript/paper.tex#L7509) | A.1 | Order-three odd-dihedral arity-six classification | Direct | [`SourceFaithful.SourceStatements.OddDihedralSixPort.source_A_1`](../Paper2/SourceFaithful/SourceStatements/OddDihedralSixPortStatement.lean) |
| [F.A.2](../manuscript/paper.tex#L7718) | A.3 | Arity-six support classification | Components | [`HeightOne.Dihedral.SixPortPencils.three_phase_union_card_le_four`](../Paper2/HeightOne/Dihedral/SixPortPencils.lean) |
| [F.A.3](../manuscript/paper.tex#L7807) | A.4 | Height-three coefficient classification | Direct | [`Certificates.Q6.joint_deck_support`](../Paper2/Certificates/Q6JointDeck.lean) |
| [F.A.4](../manuscript/paper.tex#L7883) | A.6 | Consequence for loop and two-copy arrays | Direct | [`Certificates.Q6.joint_deck_support`](../Paper2/Certificates/Q6JointDeck.lean) |
| [F.A.6](../manuscript/paper.tex#L7937) | A.8 | Arity-eight matching classification | Direct | [`Certificates.Q8.Atlas.normalizedAtlasEquiv`](../Paper2/Certificates/Q8AtlasClassification.lean) |
| [F.A.7](../manuscript/paper.tex#L7985) | A.9 | Translation form of the matching family | Direct | [`Certificates.Q8.Atlas.collision_free_translation`](../Paper2/Certificates/Q8AtlasUnnormalized.lean) |
| [F.A.8](../manuscript/paper.tex#L8013) | A.10 | Coefficients on affine planes | Direct | [`SourceFaithful.SourceStatements.AppendixSupport.source_A_10`](../Paper2/SourceFaithful/SourceStatements/AppendixSupportStatement.lean) |
| [F.A.9](../manuscript/paper.tex#L8108) | A.11 | Affine-plane coefficients | Direct | [`SourceFaithful.SourceStatements.AppendixSupport.source_A_11`](../Paper2/SourceFaithful/SourceStatements/AppendixSupportStatement.lean) |

## Expository remarks

These are source-index entries, not independent Lean propositions.

| Current number | Historical number | Source title |
| --- | --- | --- |
| [F.3.1](../manuscript/paper.tex#L2392) | 2.4 | Notation relative to prior work |
| [F.3.4](../manuscript/paper.tex#L2627) | 2.9 | (Untitled remark) |
| [F.5.3](../manuscript/paper.tex#L3745) | 4.2 | (Untitled remark) |
| [F.6.3](../manuscript/paper.tex#L3863) | 2.5 | Bell notation in Shao--Cai |
| [F.6.4](../manuscript/paper.tex#L3882) | 5.2 | Relation to binary-signature classifications |
| [F.9.2](../manuscript/paper.tex#L6411) | 8.2 | Relation to the real-valued Holant argument |
| [F.9.12](../manuscript/paper.tex#L7037) | 2.6 | The Reed--Muller signature in Shao--Cai |
| [F.A.5](../manuscript/paper.tex#L7903) | A.7 | Why the two-copy arity-six arrays are necessary |

## Independent statement comparison

[Verification](VERIFICATION.md) describes the separate statement challenge and
solution for short Theorem 1.1 / full Theorem F.1.1, Theorem F.10.1 and Theorem
F.10.3. The comparator checks formal types and dependent definitions; the source
ledger supports the separate human review of their mathematical interpretation.
Release checks regenerate the source inventory, inspect all mapped declaration
types and axioms, and require fresh build and comparison evidence. Historical
arXiv-v1 verification results do not certify this snapshot.
