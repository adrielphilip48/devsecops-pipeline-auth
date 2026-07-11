"""
grade_analyzer.py

A Student Grade Analysis System.

Loads exam-score records (student, region, year, subject, score) and
provides statistical analysis and visualization tools to investigate
patterns in academic performance -- in particular, regional disparities
that may relate to differences in school resourcing and teacher
retention (the theme of my EPQ research project).

Author: Phx
"""

from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt


PASS_MARK = 40  # NECTA-style pass threshold used for this project (illustrative)

GRADE_BOUNDARIES = [
    (75, "A"),
    (65, "B"),
    (50, "C"),
    (PASS_MARK, "D"),
    (0, "F"),
]


def score_to_grade(score: float) -> str:
    """Convert a numeric score to a letter grade using GRADE_BOUNDARIES."""
    for threshold, grade in GRADE_BOUNDARIES:
        if score >= threshold:
            return grade
    return "F"


@dataclass(frozen=True)
class GradeRecord:
    """A single exam result for one student, in one subject, one year."""
    student_id: int
    name: str
    region: str
    year: int
    subject: str
    score: float

    @property
    def grade(self) -> str:
        return score_to_grade(self.score)

    @property
    def passed(self) -> bool:
        return self.score >= PASS_MARK


class GradeAnalyzer:
    """
    Loads grade data from CSV and provides analysis and plotting methods.

    Typical usage:
        analyzer = GradeAnalyzer("data/student_grades.csv")
        analyzer.summary()
        analyzer.plot_regional_pass_rates("output/pass_rates.png")
    """

    def __init__(self, csv_path: str | Path):
        self.records: list[GradeRecord] = []
        self._load(csv_path)

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    def _load(self, csv_path: str | Path) -> None:
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.records.append(GradeRecord(
                    student_id=int(row["student_id"]),
                    name=row["name"],
                    region=row["region"],
                    year=int(row["year"]),
                    subject=row["subject"],
                    score=float(row["score"]),
                ))

    # ------------------------------------------------------------------
    # Filtering helper
    # ------------------------------------------------------------------
    def _filter(self, region: Optional[str] = None, subject: Optional[str] = None,
                year: Optional[int] = None) -> list[GradeRecord]:
        records = self.records
        if region is not None:
            records = [r for r in records if r.region == region]
        if subject is not None:
            records = [r for r in records if r.subject == subject]
        if year is not None:
            records = [r for r in records if r.year == year]
        return records

    # ------------------------------------------------------------------
    # Core statistics
    # ------------------------------------------------------------------
    def stats(self, region: Optional[str] = None, subject: Optional[str] = None,
               year: Optional[int] = None) -> dict:
        """Return mean, median, mode, standard deviation and pass rate."""
        records = self._filter(region, subject, year)
        scores = [r.score for r in records]

        if not scores:
            return {"n": 0}

        pass_rate = sum(1 for r in records if r.passed) / len(records) * 100

        return {
            "n": len(scores),
            "mean": round(statistics.mean(scores), 2),
            "median": statistics.median(scores),
            "mode": statistics.mode(scores),
            "stdev": round(statistics.stdev(scores), 2) if len(scores) > 1 else 0.0,
            "pass_rate": round(pass_rate, 1),
        }

    def grade_distribution(self, region: Optional[str] = None, subject: Optional[str] = None,
                            year: Optional[int] = None) -> dict:
        """Return counts of each letter grade (A-F) for the filtered records."""
        records = self._filter(region, subject, year)
        dist = {grade: 0 for _, grade in GRADE_BOUNDARIES}
        for r in records:
            dist[r.grade] += 1
        return dist

    def compare_regions(self, subject: Optional[str] = None, year: Optional[int] = None) -> dict:
        """Return {region: stats_dict} for every region present in the data."""
        regions = sorted({r.region for r in self.records})
        return {region: self.stats(region=region, subject=subject, year=year) for region in regions}

    def trend_over_years(self, region: Optional[str] = None, subject: Optional[str] = None) -> dict:
        """Return {year: pass_rate} to show change over time."""
        years = sorted({r.year for r in self.records})
        return {year: self.stats(region=region, subject=subject, year=year)["pass_rate"] for year in years}

    # ------------------------------------------------------------------
    # Visualizations
    # ------------------------------------------------------------------
    def plot_regional_pass_rates(self, out_path: str | Path, year: Optional[int] = None) -> None:
        comparison = self.compare_regions(year=year)
        regions = list(comparison.keys())
        pass_rates = [comparison[r]["pass_rate"] for r in regions]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(regions, pass_rates, color="#1F4E5F")
        ax.set_ylabel("Pass rate (%)")
        title = f"Pass Rate by Region" + (f" ({year})" if year else " (all years)")
        ax.set_title(title)
        ax.set_ylim(0, 100)
        for bar, rate in zip(bars, pass_rates):
            ax.text(bar.get_x() + bar.get_width() / 2, rate + 1.5, f"{rate}%",
                    ha="center", fontsize=9)
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

    def plot_score_distribution(self, out_path: str | Path) -> None:
        regions = sorted({r.region for r in self.records})
        data = [[r.score for r in self.records if r.region == region] for region in regions]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot(data, tick_labels=regions, patch_artist=True,
                   boxprops=dict(facecolor="#EAF1F3"))
        ax.axhline(PASS_MARK, color="#B22222", linestyle="--", linewidth=1, label=f"Pass mark ({PASS_MARK})")
        ax.set_ylabel("Score")
        ax.set_title("Score Distribution by Region (all subjects, all years)")
        ax.legend()
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

    def plot_trend(self, out_path: str | Path) -> None:
        regions = sorted({r.region for r in self.records})
        years = sorted({r.year for r in self.records})

        fig, ax = plt.subplots(figsize=(8, 5))
        for region in regions:
            rates = [self.stats(region=region, year=year)["pass_rate"] for year in years]
            ax.plot(years, rates, marker="o", label=region)

        ax.set_xlabel("Year")
        ax.set_ylabel("Pass rate (%)")
        ax.set_title("Pass Rate Trend by Region (2022-2024)")
        ax.set_xticks(years)
        ax.legend(loc="upper left", fontsize=8)
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close(fig)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def generate_report(self, out_path: str | Path) -> None:
        lines = ["STUDENT GRADE ANALYSIS REPORT", "=" * 40, ""]

        overall = self.stats()
        lines.append("Overall statistics (all regions, subjects, years):")
        for key, value in overall.items():
            lines.append(f"  {key:10}: {value}")
        lines.append("")

        lines.append("Regional comparison (all subjects, all years):")
        for region, s in self.compare_regions().items():
            lines.append(f"  {region:15} n={s['n']:<5} mean={s['mean']:<6} "
                          f"stdev={s['stdev']:<6} pass_rate={s['pass_rate']}%")
        lines.append("")

        lines.append("Pass rate trend by year (all regions combined):")
        for year, rate in self.trend_over_years().items():
            lines.append(f"  {year}: {rate}%")

        with open(out_path, "w") as f:
            f.write("\n".join(lines))

        print("\n".join(lines))


if __name__ == "__main__":
    analyzer = GradeAnalyzer("data/student_grades.csv")
    analyzer.generate_report("output/report.txt")
    analyzer.plot_regional_pass_rates("output/pass_rates_by_region.png")
    analyzer.plot_score_distribution("output/score_distribution.png")
    analyzer.plot_trend("output/pass_rate_trend.png")
