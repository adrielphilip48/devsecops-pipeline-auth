# Resource Allocation Simulator

A Python simulation that models how a fixed pool of additional education
funding could be distributed across regions under different allocation
rules, and projects the effect on exam pass rates — built as a companion
piece to my Grade Analysis System, and to explore the "resourcing" side of
my EPQ research question directly through code.

## The core idea

It's tempting to assume that giving under-resourced regions more money
automatically closes the achievement gap. This simulator tests that
assumption using a simple economic model: **funding effectiveness is
scaled by teacher retention.** A region that keeps losing trained
teachers gets a smaller pass-rate improvement from the same extra
shilling per pupil than a region with a stable teaching staff. This
is the central claim my EPQ investigates — this project turns it into
a testable, quantified model.

```
pass_rate_gain = K * sqrt(extra_funding_per_pupil) * teacher_retention_rate
```

- `sqrt()` gives diminishing returns — consistent with standard economic
  reasoning about marginal returns to investment (the first extra funding
  matters far more than the last).
- Multiplying by retention rate means the same funding produces a smaller
  gain in high-attrition regions like Tabora and Katavi.
- Gains are capped at 100%.

This is a deliberately simple, illustrative model — not a validated
econometric one — designed to generate a concrete, testable claim rather
than just a static comparison.

## Allocation strategies compared

| Strategy | Rule |
|---|---|
| Equal split | Every region gets the same extra amount per pupil |
| Enrollment-weighted | Budget split in proportion to student numbers (efficiency-oriented) |
| Needs-weighted | Budget split in proportion to the current funding gap (equity-oriented) |
| Hybrid (50/50) | A blend of enrollment-weighted and needs-weighted |

## Design

- `region.py` — `Region` dataclass (students, funding per pupil, pass rate, teacher attrition)
- `allocator.py` — `BudgetAllocator` class implementing the four strategies
- `impact_model.py` — `ImpactModel` class implementing the diminishing-returns projection
- `main.py` — runs all four strategies, prints/writes a report, and generates three charts

## Result (with the synthetic data provided)

Needs-weighted allocation produces both the **highest average pass-rate
gain** (+6.44pp) and the **lowest post-allocation inequality** (stdev
15.76) — beating the enrollment-weighted approach on both efficiency and
equity, despite sending the least money to the best-performing region.
This is the kind of finding I want to test against real data in my EPQ.

## A note on the data

Regional figures (funding per pupil, pass rates, teacher attrition) are
synthetic and consistent with the pattern used in the Grade Analysis
System project — not drawn from real government data. Both projects are
built so real regional statistics (e.g. from PO-RALG, NECTA, MoEST) could
be substituted in directly without changing the code.

## Running it

```bash
pip install matplotlib
python3 main.py
```

Outputs are written to `output/`: `report.txt` and three PNG charts.

## Possible extensions

- Replace synthetic figures with real regional budget and attrition data
- Add a budget-constrained optimizer that finds the allocation maximising
  average gain subject to a maximum-inequality constraint
- Model multi-year effects (e.g. compounding retention improvements)
