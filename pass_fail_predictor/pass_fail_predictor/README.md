# Pass/Fail Predictor

A machine learning project that predicts whether a student passes an
exam using region-level resourcing (funding per pupil) and teacher
retention as the key features — a third, independent way of testing
the same question at the heart of my EPQ, this time using predictive
modelling rather than descriptive statistics (Grade Analysis System) or
simulation (Resource Allocation Simulator).

## What it does

- Builds a student-level dataset combining exam outcomes with two
  region-level features: `funding_per_pupil` and `teacher_retention`
  (plus subject and year as controls)
- Trains two classifiers — **Logistic Regression** and a **Decision
  Tree** — to predict pass/fail
- Compares which feature carries more predictive weight in each model
- Evaluates both models with accuracy, confusion matrices, and ROC curves

## Design

- `data/build_dataset.py` — generates the combined student-level dataset
- `predictor.py` — `PassFailPredictor` class: feature preparation, model
  training, evaluation
- `main.py` — runs everything, writes the report and three charts

## The key finding (and why it matters more than it first looks)

The two models **disagree** on which factor matters more:

- **Logistic Regression** ranks `funding_per_pupil` as the strongest
  predictor, with `teacher_retention` actually showing a small
  *negative* coefficient.
- **Decision Tree** ranks `teacher_retention` as by far the dominant
  feature (importance ≈ 0.91), with funding barely registering.

At first glance this looks like a contradiction. It isn't — it's
**multicollinearity**: in this dataset, funding and teacher retention
both move together region by region (well-funded regions also happen
to retain teachers better), so a linear model struggles to credit the
right one; a small change in the data can flip which variable "gets
the credit." The decision tree, which splits on thresholds rather than
fitting a single linear weight, is less confused by this and leans
heavily on teacher retention instead.

**This is a genuinely useful result for my EPQ, not just a modelling
artifact.** It shows precisely why resourcing and teacher retention are
hard to disentangle using observational data — they're confounded in
practice — and it strengthens the case for looking at regions where
the two factors diverge (e.g. a well-funded region with high teacher
turnover, or vice versa) rather than relying on a single model's
feature ranking as a verdict.

## A note on the data

The dataset is synthetic, built the same way as in the other two
projects (see `data/build_dataset.py`) — not real NECTA/PO-RALG data.
Because funding and retention are constructed together per region here,
some of the collinearity described above is inherited from how the data
was generated. With real, more granular data (e.g. district-level rather
than regional-level, where funding and retention don't always move
together), this ambiguity should be easier to resolve.

## Running it

```bash
pip install pandas numpy matplotlib scikit-learn
cd data && python3 build_dataset.py && cd ..
python3 main.py
```

Outputs are written to `output/`: `report.txt` and three PNG charts
(confusion matrices, feature importance comparison, ROC curves).

## Possible extensions

- Use real, district-level data where funding and retention vary more
  independently, to properly separate their effects
- Add regularisation (e.g. Ridge/Lasso logistic regression) to see if
  it stabilises the coefficient sign
- Try a random forest or gradient-boosted model for a third opinion
