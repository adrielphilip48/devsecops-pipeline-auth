"""
build_dataset.py

Builds a student-level dataset for the Pass/Fail Predictor, combining:
  - individual exam scores (as in the Grade Analysis System project)
  - region-level resourcing and teacher-retention features (as in the
    Resource Allocation Simulator project)

This is the dataset a classifier can learn from: for each student result,
it has both the outcome (pass/fail) and the two candidate explanatory
factors at the heart of my EPQ -- funding per pupil and teacher
attrition -- plus subject and year as controls.

NOTE: Synthetic/illustrative data, consistent with the other two
portfolio projects. See README.md.
"""

import csv
import random

random.seed(42)

# region: (mean_score, std_dev, funding_per_pupil, teacher_attrition)
REGIONS = {
    "Dar es Salaam": (68, 12, 120_000, 0.05),
    "Dodoma":        (58, 14, 95_000,  0.10),
    "Mwanza":        (55, 15, 80_000,  0.15),
    "Tabora":        (44, 16, 55_000,  0.28),
    "Katavi":        (41, 17, 45_000,  0.35),
}

SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]
YEARS = [2022, 2023, 2024]
STUDENTS_PER_REGION_PER_YEAR = 24
PASS_MARK = 40


def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def main():
    rows = []
    student_id = 1000

    for region, (mean, std, funding, attrition) in REGIONS.items():
        for year in YEARS:
            for _ in range(STUDENTS_PER_REGION_PER_YEAR):
                student_id += 1
                for subject in SUBJECTS:
                    subject_shift = random.uniform(-4, 4)
                    score = round(clamp(random.gauss(mean + subject_shift, std)))
                    rows.append({
                        "student_id": student_id,
                        "region": region,
                        "year": year,
                        "subject": subject,
                        "funding_per_pupil": funding,
                        "teacher_attrition": attrition,
                        "score": score,
                        "passed": int(score >= PASS_MARK),
                    })

    fieldnames = ["student_id", "region", "year", "subject", "funding_per_pupil",
                  "teacher_attrition", "score", "passed"]
    with open("student_features.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows.")


if __name__ == "__main__":
    main()
