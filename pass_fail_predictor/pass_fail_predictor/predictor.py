"""
predictor.py

Trains classifiers to predict whether a student passes an exam, using
region-level resourcing (funding per pupil) and teacher-retention
(1 - attrition) as the two key candidate features, alongside subject
and year as controls.

The purpose isn't just prediction accuracy -- it's using feature
importance / coefficients to answer, in a third and independent way,
the same question my EPQ investigates: does funding or teacher
retention carry more predictive weight for exam outcomes?

Two models are trained so the answer can be cross-checked between a
linear model and a non-linear one:
    - Logistic Regression  (coefficients show direction + relative weight)
    - Decision Tree         (feature_importances_ show relative weight,
                              can capture non-linear/threshold effects)
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report, roc_curve, auc,
)


class PassFailPredictor:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.df["teacher_retention"] = 1 - self.df["teacher_attrition"]
        self.feature_names: list[str] = []
        self.models = {}
        self.results = {}

    # ------------------------------------------------------------------
    def prepare_features(self):
        df = self.df.copy()

        # One-hot encode subject (drop first to avoid redundancy)
        subject_dummies = pd.get_dummies(df["subject"], prefix="subject", drop_first=True)

        X = pd.concat([
            df[["funding_per_pupil", "teacher_retention", "year"]],
            subject_dummies,
        ], axis=1)
        y = df["passed"]

        self.feature_names = list(X.columns)
        return X, y

    # ------------------------------------------------------------------
    def train_and_evaluate(self, test_size: float = 0.25, random_state: int = 42):
        X, y = self.prepare_features()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # --- Logistic Regression ---
        logreg = LogisticRegression(max_iter=1000)
        logreg.fit(X_train_scaled, y_train)
        logreg_pred = logreg.predict(X_test_scaled)
        logreg_proba = logreg.predict_proba(X_test_scaled)[:, 1]

        self.models["Logistic Regression"] = logreg
        self.results["Logistic Regression"] = {
            "accuracy": accuracy_score(y_test, logreg_pred),
            "confusion_matrix": confusion_matrix(y_test, logreg_pred),
            "report": classification_report(y_test, logreg_pred, zero_division=0),
            "y_test": y_test,
            "y_proba": logreg_proba,
            "importance": dict(zip(self.feature_names, logreg.coef_[0])),
        }

        # --- Decision Tree ---
        tree = DecisionTreeClassifier(max_depth=4, random_state=random_state)
        tree.fit(X_train, y_train)  # trees don't need scaling
        tree_pred = tree.predict(X_test)
        tree_proba = tree.predict_proba(X_test)[:, 1]

        self.models["Decision Tree"] = tree
        self.results["Decision Tree"] = {
            "accuracy": accuracy_score(y_test, tree_pred),
            "confusion_matrix": confusion_matrix(y_test, tree_pred),
            "report": classification_report(y_test, tree_pred, zero_division=0),
            "y_test": y_test,
            "y_proba": tree_proba,
            "importance": dict(zip(self.feature_names, tree.feature_importances_)),
        }

        return self.results
