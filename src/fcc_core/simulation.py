import json
import math
from dataclasses import asdict
from typing import Dict, List, Tuple

import numpy as np

from .params import FCCParameters
from .state import FCCState

# --- Menger sponge child offsets (20 kept out of 27) ---
def _menger_child_offsets() -> List[Tuple[int,int,int]]:
    keep = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                # remove center and 6 face-centers (implemented by 'two coordinates == 1' rule)
                if (i == 1 and j == 1) or (i == 1 and k == 1) or (j == 1 and k == 1):
                    continue
                keep.append((i-1, j-1, k-1))
    assert len(keep) == 20
    return keep

_OFFSETS = _menger_child_offsets()

def p_defect(t: int, E_heal: float, params: FCCParameters) -> float:
    return float(params.p0 * (1.0 + params.eps) ** (-t) * math.exp(-params.k * E_heal))

def generate_children_centers(parent_centers: List[Tuple[float,float,float]], level: int) -> List[Tuple[float,float,float]]:
    """Generate centers of all 20-children for each parent at the next level."""
    parent_size = 3.0 ** (-level)
    child_size = parent_size / 3.0
    out = []
    for (x,y,z) in parent_centers:
        for (ox,oy,oz) in _OFFSETS:
            out.append((x + ox*child_size, y + oy*child_size, z + oz*child_size))
    return out

def apply_defects(all_child_centers: List[Tuple[float,float,float]], p_def: float, rng: np.random.Generator):
    realized = []
    defects = 0
    for c in all_child_centers:
        if rng.random() > p_def:
            realized.append(c)
        else:
            defects += 1
    return realized, defects

def R_heal(defects_count: int, budget: float, level: int) -> Tuple[int, float]:
    """Heal up to floor(budget/cost) defects, return healed_count and residual budget."""
    cost = 20.0 ** (-level)
    max_heal = int(budget // cost) if cost > 0 else 0
    healed = min(defects_count, max_heal)
    residual = budget - healed * cost
    return healed, residual

def evolve_step(state: FCCState, params: FCCParameters, rng: np.random.Generator) -> FCCState:
    t = state.t
    p_def = p_defect(t, state.E_heal, params)

    # generate next-level children centers and sample defects
    all_children = generate_children_centers(state.realized_centers, level=t)
    realized_next, defects_next = apply_defects(all_children, p_def, rng)

    # energy deficit due to defects
    Delta_E_geom = defects_next * (20.0 ** (-(t+1)))

    # healing budget
    E_heal_avail = state.E_heal + params.alpha * Delta_E_geom
    heal_need_max = Delta_E_geom
    E_heal_used = min(params.eta * E_heal_avail, heal_need_max)

    healed_count, residual = R_heal(defects_next, E_heal_used, t+1)

    # apply healing (by count; centers of healed are not tracked in this reference implementation)
    effective_defects = defects_next - healed_count

    # leak
    E_leak = params.beta * state.E_heal

    next_state = FCCState(
        t=t+1,
        realized_centers=realized_next,  # reference: only un-defected realized; healing effect on geometry is tracked via energy, not by adding centers
        defects_count=effective_defects,
        E_geom=state.E_geom - Delta_E_geom + E_heal_used + residual,
        E_heal=state.E_heal + params.alpha * Delta_E_geom - E_heal_used - E_leak,
        E_entropy=state.E_entropy + (1.0 - params.alpha) * Delta_E_geom + E_leak,
    )
    next_state.validate_energy()
    return next_state

def run_simulation(T_max: int, params: FCCParameters, seed: int = 42) -> List[FCCState]:
    params.validate()
    rng = np.random.default_rng(seed)

    # initial state: single cube center
    s0 = FCCState(
        t=0,
        realized_centers=[(0.5, 0.5, 0.5)],
        defects_count=0,
        E_geom=1.0,
        E_heal=0.0,
        E_entropy=0.0,
    )
    s0.validate_energy()
    states = [s0]
    for _ in range(T_max):
        states.append(evolve_step(states[-1], params, rng))
    return states

def export_run(states: List[FCCState], params: FCCParameters, out_path: str) -> None:
    payload: Dict = {
        "meta": {
            "model": "FCC-CORE",
            "version": "1.3.1",
            "seed": None,
        },
        "params": asdict(params),
        "series": [
            {
                "t": s.t,
                "defects_count": s.defects_count,
                "E_geom": s.E_geom,
                "E_heal": s.E_heal,
                "E_entropy": s.E_entropy,
                "n_realized_centers": len(s.realized_centers),
            }
            for s in states
        ],
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
