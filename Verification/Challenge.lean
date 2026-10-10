import Paper2.ExactInput.Recognition.NativeUniform
import Paper2.Mountain

/-!
# Independently reviewable statements

These are the three principal manuscript contracts, written explicitly without
importing the classification proofs. The three `sorry` terms are intentional
reference holes used only by leanprover/comparator. This module must never be
imported by `Paper2` or by `Verification.Solution`.

The trusted definitions below retain the literal finite algebraic table input,
ordered graph ports, strict algebraic output encoding, seven family-wide
tractability alternatives, and finite machine semantics. Recognition is
effective; evaluation is polynomial for each fixed language. No polynomial
bound is claimed for recognition as the language itself varies.
-/
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
  sorry

/-- Theorem 9.1. Supported half-charge divisibility is needed only at height ≥ 3. -/
theorem mountain_classification
    (L : Language) {d : ℕ}
    (heven : ∀ f ∈ L.family, Even f.1)
    (hdiv : 3 ≤ d → ∀ f ∈ L.family, Tensor.HalfChargeDivisible f.2 d)
    (M : Signature AlgebraicComplex (2*d)) (hM : IsMountain M)
    (hmem : (⟨2*d, M⟩ : AnySignature AlgebraicComplex) ∈ L.family) :
    Tract (kImage L) ∨ Problem.SharpPHard .nativeX L := by
  sorry

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
  sorry

end
end Paper2.Verification.Theorems
