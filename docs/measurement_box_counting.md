# Measuring effective fractal dimension D_eff (box-counting)

Given realized cell centers `x(v) ∈ R^3` at level `t`:

1. Choose scales `r_i = 3^{-i}`, `i = 0..t`
2. For each `r_i`, map each point to a grid index:
   `idx = (floor(x/r_i), floor(y/r_i), floor(z/r_i))`
3. Let `N(r_i)` be the number of occupied grid boxes
4. Fit a line to `log N(r_i)` vs `log(1/r_i)`; slope ≈ `D_eff`

The reference implementation is in `src/fcc_core/measure_dimension.py`.
