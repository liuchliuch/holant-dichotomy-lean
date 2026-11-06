import Paper2.STOC2027

/-! Proved counterparts of the separately loaded Comparator challenge. -/
namespace Paper2.Verification.Theorems
open Paper2.Tractable Paper2.ExactInput Paper2.Problem
noncomputable section

/-- Short Theorem 1.1 / full Theorem F.1.1, with effective ordinary recognition. -/
theorem main_classification :
    ∃ r : TractRecognizer,
      (∀ raw : RawLanguage, ∀ hraw : raw.Valid,
        ∃ b : Bool, ∃ steps : ℕ,
          (fun c : Option r.machine.tm.Cfg => c.bind r.machine.tm.step)^[steps]
            (some (r.initial raw)) = some (r.final b) ∧
          r.machine.tm.step (r.final b) = none ∧
          (b = true ↔ Tract (Language.family ⟨raw, hraw⟩))) ∧
      (∀ L : Language,
        (r.decision L = true ↔ Tract L.family) ∧
        (Tract L.family → Problem.InFP .ordinary L) ∧
        (¬Tract L.family → Problem.SharpPHard .ordinary L)) := by
  exact Paper2.STOC2027.full_dichotomy

/-- Full Theorem F.10.1. Supported half-charge divisibility is needed only at height ≥ 3. -/
theorem mountain_classification
    (L : Language) {d : ℕ}
    (heven : ∀ f ∈ L.family, Even f.1)
    (hdiv : 3 ≤ d → ∀ f ∈ L.family, Tensor.HalfChargeDivisible f.2 d)
    (M : Signature AlgebraicComplex (2*d)) (hM : IsMountain M)
    (hmem : (⟨2*d, M⟩ : AnySignature AlgebraicComplex) ∈ L.family) :
    Tract (kImage L) ∨ Problem.SharpPHard .nativeX L := by
  exact Paper2.STOC2027.mountain_dichotomy L heven hdiv M hM hmem

/-- Full Theorem F.10.3, including effective recognition on each valid exact table list. -/
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
  exact Paper2.STOC2027.native_dichotomy

end
end Paper2.Verification.Theorems
