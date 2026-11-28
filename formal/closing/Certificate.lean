import Mathlib.Algebra.Field.Basic
import Mathlib.Tactic.Ring
namespace NashBase
variable {F : Type*} [Field F]
/-- Evaluation of the row-player equation against its four independent payoff entries. -/
def rowBase (a b c d : F) := ∀ x y z w : F,
  (c+d)*(a*x+b*y) - (a+b)*(c*z+d*w) = 0
theorem row_base_iff (a b c d : F) : rowBase a b c d ↔
    (a=0 ∧ b=0) ∨ (c=0 ∧ d=0) ∨ (a+b=0 ∧ c+d=0) := by
  constructor
  · intro h
    have h1 := h 1 0 0 0
    have h2 := h 0 1 0 0
    have h3 := h 0 0 1 0
    have h4 := h 0 0 0 1
    simp_all only [mul_one,mul_zero,add_zero,zero_add,sub_zero,zero_sub,neg_eq_zero,mul_eq_zero]
    grind
  · rintro (⟨rfl,rfl⟩|⟨rfl,rfl⟩|⟨h1,h2⟩) <;> intro x y z w <;> simp_all
/-- The simultaneous row and column base locus consists of the four coordinate
axes and the checkerboard line in the affine cone, hence five projective points. -/
theorem mixed_base (a b c d : F) : rowBase a b c d ∧ rowBase a c b d ↔
  (b=0 ∧ c=0 ∧ d=0) ∨ (a=0 ∧ c=0 ∧ d=0) ∨
  (a=0 ∧ b=0 ∧ d=0) ∨ (a=0 ∧ b=0 ∧ c=0) ∨ (b= -a ∧ c= -a ∧ d=a) := by
  simp only [row_base_iff]
  constructor
  · rintro ⟨h,k⟩
    rcases h with h|h|h <;> rcases k with k|k|k <;> grind
  · rintro (h|h|h|h|h) <;> grind
end NashBase
#print axioms NashBase.mixed_base
