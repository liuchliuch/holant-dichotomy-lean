import Paper2.PublicNativeClassification
import Paper2.SourceFaithful.Synthesis.PublicMountainInterface

/-! Proved counterparts of the separately loaded Comparator challenge. -/
namespace Paper2.Verification.Theorems
open Paper2.Tractable Paper2.ExactInput Paper2.Problem
noncomputable section

/-- Theorem 1.1, with effective recognition in both coordinate conventions. -/
theorem main_classification :
    ∃ ordinary : TractRecognizer, ∃ native : NativeTractRecognizer,
      (∀ raw : RawLanguage, ∀ hraw : raw.Valid,
        ∃ b : Bool, ∃ steps : ℕ,
          (fun c : Option ordinary.machine.tm.Cfg => c.bind ordinary.machine.tm.step)^[steps]
            (some (ordinary.initial raw)) = some (ordinary.final b) ∧
          ordinary.machine.tm.step (ordinary.final b) = none ∧
          (b = true ↔ Tract (Language.family ⟨raw, hraw⟩))) ∧
      (∀ raw : RawLanguage, ∀ hraw : raw.Valid,
        ∃ b : Bool, ∃ steps : ℕ,
          (fun c : Option native.machine.tm.Cfg => c.bind native.machine.tm.step)^[steps]
            (some (native.initial raw)) = some (native.final b) ∧
          native.machine.tm.step (native.final b) = none ∧
          (b = true ↔ Tract (kImage (⟨raw, hraw⟩ : Language)))) ∧
      (∀ L : Language,
        (ordinary.decision L = true ↔ Tract L.family) ∧
        (native.decision L = true ↔ Tract (kImage L)) ∧
        (Tract L.family → Problem.InFP .ordinary L) ∧
        (¬Tract L.family → Problem.SharpPHard .ordinary L) ∧
        (Tract (kImage L) → Problem.InFP .nativeX L) ∧
        (¬Tract (kImage L) → Problem.SharpPHard .nativeX L)) := by
  exact Paper2.PublicDichotomy.main_theorem_with_native_recognition

/-- Theorem 9.1. Supported half-charge divisibility is needed only at height ≥ 3. -/
theorem mountain_classification
    (L : Language) {d : ℕ}
    (heven : ∀ f ∈ L.family, Even f.1)
    (hdiv : 3 ≤ d → ∀ f ∈ L.family, Tensor.HalfChargeDivisible f.2 d)
    (M : Signature AlgebraicComplex (2*d)) (hM : IsMountain M)
    (hmem : (⟨2*d, M⟩ : AnySignature AlgebraicComplex) ∈ L.family) :
    Tract (kImage L) ∨ Problem.SharpPHard .nativeX L := by
  exact Paper2.SourceFaithful.Synthesis.theorem_9_1_public L heven hdiv M hM hmem

/-- Theorem 9.2, including effective recognition on each valid exact table list. -/
theorem native_classification :
    ∃ r : NativeTractRecognizer,
      (∀ raw : RawLanguage, ∀ hraw : raw.Valid,
        ∃ b : Bool, ∃ steps : ℕ,
          (fun c : Option r.machine.tm.Cfg => c.bind r.machine.tm.step)^[steps]
            (some (r.initial raw)) = some (r.final b) ∧
          r.machine.tm.step (r.final b) = none ∧
          (b = true ↔ Tract (kImage (⟨raw, hraw⟩ : Language)))) ∧
      (∀ L : Language,
        (r.decision L = true ↔ Tract (kImage L)) ∧
        (Tract (kImage L) → Problem.InFP .nativeX L) ∧
        (¬Tract (kImage L) → Problem.SharpPHard .nativeX L)) := by
  exact Paper2.PublicDichotomy.theorem_9_2

end
end Paper2.Verification.Theorems
