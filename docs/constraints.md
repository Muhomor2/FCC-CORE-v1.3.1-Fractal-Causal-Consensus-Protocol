# Parameter constraints (recommended)

These constraints are *sufficient* (not claimed necessary) for stable first runs:

1. Defect probability decays: `ε > 0`
2. Healing dominates entropy inflow: `α·η > (1-α)`
3. Leak does not dominate healing budget: `β < α·η`
4. Base defects bounded (mean-field sanity): `p0 < (1+ε)/20`

The code enforces these by default in `FCCParameters.validate()`.
