# FCC-CORE v1.3.x — Overview

FCC-CORE models a fractal causal substrate constructed via Menger sponge expansion.
At each level `t`, each existing cell produces 20 children; a subset fails to realize
(stochastic defects). An explicit energy budget is redistributed across:

- `E_geom`   — geometric realization energy
- `E_heal`   — repair/healing reserve
- `E_entropy`— irreversible leakage / entropy channel

The key invariant is conservation of total energy:
`E_total(t) = E_geom(t) + E_heal(t) + E_entropy(t) = 1` for all `t`.

See:
- `docs/specification.md` (formal definitions)
- `docs/constraints.md` (stability constraints)
- `docs/measurement_box_counting.md` (D_eff estimation)
