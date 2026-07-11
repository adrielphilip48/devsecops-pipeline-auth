"""
main.py

Demo entry point for the Student Grade Analysis System.
Run this to regenerate the report and all charts in output/.

    python3 main.py
"""

from grade_analyzer import GradeAnalyzer


def main():
    analyzer = GradeAnalyzer("data/student_grades.csv")

    print("\n--- Overall stats ---")
    print(analyzer.stats())

    print("\n--- Regional comparison (Mathematics only) ---")
    for region, stats in analyzer.compare_regions(subject="Mathematics").items():
        print(f"{region:15} {stats}")

    print("\n--- Grade distribution: Tabora, all years ---")
    print(analyzer.grade_distribution(region="Tabora"))

    print("\nGenerating report and charts in output/ ...")
    analyzer.generate_report("output/report.txt")
    analyzer.plot_regional_pass_rates("output/pass_rates_by_region.png")
    analyzer.plot_score_distribution("output/score_distribution.png")
    analyzer.plot_trend("output/pass_rate_trend.png")
    print("Done.")


if __name__ == "__main__":
    main()
