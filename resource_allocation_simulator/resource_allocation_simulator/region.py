"""
region.py

Data model for a single education region used in the Resource Allocation
Simulator. Figures are illustrative/synthetic (see README) but modelled
on the same regional pattern used in the Grade Analysis System project:
Tabora and Katavi under-resourced with high teacher attrition, Dar es
Salaam well-resourced with low attrition.
"""

from dataclasses import dataclass


@dataclass
class Region:
    name: str
    students: int                  # number of enrolled students
    funding_per_pupil: float       # current annual funding per pupil (TZS)
    pass_rate: float               # current exam pass rate (%)
    teacher_attrition: float       # current annual teacher attrition rate (0-1)

    @property
    def retention_rate(self) -> float:
        """Fraction of teachers retained each year (1 - attrition)."""
        return 1 - self.teacher_attrition


# The five regions used throughout this project, consistent with the
# Grade Analysis System dataset.
DEFAULT_REGIONS = [
    Region("Dar es Salaam", students=15000, funding_per_pupil=120_000, pass_rate=99.2, teacher_attrition=0.05),
    Region("Dodoma",        students=12000, funding_per_pupil=95_000,  pass_rate=91.4, teacher_attrition=0.10),
    Region("Mwanza",        students=20000, funding_per_pupil=80_000,  pass_rate=81.4, teacher_attrition=0.15),
    Region("Tabora",        students=9000,  funding_per_pupil=55_000,  pass_rate=59.2, teacher_attrition=0.28),
    Region("Katavi",        students=4000,  funding_per_pupil=45_000,  pass_rate=53.6, teacher_attrition=0.35),
]
