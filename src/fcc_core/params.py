from dataclasses import dataclass

@dataclass(frozen=True)
class FCCParameters:
    # Defect generation
    p0: float = 0.10     # base defect probability
    eps: float = 0.30    # decay with level (must be >0 for stability)
    k: float = 2.00      # sensitivity to E_heal

    # Energy redistribution
    alpha: float = 0.70  # deficit -> healing share
    eta: float = 0.50    # healing efficiency
    beta: float = 0.02   # leak from healing -> entropy

    def validate(self) -> None:
        assert 0.0 < self.p0 < 1.0
        assert self.eps > 0.0
        assert self.k >= 0.0
        assert 0.0 <= self.alpha <= 1.0
        assert 0.0 <= self.eta <= 1.0
        assert 0.0 <= self.beta <= 1.0

        # Recommended stability constraints
        assert self.alpha * self.eta > (1.0 - self.alpha), "Constraint: alpha*eta > (1-alpha)"
        assert self.beta < self.alpha * self.eta, "Constraint: beta < alpha*eta"
        assert self.p0 < (1.0 + self.eps) / 20.0, "Constraint: p0 < (1+eps)/20"
