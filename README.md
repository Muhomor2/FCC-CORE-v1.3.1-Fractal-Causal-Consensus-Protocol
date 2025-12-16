# FCC-CORE v1.3.1

**FCC-CORE** is a research software + formal-specification package implementing the **Fractal Causal Core** model (FCC-CORE v1.3.x): Menger-sponge growth with stochastic defects, cost-bounded healing, and an explicit energy invariant.

- **Author:** Igor Chechelnitsky (ORCID: 0009-0007-4607-1946)
- **Version:** v1.3.1
- **Jurisdiction:** Israel (primary)
- **Primary outputs:** reproducible simulation code + specification + preprint source

## Repository layout

- `docs/` — specification, model definitions, measurement procedures (D_eff via box-counting)
- `src/fcc_core/` — Python implementation (simulation + measurement)
- `scripts/` — runnable entry points
- `tests/` — invariants / energy conservation checks
- `paper/` — LaTeX preprint (Zenodo-ready)
- `reviews/` — BC5 critical review and implementation plan (RU)
- `reproducibility/` — environment pins / seeds

## Quickstart (local, non-commercial)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reproducibility/requirements.txt

python scripts/run_simulation.py --T 12 --seed 42
python scripts/analyze_results.py --input outputs/run_T12_seed42.json
```

Outputs are written to `outputs/`:
- time series of energies (E_geom, E_heal, E_entropy)
- defect counts (absolute + normalized)
- convergence diagnostics for Σ (δ_t / 20^t)

## Reproducibility

- Fixed RNG seeds are supported (see `reproducibility/seeds.md`)
- Deterministic invariants are unit-tested (`tests/test_energy_conservation.py`)
- Parameter constraints are validated in code (see `docs/constraints.md`)

## License (IMPORTANT)

This repository is distributed under the **Combined License: FCC-CORE v1.3.1**:
- **CC BY-NC-ND 4.0 + OSL-ER v1.0 + Anti-Harm + No Commercial Use**
- The **most restrictive provisions apply**.
- **Commercial use is strictly prohibited** without explicit written permission.
- **No-derivatives**: do not fork/modify; use Issues to propose changes.

See [`LICENSE.txt`](LICENSE.txt) and [`NOTICE.md`](NOTICE.md).

## How to cite

See [`CITATION.cff`](CITATION.cff). For papers:

> Chechelnitsky, I. (2025). *FCC-CORE v1.3.1: Fractal Causal Core with cost-bounded healing and energy invariants* (v1.3.1). Zenodo. DOI: (assigned after Zenodo release).

## Zenodo publishing checklist (GitHub → Zenodo)

## Contact

- GitHub Issues (preferred)
- ORCID: 0009-0007-4607-1946
