from fcc_core.params import FCCParameters
from fcc_core.simulation import run_simulation

def test_energy_conserved():
    params = FCCParameters()
    states = run_simulation(T_max=8, params=params, seed=1)
    for s in states:
        assert abs(s.total_energy() - 1.0) < 1e-10
