# Manuscript statements

The [ledger](STATEMENT_LEDGER.json) maps all 99 numbered environments in the
[pinned manuscript](../manuscript/paper.tex) to Lean declarations. The proof scope
contains **80 mathematical results and five definitions**. Twelve explanatory
remarks are indexed separately; the two external CSP classifications 2.16 and
2.17 are deferred and are not dependencies of the public main proof.

The 85 required rows contain 196 declaration mappings, with 176 distinct Lean
declarations. Several declarations contribute to more than one source result.
A row is a correspondence record, not a claim that every printed environment
has one identically worded Lean theorem.

## Reading the correspondence

- **Direct:** a source statement, or a closed proved interface realizing it.
- **Stronger:** a proved result whose conclusion covers the source claim under
  weaker assumptions, possibly by establishing one permitted disjunct.
- **Components:** the source claim is represented by proved constituent results
  or proved input records; the ledger states their exact scope.
- **Definition:** a concrete definition, with the displayed equivalences where
  applicable.

The table links one primary declaration for each required row. The ledger
contains every mapped declaration, source label, referenced label, file and
scope qualification. The numbered links open the corresponding manuscript
source line.

## Scope that affects interpretation

Theorem 1.1 provides ordinary and native-X dichotomies and effective recognizers
for every valid finite language of algebraic signature tables. It has no unary,
classification-provider or recognition-machine assumption. Evaluation and
hardness bounds fix the language before varying the graph. Recognition over a
varying input language is effective; no polynomial recognition bound is asserted.
The original graph semantics retain zero and nullary signatures, repeated rows,
mixed arities and tensor decompositions.

Theorem 9.1 retains its source hypotheses: all original signatures have even
arity, the specified mountain belongs to the language, and whole-language
half-charge divisibility is required at heights at least three. Theorem 9.2
classifies the original native-X problem and includes effective recognition.

For 5.1, 5.7, 5.8, 5.18, 5.24 and 5.25, the stronger unconditional native
dichotomy proves the permitted current-language terminal outcome. The narrower
height-one, prime-signature and stable-stage constructions remain secondary
mappings at their stated scopes. These rows do not assert separate standalone
proofs of every specified strict-successor, same-coordinate saturation or
proper-factor alternative. The same distinction between a stronger complexity
conclusion and a separate structural component applies to 2.25 and 3.13.
The 3.15 entry combines that complexity conclusion with a constructive
root-of-unity anchor clause.

The 2.14, 3.1 and 3.6 source interfaces include the proved reduction programs
and output conversions internally. Generic lower-level lemmas may take named
input records, but their public instances use proved implementations. Appendix
A.3 is represented by support-level components; coefficient factorization is
not inferred solely from the support shape.

## Required statements

| Number | Source title | Correspondence | Primary Lean declaration |
| --- | --- | --- | --- |
| [1.1](../manuscript/paper.tex#L444) | Full dichotomy theorem | Direct | [`PublicDichotomy.main_theorem_with_native_recognition`](../Paper2/PublicNativeClassification.lean) |
| [2.1](../manuscript/paper.tex#L1003) | Finite projective binary groups | Direct | [`FiniteGroups.proposition_2_1`](../Paper2/SourceFaithful/SourceStatements/FiniteGroupStatements.lean) |
| [2.2](../manuscript/paper.tex#L1019) | Finite projective-group facts | Direct | [`FiniteGroups.lemma_2_2`](../Paper2/SourceFaithful/SourceStatements/FiniteGroupStatements.lean) |
| [2.3](../manuscript/paper.tex#L1290) | Mountain | Definition | [`Paper2.IsMountain`](../Paper2/Mountain.lean) |
| [2.7](../manuscript/paper.tex#L1478) | Common transformability and `K`-presentation | Definition | [`Tractable.CommonTransformable`](../Paper2/Tractable/CommonTransform.lean) |
| [2.8](../manuscript/paper.tex#L1539) | The predicate `EOTract` | Definition | [`Tractable.EOTract`](../Paper2/Tractable/Criteria.lean) |
| [2.10](../manuscript/paper.tex#L1625) | Effective algebraic transformability witnesses | Direct | [`AlgebraicWitness.theorem_2_10_descent`](../Paper2/SourceFaithful/SourceStatements/AlgebraicWitness.lean) |
| [2.11](../manuscript/paper.tex#L1648) | Weighted Eulerian orientations | Components | [`Paper1Proved.eoProvider`](../Paper2/Paper1ProvedEOProvider.lean) |
| [2.12](../manuscript/paper.tex#L1657) | Single-weight K-Holant | Components | [`Paper1Proved.singleWeightHard`](../Paper2/Paper1ProvedSingleWeightProvider.lean) |
| [2.13](../manuscript/paper.tex#L1668) | Odd-arity Holant | Components | [`OddResidue.oddProviderOfUnary`](../Paper2/Paper1ProvedOddResidueUnaryReduction.lean) |
| [2.14](../manuscript/paper.tex#L1680) | Tensor-factor extraction | Direct | [`FactorExtraction.source_2_14`](../Paper2/SourceFaithful/SourceStatements/FactorExtractionStatement.lean) |
| [2.15](../manuscript/paper.tex#L1696) | Quaternary eight-vertex boundary | Direct | [`EightVertexBoundary.theorem_2_15`](../Paper2/SourceFaithful/SourceStatements/EightVertexBoundary.lean) |
| [2.18](../manuscript/paper.tex#L1752) | Recognition and evaluation | Direct | [`Paper1ProvedRecognition.uniform_recognition`](../Paper2/Paper1ProvedRecognition/Source.lean) |
| [2.19](../manuscript/paper.tex#L1774) | Factor closure | Components | [`Paper2.exists_prime_decomposition`](../Paper2/PrimeFactorization.lean) |
| [2.20](../manuscript/paper.tex#L1805) | Downward inheritance | Direct | [`Tractable.downward_inheritance`](../Paper2/Tractable/Downward.lean) |
| [2.21](../manuscript/paper.tex#L1815) | `GO(X)`-invariance of tractability | Direct | [`Tractable.goX_tract_invariance`](../Paper2/Tractable/Conformal.lean) |
| [2.22](../manuscript/paper.tex#L1830) | Coordinate transport along equivalent augmentations | Direct | [`NormalizationLedger.source_2_22_natural`](../Paper2/SourceFaithful/SourceStatements/NormalizationLedgerInfinite.lean) |
| [2.23](../manuscript/paper.tex#L1919) | Binary-equality `K`-Holant dichotomy | Direct | [`Recognition.literalEqualityDichotomyWithRecognition_2_23`](../Paper2/ExactInput/Recognition/NativeComplete.lean) |
| [2.24](../manuscript/paper.tex#L1939) | Tensor-prime quaternary `K`-Holant dichotomy | Direct | [`Recognition.primeQuaternaryDichotomyWithRecognition_2_24`](../Paper2/ExactInput/Recognition/NativeComplete.lean) |
| [2.25](../manuscript/paper.tex#L1952) | Eight-vertex `K`-Holant dichotomy | Stronger | [`PublicDichotomy.theorem_9_2`](../Paper2/PublicNativeClassification.lean) |
| [3.1](../manuscript/paper.tex#L2004) | Binary interpolation | Direct | [`BinaryInterpolation.source_3_1`](../Paper2/SourceFaithful/SourceStatements/BinaryInterpolationStatement.lean) |
| [3.2](../manuscript/paper.tex#L2039) | Reduction with at most one `Delta`-vertex | Components | [`Paper1Proved.universalPair`](../Paper2/Paper1ProvedUniversalPairProvider.lean) |
| [3.3](../manuscript/paper.tex#L2059) | Single-occurrence replication | Direct | [`Replication.theorem_3_3_literal`](../Paper2/SourceFaithful/SourceStatements/ReplicationStatement.lean) |
| [3.4](../manuscript/paper.tex#L2114) | Dichotomy with a nonzero unary | Direct | [`UnaryProvider.native_classification`](../Paper2/Paper1ProvedOddUnaryComplete.lean) |
| [3.5](../manuscript/paper.tex#L2127) | Higher equality supplies unaries | Direct | [`EqualityPins.corollary_3_5`](../Paper2/SourceFaithful/SourceStatements/EqualityPinsStatement.lean) |
| [3.6](../manuscript/paper.tex#L2174) | Substitution of fixed gadgets in a larger signature set | Direct | [`RelativeEOAmbient.source_3_6`](../Paper2/SourceFaithful/SourceStatements/RelativeEOAmbientStatement.lean) |
| [3.7](../manuscript/paper.tex#L2205) | Hardness from an EO signature outside `B_ARS` | Components | [`RelativeEO.relative_terminal`](../Paper2/SourceFaithful/RelativeEO/Terminal.lean) |
| [3.8](../manuscript/paper.tex#L2219) | Complementary quaternaries supply a unary | Components | [`RelativeEO.complementary_supplies_pins`](../Paper2/SourceFaithful/RelativeEO/WeightedComplementaryExit.lean) |
| [3.9](../manuscript/paper.tex#L2278) | EO alternative | Stronger | [`RelativeEO.realized_isARSProduct`](../Paper2/SourceFaithful/RelativeEO/Terminal.lean) |
| [3.10](../manuscript/paper.tex#L2423) | ARS alternative | Components | [`RelativeEO.ars_relative_terminal`](../Paper2/SourceFaithful/RelativeEO/ARSTerminal.lean) |
| [3.13](../manuscript/paper.tex#L2540) | Dichotomy from a transformed quaternary equality | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [3.14](../manuscript/paper.tex#L2562) | Dichotomy with a generalized equality | Stronger | [`SourceFaithful.generalized_equality_relative_terminal`](../Paper2/SourceFaithful/GeneralizedEqualityTerminal.lean) |
| [3.15](../manuscript/paper.tex#L2577) | Dichotomy from a two-point Walsh factor | Stronger | [`TwoPointWalsh.source_3_15`](../Paper2/SourceFaithful/SourceStatements/TwoPointWalshStatement.lean) |
| [4.1](../manuscript/paper.tex#L2648) | Producing the gcd-height signature or both point masses | Direct | [`ChargeBridge.literal_charge_bridge`](../Paper2/ChargeBridgeReduction.lean) |
| [5.1](../manuscript/paper.tex#L2805) | Dichotomy with a height-one mountain | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [5.3](../manuscript/paper.tex#L2853) | Bounded torsion | Direct | [`GroupSplit.provedBoundedTorsion`](../Paper2/HeightOne/GroupSplit/Paper1Proved.lean) |
| [5.4](../manuscript/paper.tex#L2882) | Weighted equality or an odd cyclic or dihedral group | Direct | [`WeightedEqualityStage.theorem_5_4`](../Paper2/SourceFaithful/SourceStatements/WeightedEqualityStage.lean) |
| [5.5](../manuscript/paper.tex#L3092) | Equivalent updates with strict progress | Definition | [`HeightOne.PrimeStage`](../Paper2/SourceFaithful/HeightOneProgress.lean) |
| [5.6](../manuscript/paper.tex#L3127) | Termination of the strict updates | Direct | [`GroupSplit.no_infinite_fixed_field_updates`](../Paper2/HeightOne/UniformBound/Progress.lean) |
| [5.7](../manuscript/paper.tex#L3201) | The odd-dihedral case | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [5.8](../manuscript/paper.tex#L3270) | Finite recursive contraction and factor extraction | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [5.9](../manuscript/paper.tex#L3437) | Shared cyclic phase pencil, including zeros | Components | [`PhaseCards.provedPhasePencil`](../Paper2/HeightOne/PhaseCards/Paper1Pencil.lean) |
| [5.10](../manuscript/paper.tex#L3456) | Walsh parity from contractions | Direct | [`TypeParityStatement.lemma_5_10`](../Paper2/SourceFaithful/SourceStatements/TypeParityStatement.lean) |
| [5.11](../manuscript/paper.tex#L3564) | Closure of `\mathcal P_N` under contractions | Direct | [`SourceStatements.source_5_11`](../Paper2/SourceFaithful/SourceStatements/PhaseProductContractionStatement.lean) |
| [5.12](../manuscript/paper.tex#L3653) | Shared cyclic quaternary family | Direct | [`PhaseProductParity.source_5_12_literal`](../Paper2/SourceFaithful/SourceStatements/PhaseProductParityLiteralCyclic.lean) |
| [5.13](../manuscript/paper.tex#L3706) | Dihedral quaternary classification | Direct | [`PhaseProductParity.source_5_13_conditionC`](../Paper2/SourceFaithful/SourceStatements/PhaseProductParityFactorCondition.lean) |
| [5.14](../manuscript/paper.tex#L3791) | Six-port factorization from contractions | Direct | [`SixPortBinary.source_5_14`](../Paper2/SourceFaithful/SourceStatements/SixPortBinaryStatement.lean) |
| [5.15](../manuscript/paper.tex#L3862) | Three matching products on a line | Stronger | [`SourceStatements.source_5_15`](../Paper2/SourceFaithful/SourceStatements/ThreeMatchingLineStatement.lean) |
| [5.16](../manuscript/paper.tex#L3903) | Phase-independent matching and common factors | Stronger | [`DihedralRuling.source_5_16`](../Paper2/SourceFaithful/SourceStatements/DihedralRulingStatement.lean) |
| [5.17](../manuscript/paper.tex#L3941) | A binary factor from contractions | Stronger | [`DihedralRuling.source_5_17`](../Paper2/SourceFaithful/SourceStatements/DihedralRulingStatement.lean) |
| [5.18](../manuscript/paper.tex#L4052) | The odd-cyclic case | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [5.19](../manuscript/paper.tex#L4148) | Phase-independent matching | Components | [`CyclicCardFactorBridge.root_card_data`](../Paper2/SourceFaithful/SourceStatements/CyclicCardFactorBridge.lean) |
| [5.20](../manuscript/paper.tex#L4213) | Every port pair has a nonzero phase contraction above arity four | Stronger | [`CyclicCardFactorBridge.root_card_data`](../Paper2/SourceFaithful/SourceStatements/CyclicCardFactorBridge.lean) |
| [5.21](../manuscript/paper.tex#L4268) | Rank-one diagonal restrictions | Components | [`PhaseCards.provedDiagonalSlices`](../Paper2/HeightOne/PhaseCards/Paper1Diagonal.lean) |
| [5.22](../manuscript/paper.tex#L4291) | The minimum nonbinary arity is four in the cyclic case | Stronger | [`CyclicMinimumStatement.source_5_22`](../Paper2/SourceFaithful/SourceStatements/CyclicMinimumStatement.lean) |
| [5.23](../manuscript/paper.tex#L4417) | Attaching cyclic binary representatives to four ports | Direct | [`CyclicDressing.source_5_23`](../Paper2/SourceFaithful/SourceStatements/CyclicDressingStatement.lean) |
| [5.24](../manuscript/paper.tex#L4458) | The quaternary odd-cyclic case | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [5.25](../manuscript/paper.tex#L4659) | Hardness, tractability, or a strict update | Stronger | [`PublicDichotomy.native_dichotomy`](../Paper2/PublicDichotomyComplete.lean) |
| [6.1](../manuscript/paper.tex#L4780) | Dichotomy with a height-two mountain | Components | [`HeightTwo.mountain_classification`](../Paper2/SourceFaithful/HeightTwo.lean) |
| [7.1](../manuscript/paper.tex#L4801) | Height-three mountain dichotomy | Components | [`HeightThree.theorem_7_1`](../Paper2/SourceFaithful/HeightThree/Complete.lean) |
| [7.2](../manuscript/paper.tex#L4850) | A matching-product central layer yields a hard quaternary | Direct | [`TransversalCube.exists_native_gadget_WT18a`](../Paper2/TransversalCube.lean) |
| [7.3](../manuscript/paper.tex#L4940) | Loop and two-copy contractions of a six-port mountain | Definition | [`HeightThree.loopSignature_array`](../Paper2/HeightThree/LoopGeometry.lean) |
| [7.4](../manuscript/paper.tex#L4994) | Support forced by six-port contractions | Direct | [`Q6.joint_deck_support`](../Paper2/Certificates/Q6JointDeck.lean) |
| [7.5](../manuscript/paper.tex#L5018) | A non-matching quaternary output from a six-port mountain | Direct | [`HeightThree.nonmatching_mountain`](../Paper2/HeightThree/NonMatching.lean) |
| [8.1](../manuscript/paper.tex#L5083) | Mountain dichotomy at every height at least four | Components | [`HighHeight.classification_ge_four`](../Paper2/SourceFaithful/HighHeightCompleteTerminal.lean) |
| [8.3](../manuscript/paper.tex#L5178) | Vanishing pair contractions | Direct | [`CommonPhase.vanishing_pair_contractions_weight`](../Paper2/CommonPhase/ZeroLoops.lean) |
| [8.4](../manuscript/paper.tex#L5191) | Propagation of `X`-matching products | Direct | [`MatchingPropagation.x_line_propagation_source`](../Paper2/MatchingPropagation.lean) |
| [8.5](../manuscript/paper.tex#L5272) | Relative port normalization at every arity at least eight | Components | [`HighHeight.finite_port_normalization`](../Paper2/SourceFaithful/HighHeightCompleteNormalization.lean) |
| [8.6](../manuscript/paper.tex#L5350) | A common phase for EO contractions | Stronger | [`CommonPhase.common_phase_algebraic`](../Paper2/CommonPhase.lean) |
| [8.7](../manuscript/paper.tex#L5392) | Shao--Cai matching-product reconstruction | Stronger | [`HighHeightReconstruction.reconstruct_ge_ten`](../Paper2/HighHeightReconstruction/Source.lean) |
| [8.8](../manuscript/paper.tex#L5456) | A shared edge forces a matching product | Direct | [`Atlas.matching_deck_of_collision`](../Paper2/Certificates/Q8AlgebraicReconstruction.lean) |
| [8.9](../manuscript/paper.tex#L5477) | Translation form of the matching family | Components | [`Atlas.collision_free_translation`](../Paper2/Certificates/Q8AtlasUnnormalized.lean) |
| [8.10](../manuscript/paper.tex#L5520) | The matching family determines the central `RM(1,3)` coefficients | Direct | [`Atlas.collision_free_deck_reedMuller_algebraic`](../Paper2/Certificates/Q8AlgebraicReconstruction.lean) |
| [8.11](../manuscript/paper.tex#L5602) | Normalizing the endpoint coefficients of `RM core` | Components | [`ReedMullerNormalization.canonical_endpoint_repair`](../Paper2/ReedMullerNormalization/Endpoint.lean) |
| [8.12](../manuscript/paper.tex#L5685) | The Reed--Muller Bell reduction under high charge | Direct | [`BellTerminal.bell_reduction`](../Paper2/SourceFaithful/BellTerminal.lean) |
| [9.1](../manuscript/paper.tex#L5854) | Dichotomy for sets containing a mountain | Direct | [`Synthesis.theorem_9_1_public`](../Paper2/SourceFaithful/Synthesis/PublicMountainInterface.lean) |
| [9.2](../manuscript/paper.tex#L5886) | Structural classification in `K`-coordinates | Direct | [`PublicDichotomy.theorem_9_2`](../Paper2/PublicNativeClassification.lean) |
| [A.1](../manuscript/paper.tex#L6102) | Order-three odd-dihedral six-port classification | Direct | [`OddDihedralSixPort.source_A_1`](../Paper2/SourceFaithful/SourceStatements/OddDihedralSixPortStatement.lean) |
| [A.3](../manuscript/paper.tex#L6322) | Six-port support classification | Components | [`SixPortPencils.three_phase_union_card_le_four`](../Paper2/HeightOne/Dihedral/SixPortPencils.lean) |
| [A.4](../manuscript/paper.tex#L6409) | High-charge six-port coefficient classification | Direct | [`Q6.joint_deck_support`](../Paper2/Certificates/Q6JointDeck.lean) |
| [A.6](../manuscript/paper.tex#L6513) | Consequence for loop and two-copy arrays | Direct | [`Q6.joint_deck_support`](../Paper2/Certificates/Q6JointDeck.lean) |
| [A.8](../manuscript/paper.tex#L6566) | Eight-port matching classification | Direct | [`Atlas.normalizedAtlasEquiv`](../Paper2/Certificates/Q8AtlasClassification.lean) |
| [A.9](../manuscript/paper.tex#L6627) | Translation form of the matching family | Direct | [`Atlas.collision_free_translation`](../Paper2/Certificates/Q8AtlasUnnormalized.lean) |
| [A.10](../manuscript/paper.tex#L6655) | Coefficients on affine planes | Direct | [`AppendixSupport.source_A_10`](../Paper2/SourceFaithful/SourceStatements/AppendixSupportStatement.lean) |
| [A.11](../manuscript/paper.tex#L6752) | Affine-plane coefficients | Direct | [`AppendixSupport.source_A_11`](../Paper2/SourceFaithful/SourceStatements/AppendixSupportStatement.lean) |

## Deferred external references

Theorems 2.16 and 2.17 are independently cited degree-constrained CSP
classifications. Their retained structural components identify the relevant
classes and phase conventions. They are not presented as complete CSP
hardness classifications or complete public complexity interfaces.

## Expository remarks

The numbered remarks are 2.4, 2.5, 2.6, 2.9, 3.11, 3.12, 4.2, 5.2, 8.2, A.2, A.5, A.7.
They are source-index entries rather than independent Lean propositions.

## Independent statement comparison

[Verification](VERIFICATION.md) describes the separate statement challenge and
solution for Theorems 1.1, 9.1 and 9.2. The comparator checks their formal types
and dependent definitions; the source ledger supports the separate human task
of checking that those types express the intended mathematical statements.
