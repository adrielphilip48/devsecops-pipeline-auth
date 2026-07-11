# Student Grade Analysis System

A Python tool for analysing exam-score data — built to explore how academic
performance varies across regions, subjects, and years, and to support the
data-analysis stage of my EPQ research project on resource disparities and
teacher retention in Tanzania's national education system.

## What it does

- Loads student exam records (region, year, subject, score) from CSV
- Computes core statistics: mean, median, mode, standard deviation, pass rate
- Converts numeric scores to letter grades (A–F) using configurable boundaries
- Compares performance across regions and tracks pass-rate trends over time
- Generates visualisations: regional pass-rate bar chart, score-distribution
  box plot, and a multi-year trend line chart
- Produces a plain-text summary report

## Design

The system is built around two small classes:

- `GradeRecord` — an immutable record of one student's result in one subject/year
- `GradeAnalyzer` — loads a CSV of records and exposes filtering, statistics,
  and plotting methods (`stats()`, `compare_regions()`, `trend_over_years()`,
  `plot_regional_pass_rates()`, etc.)

Filtering by region, subject, and year is handled by a single internal
`_filter()` method, so every statistic and every chart can be generated for
any combination (e.g. "Mathematics results in Tabora in 2023") without
duplicating logic.

## A note on the data

`data/student_grades.csv` is **synthetic, illustrative data** (see
`data/generate_sample_data.py`), generated to loosely reflect a documented
pattern: under-resourced regions such as Tabora and Katavi tend to show
lower average scores and pass rates than better-resourced regions such as
Dar es Salaam. The exact numbers are not drawn from real NECTA statistics —
this project demonstrates the analysis pipeline I plan to apply to genuine
regional exam data during my EPQ.

## Running it

```bash
pip install pandas numpy matplotlib   # if not already installed
python3 main.py
```

Outputs are written to `output/`: `report.txt` and three PNG charts.

## Example output

Overall (synthetic) dataset: 1,800 records across 5 regions, 5 subjects, 3 years.

| Region         | Mean score | Pass rate |
|----------------|-----------:|----------:|
| Dar es Salaam  | 67.9       | 99.2%     |
| Dodoma         | 58.0       | 91.4%     |
| Mwanza         | 55.2       | 81.4%     |
| Tabora         | 43.4       | 59.2%     |
| Katavi         | 41.0       | 53.6%     |

## Possible extensions

- Replace synthetic data with real NECTA/regional statistics
- Add a simple regression to test correlation between pupil-teacher ratio
  and pass rate directly within the tool
- Export results to a formatted PDF/Word summary
