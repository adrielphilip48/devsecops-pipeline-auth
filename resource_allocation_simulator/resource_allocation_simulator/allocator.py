"""
allocator.py

Implements several budget-allocation strategies for distributing a fixed
pool of additional education funding across regions. Each strategy
returns {region_name: extra_funding_per_pupil}.

Strategies:
    equal_split        - every region gets the same extra amount per pupil
    enrollment_weighted - extra budget split in proportion to student numbers
                          (efficiency-oriented: funds go where the most
                          students are)
    needs_weighted      - extra budget split in proportion to how far below
                          the best-funded region each region currently is
                          (equity-oriented: funds go where the gap is biggest)
    hybrid              - a blend of enrollment_weighted and needs_weighted,
                          controlled by a weighting parameter alpha
"""

from __future__ import annotations
from region import Region


class BudgetAllocator:
    def __init__(self, regions: list[Region], total_budget: float):
        """
        total_budget: total additional money (TZS) available to allocate
        across all regions this year.
        """
        self.regions = regions
        self.total_budget = total_budget

    # ------------------------------------------------------------------
    def _to_per_pupil(self, region_shares: dict[str, float]) -> dict[str, float]:
        """Convert a {region: total_money} allocation into {region: extra funding per pupil}."""
        result = {}
        for region in self.regions:
            total_for_region = region_shares[region.name]
            result[region.name] = total_for_region / region.students
        return result

    # ------------------------------------------------------------------
    def equal_split(self) -> dict[str, float]:
        share = self.total_budget / len(self.regions)
        return self._to_per_pupil({r.name: share for r in self.regions})

    def enrollment_weighted(self) -> dict[str, float]:
        total_students = sum(r.students for r in self.regions)
        shares = {r.name: self.total_budget * (r.students / total_students) for r in self.regions}
        return self._to_per_pupil(shares)

    def needs_weighted(self) -> dict[str, float]:
        best_funding = max(r.funding_per_pupil for r in self.regions)
        gaps = {r.name: max(best_funding - r.funding_per_pupil, 0) for r in self.regions}
        total_gap = sum(gaps.values())
        shares = {r.name: self.total_budget * (gaps[r.name] / total_gap) for r in self.regions}
        return self._to_per_pupil(shares)

    def hybrid(self, alpha: float = 0.5) -> dict[str, float]:
        """
        alpha=1.0 -> pure enrollment_weighted
        alpha=0.0 -> pure needs_weighted
        """
        enrollment = self.enrollment_weighted()
        needs = self.needs_weighted()
        return {
            r.name: alpha * enrollment[r.name] + (1 - alpha) * needs[r.name]
            for r in self.regions
        }

    def strategies(self) -> dict[str, dict[str, float]]:
        """Run all four strategies and return {strategy_name: allocation}."""
        return {
            "Equal split": self.equal_split(),
            "Enrollment-weighted": self.enrollment_weighted(),
            "Needs-weighted": self.needs_weighted(),
            "Hybrid (50/50)": self.hybrid(0.5),
        }
