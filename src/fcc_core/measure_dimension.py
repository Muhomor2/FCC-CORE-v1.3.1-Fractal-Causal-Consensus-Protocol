import math
from typing import List, Tuple

def box_counting_dimension(points: List[Tuple[float,float,float]], t_max: int):
    """Estimate D_eff via box-counting on scales r_i = 3^{-i}, i=0..t_max."""
    if not points:
        return float("nan"), [], []

    scales = [3.0 ** (-i) for i in range(t_max + 1)]
    Ns = []
    xs = []  # log(1/r)
    ys = []  # log N

    for r in scales:
        occupied = set()
        inv = 1.0 / r
        for (x,y,z) in points:
            idx = (int(x*inv), int(y*inv), int(z*inv))
            occupied.add(idx)
        N = len(occupied)
        if N <= 0:
            continue
        xs.append(math.log(inv))
        ys.append(math.log(N))
        Ns.append(N)

    # simple least squares slope
    n = len(xs)
    if n < 2:
        return float("nan"), scales, Ns

    xbar = sum(xs)/n
    ybar = sum(ys)/n
    num = sum((xs[i]-xbar)*(ys[i]-ybar) for i in range(n))
    den = sum((xs[i]-xbar)**2 for i in range(n))
    D = num/den if den > 0 else float('nan')
    return D, scales, Ns
