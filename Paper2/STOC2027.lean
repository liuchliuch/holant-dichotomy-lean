import Paper2.PublicNativeClassification
import Paper2.SourceFaithful.Synthesis.PublicMountainInterface

/-!
# Public statements for the STOC 2027 manuscript

The November 6, 2026 manuscript contains a short paper and an embedded full
paper. The semantic names in this module follow their current statements:
short Theorem 1.1 / full Theorem F.1.1, full Theorem F.10.1, and full
Theorem F.10.3. The older numbered proof declarations remain available for
compatibility with the arXiv-v1 development; their numbers are historical.

The proofs below transport the already proved public results without changing
the structural criterion, exact algebraic input, original graph semantics,
strict root output convention, or polynomial-time reduction semantics.
-/
namespace Paper2.STOC2027
open Paper2.Tractable Paper2.ExactInput Paper2.Problem
noncomputable section

/-- Short Theorem 1.1 and full Theorem F.1.1 (`short:thm:main`, `thm:main`).
One finite recognizer precedes all varying valid table inputs. Evaluation and
hardness are polynomial for each fixed language, with no arity or unary promise.
This is the ordinary-coordinate projection of the proved public classification. -/
theorem full_dichotomy :
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
  obtain ⟨r, hrun, hclassification, _⟩ := Paper2.PublicDichotomy.main_theorem
  exact ⟨r, hrun, hclassification⟩

/-- Full Theorem F.10.1 (`thm:mountain-interface`). Every original signature
has even arity, and the mountain belongs to the original language. Supported
half-charge divisibility of the whole language is required only at height ≥ 3. -/
theorem mountain_dichotomy
    (L : Language) {d : ℕ}
    (heven : ∀ f ∈ L.family, Even f.1)
    (hdiv : 3 ≤ d → ∀ f ∈ L.family, Tensor.HalfChargeDivisible f.2 d)
    (M : Signature AlgebraicComplex (2*d)) (hM : IsMountain M)
    (hmem : (⟨2*d, M⟩ : AnySignature AlgebraicComplex) ∈ L.family) :
    Tract (kImage L) ∨ Problem.SharpPHard .nativeX L := by
  exact Paper2.SourceFaithful.Synthesis.theorem_9_1_public L heven hdiv M hM hmem

/-- Full Theorem F.10.3 (`thm:K-structural`). The criterion is literally
`Tract (kImage L)`, with an effective recognizer on varying native tables and
polynomial evaluation or hardness for each fixed original native-X language. -/
theorem native_dichotomy :
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
end Paper2.STOC2027
