from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Cell:
    id: int
    level: int
    x: Tuple[float, float, float]
    parent_id: int | None = None

@dataclass
class FCCState:
    t: int
    # For reproducibility and memory safety we store *counts* and centers list (optional)
    realized_centers: List[Tuple[float, float, float]] = field(default_factory=list)
    defects_count: int = 0
    E_geom: float = 0.0
    E_heal: float = 0.0
    E_entropy: float = 0.0

    def total_energy(self) -> float:
        return self.E_geom + self.E_heal + self.E_entropy

    def validate_energy(self, tol: float = 1e-10) -> None:
        total = self.total_energy()
        assert abs(total - 1.0) < tol, f"Energy not conserved: {total}"
        assert 0.0 <= self.E_geom <= 1.0
        assert 0.0 <= self.E_heal <= 1.0
        assert 0.0 <= self.E_entropy <= 1.0
