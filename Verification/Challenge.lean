import Paper2.ExactInput.Recognition.NativeUniform
import Paper2.Mountain

/-!
# Independently reviewable statements

These are the three principal STOC 2027 manuscript contracts: short Theorem 1.1
(also full Theorem F.1.1), full Theorem F.10.1, and full Theorem F.10.3. They are
written explicitly without importing the classification proofs or their public
wrappers. The three `sorry` terms are intentional
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
  sorry

/-- Full Theorem F.10.1. Supported half-charge divisibility is needed only at height ≥ 3. -/
theorem mountain_classification
    (L : Language) {d : ℕ}
    (heven : ∀ f ∈ L.family, Even f.1)
    (hdiv : 3 ≤ d → ∀ f ∈ L.family, Tensor.HalfChargeDivisible f.2 d)
    (M : Signature AlgebraicComplex (2*d)) (hM : IsMountain M)
    (hmem : (⟨2*d, M⟩ : AnySignature AlgebraicComplex) ∈ L.family) :
    Tract (kImage L) ∨ Problem.SharpPHard .nativeX L := by
  sorry

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
  sorry

end
end Paper2.Verification.Theorems
