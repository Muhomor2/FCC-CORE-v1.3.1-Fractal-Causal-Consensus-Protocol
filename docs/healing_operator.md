# Healing operator R_heal (strict)

At level `t+1`:
- per-cell repair cost: `cost = 20^{-(t+1)}`
- given a budget `B`, the operator repairs at most `floor(B / cost)` defects
- the remaining budget `B_residual = B - healed_count·cost` is preserved

This avoids fractional-cell paradox at large `t`.
