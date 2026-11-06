import Paper2.SourceFaithful.ChargeBridgeReduction
import Paper2.SourceFaithful.RelativeEO.Terminal
import Paper2.SourceFaithful.SourceStatements.PublicReduction
import Paper2.Paper1ProvedGadgetProvider
import Paper2.Paper1ProvedFactorProvider
import Paper2.Paper1ProvedRestrictionProvider
import Paper2.Paper1ProvedOccurrenceProvider
import Paper2.Paper1ProvedInterpolationProvider
import Paper2.Paper1ProvedOddUnaryComplete
import Paper2.Synthesis.GcdMountain
import Paper2.ReedMullerNormalization.Endpoint

/-!
# Literal interfaces for the STOC 2027 manuscript

The short paper first removes zero and nullary signatures (Section 2), so its
mountain and relative-EO lemmas concern `Preprocessed` languages. The wrappers
below discharge every lower-level Paper 1 provider with its proved instance
and expose the strict public root-output reductions and hardness statements.
The endpoint lemma also records the revised convention `D(t) = diag(1,t)`;
its scalar is retained in both the tensor action and the edge congruence.
-/

namespace Paper2.STOC2027
open Paper2.Tractable Paper2.ExactInput
noncomputable section

/-- Short Lemma 3.1 and full Lemma F.5.2. The gcd divisibility conclusion
holds on the entire augmented language, including the constructed mountain.
Both reductions use the public exact algebraic output convention. -/
theorem mountain_construction
    (L : Language) (hpre : Preprocessed L.family)
    (heven : ∀ f ∈ L.family, Even f.1) (hboth : BothChargeSigns L.family) :
    let d := ChargeBridge.languageGcd L
    0 < d ∧ (∀ f ∈ L.family, Tensor.HalfChargeDivisible f.2 d) ∧
      ((∃ f : Signature AlgebraicComplex (2 * d), IsMountain f ∧
          ∃ M : Language,
            M.family = insert (⟨2 * d, f⟩ : AnySignature AlgebraicComplex) L.family ∧
            (∀ g ∈ M.family, Tensor.HalfChargeDivisible g.2 d) ∧
            Problem.Reduces .nativeX M L ∧ Problem.Reduces .nativeX L M) ∨
        ∃ M : Language,
          M.family = insert (⟨1, TensorDecomposition.literalPin false⟩ : AnySignature AlgebraicComplex)
            (insert (⟨1, TensorDecomposition.literalPin true⟩ : AnySignature AlgebraicComplex) L.family) ∧
          Problem.Reduces .nativeX M L ∧ Problem.Reduces .nativeX L M) := by
  obtain ⟨hpos, hneg⟩ := Paper2.Synthesis.signs_as_halfCharges L heven
    (Paper2.RelativeEO.bothChargeSigns_not_oneSided hboth)
  obtain ⟨hd, hdiv, hout⟩ := SourceFaithful.ChargeBridge.literal_charge_bridge
    Paper1Proved.directGadgetProvider Paper1Proved.factorProvider
    Paper1Proved.restrictionProvider L hpre (fun i => heven _ ⟨i, rfl⟩) hpos hneg
  have hdivL : ∀ f ∈ L.family,
      Tensor.HalfChargeDivisible f.2 (ChargeBridge.languageGcd L) := by
    rintro f ⟨i, rfl⟩
    exact hdiv i
  refine ⟨hd, hdivL, ?_⟩
  rcases hout with ⟨f, hf, M, hM, hML, hLM⟩ | ⟨M, hM, hML, hLM⟩
  · left
    refine ⟨f, hf, M, hM, ?_,
      SourceFaithful.SourceStatements.PublicReduction.of_fixed_field .nativeX M L hML,
      SourceFaithful.SourceStatements.PublicReduction.of_fixed_field .nativeX L M hLM⟩
    intro g hg
    rw [hM] at hg
    rcases hg with rfl | hg
    · exact Paper2.Synthesis.mountain_halfCharge_divisible hf
    · exact hdivL g hg
  · exact Or.inr ⟨M, hM,
      SourceFaithful.SourceStatements.PublicReduction.of_fixed_field .nativeX M L hML,
      SourceFaithful.SourceStatements.PublicReduction.of_fixed_field .nativeX L M hLM⟩

/-- Short Lemma 5.1 (and full Theorem F.4.13), on the original ambient
language. The exact `B_ARS` predicate and all source hypotheses are retained;
no EO classification of the mixed ambient set is assumed. -/
theorem eo_output_hardness
    (L : Language) (hpre : Preprocessed L.family)
    (_heven : ∀ f ∈ L.family, Even f.1) (hboth : BothChargeSigns L.family)
    (hnot : ¬ Tract (kImage L)) {n : ℕ} (f : Signature AlgebraicComplex n)
    (he : Signature.CentralSupport f)
    (hmem : (⟨n, f⟩ : AnySignature AlgebraicComplex) ∈ L.family)
    (hout : ¬ Paper2.RelativeEO.IsARSProduct f) : Problem.SharpPHard .nativeX L := by
  apply SourceFaithful.public_hardness_of_fixed_field .nativeX L
  exact SourceFaithful.RelativeEO.relative_terminal
    Paper1Proved.directGadgetProvider Paper1Proved.occurrenceProvider
    Paper1Proved.factorProvider Paper1Proved.OddUnary.UnaryProvider.proved
    Paper1Proved.eoProvider Paper1Proved.restrictionProvider
    Paper1Proved.binaryInterpolationProvider L hpre hboth hnot f he hmem hout

section Diagonal
variable {F : Type*} [Field F]

/-- The revised manuscript's `D(t) = diag(1,t)`, as a literal binary kernel. -/
def diagonalParameter (t : F) : Kernel F := fun a b =>
  (if a then t else 1) * Signature.equality a b

/-- The scalar in `s D(s^-2)` is essential: the resulting matrix is exactly
`diag(s,s^-1)`, not merely projectively equivalent to it. -/
theorem scaled_diagonalParameter (s : F) (hs : s ≠ 0) :
    (fun a b => s * diagonalParameter (s ^ (-2 : ℤ)) a b) =
      ReedMullerNormalization.diagonal s := by
  funext a b
  cases a <;> cases b <;>
    simp [diagonalParameter, ReedMullerNormalization.diagonal, Signature.equality,
      zpow_neg, pow_two, hs]

/-- Full Lemma F.9.11 in the revised diagonal notation. The alternative is
the actual two-source, five-edge six-variable output. Every normalizing root
gives both the literal tensor identity and exact preservation of the X edge. -/
theorem endpoint_normalization [CharZero F] (A B c : F) (hnz : A * B * c ≠ 0) :
    (ReedMullerNormalization.sixOutput A B c ≠ 0 ∧
      Signature.CentralSupport (ReedMullerNormalization.sixOutput A B c) ∧
      ¬ WeightedMatching.IsProduct (ReedMullerNormalization.sixOutput A B c)) ∨
    (A * B = c ^ 2 ∧ ∀ s : F, s ^ 8 = c / A →
      (fun a b => s * diagonalParameter (s ^ (-2 : ℤ)) a b) =
        ReedMullerNormalization.diagonal s ∧
      Signature.coordinateAction
        (fun _ a b => s * diagonalParameter (s ^ (-2 : ℤ)) a b)
        (ReedMullerNormalization.source A B c) = (fun x => c * ReedMuller.core x) ∧
      Kernel.mul
        (Kernel.mul
          (Kernel.transpose (fun a b => s * diagonalParameter (s ^ (-2 : ℤ)) a b)) Bell.X)
        (fun a b => s * diagonalParameter (s ^ (-2 : ℤ)) a b) = Bell.X) := by
  rcases ReedMullerNormalization.canonical_endpoint_repair A B c hnz with h | ⟨hab, h⟩
  · exact Or.inl h
  · right
    refine ⟨hab, ?_⟩
    intro s hs8
    have hc : c ≠ 0 := (mul_ne_zero_iff.mp hnz).2
    have hA : A ≠ 0 := (mul_ne_zero_iff.mp (mul_ne_zero_iff.mp hnz).1).1
    have hs : s ≠ 0 := by
      intro hz
      apply div_ne_zero hc hA
      rw [← hs8, hz]
      simp
    have he := scaled_diagonalParameter s hs
    refine ⟨he, ?_⟩
    have heAction :
        (fun (_ : Fin 8) a b => s * diagonalParameter (s ^ (-2 : ℤ)) a b) =
          (fun _ : Fin 8 => ReedMullerNormalization.diagonal s) :=
      funext (fun _ => he)
    rw [heAction, he]
    exact h s hs8

end Diagonal
end
end Paper2.STOC2027
