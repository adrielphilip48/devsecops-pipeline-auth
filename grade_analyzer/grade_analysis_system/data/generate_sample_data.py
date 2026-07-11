"""
generate_sample_data.py

Generates a synthetic (illustrative) dataset of secondary school exam
scores across five Tanzanian regions, for use with the Grade Analysis
System portfolio project.

NOTE: This data is SYNTHETIC. It is modelled loosely on documented
patterns (e.g. weaker average performance and lower pass rates in
under-resourced regions such as Tabora and Katavi, compared to
better-resourced regions such as Dar es Salaam) but the exact figures
are randomly generated for demonstration purposes only, not sourced
from NECTA. This is disclosed clearly in the README and should be
disclosed in any presentation of this project.
"""

import csv
import random

random.seed(42)

REGIONS = {
    # region: (mean_score, std_dev)  -- illustrative only
    "Dar es Salaam": (68, 12),
    "Dodoma": (58, 14),
    "Mwanza": (55, 15),
    "Tabora": (44, 16),
    "Katavi": (41, 17),
}

SUBJECTS = ["Mathematics", "English", "Physics", "Chemistry", "Biology"]
YEARS = [2022, 2023, 2024]
STUDENTS_PER_REGION_PER_YEAR = 24

FIRST_NAMES = ["Amani", "Baraka", "Chausiku", "Dotto", "Elizabeth", "Frank",
               "Grace", "Hamisi", "Irene", "John", "Kelvin", "Lightness",
               "Mariam", "Neema", "Omary", "Prisca", "Rehema", "Salum",
               "Tumaini", "Upendo", "Victor", "Winnie", "Yusuf", "Zainab"]


def clamp(value, low=0, high=100):
    return max(low, min(high, value))


def main():
    rows = []
    student_id = 1000

    for region, (mean, std) in REGIONS.items():
        for year in YEARS:
            for i in range(STUDENTS_PER_REGION_PER_YEAR):
                student_id += 1
                name = f"{random.choice(FIRST_NAMES)} S{student_id}"
                for subject in SUBJECTS:
                    # Slight per-subject variation
                    subject_shift = random.uniform(-4, 4)
                    score = round(clamp(random.gauss(mean + subject_shift, std)))
                    rows.append({
                        "student_id": student_id,
                        "name": name,
                        "region": region,
                        "year": year,
                        "subject": subject,
                        "score": score,
                    })

    with open("student_grades.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "name", "region", "year", "subject", "score"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows.")


if __name__ == "__main__":
    main()
