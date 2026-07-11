"""
impact_model.py

A simple diminishing-returns model used to project the effect of extra
funding per pupil on exam pass rates.

Core assumption (the whole point of this project, and the link back to
my EPQ): money alone does not translate directly into better results.
Its effectiveness is moderated by teacher retention -- a region that
keeps losing trained teachers gets much less benefit from the same
extra shilling per pupil than a region with a stable teaching staff.

    pass_rate_gain = K * sqrt(extra_funding_per_pupil) * retention_rate

- sqrt() gives diminishing returns: the first extra funding matters a
  lot more than the last (consistent with standard economic reasoning
  about marginal returns to investment).
- retention_rate (1 - teacher_attrition) scales the effect: the same
  funding produces a smaller gain where attrition is high.
- Gains are capped so no region can be projected above 100%.

This is a simplified illustrative model, not a validated econometric
one -- it is designed to demonstrate the concept and generate a
concrete, testable claim: "resourcing alone underperforms in regions
with high teacher attrition, even when it receives the most money."
"""

from __future__ import annotations
from region import Region

K = 0.09  # scaling constant, chosen so gains stay in a realistic range


class ImpactModel:
    def __init__(self, k: float = K):
        self.k = k

    def project_pass_rate(self, region: Region, extra_funding_per_pupil: float) -> float:
        """Return the projected new pass rate for a region given extra funding."""
        if extra_funding_per_pupil <= 0:
            return region.pass_rate

        gain = self.k * (extra_funding_per_pupil ** 0.5) * region.retention_rate
        new_rate = region.pass_rate + gain
        return min(new_rate, 100.0)

    def project_all(self, regions: list[Region], allocation: dict[str, float]) -> dict[str, dict]:
        """
        Given a list of regions and a {region_name: extra_funding_per_pupil}
        allocation, return {region_name: {"old": x, "new": y, "gain": y - x}}.
        """
        results = {}
        for region in regions:
            extra = allocation[region.name]
            new_rate = self.project_pass_rate(region, extra)
            results[region.name] = {
                "old": region.pass_rate,
                "new": round(new_rate, 1),
                "gain": round(new_rate - region.pass_rate, 1),
            }
        return results
