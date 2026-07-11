"""
main.py

Pass/Fail Predictor
--------------------
Trains machine learning models to predict exam pass/fail from region-level
resourcing (funding per pupil) and teacher-retention data, and compares
which factor carries more predictive weight -- a third, independent lens
on the same question explored in the Grade Analysis System (descriptive
statistics) and the Resource Allocation Simulator (simulation).

Run:
    python3 main.py
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc

from predictor import PassFailPredictor


def plot_confusion_matrices(results, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, (model_name, result) in zip(axes, results.items()):
        cm = result["confusion_matrix"]
        im = ax.imshow(cm, cmap="Blues")
        ax.set_title(f"{model_name}\nAccuracy: {result['accuracy']*100:.1f}%")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Fail", "Pass"])
        ax.set_yticklabels(["Fail", "Pass"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                        color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=12)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_feature_importance(results, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    for ax, (model_name, result) in zip(axes, results.items()):
        importance = result["importance"]
        names = list(importance.keys())
        values = list(importance.values())

        # sort by absolute value, descending
        order = np.argsort(np.abs(values))[::-1]
        names = [names[i] for i in order]
        values = [values[i] for i in order]

        colors = ["#1F4E5F" if v >= 0 else "#C6484E" for v in values]
        ax.barh(names, values, color=colors)
        ax.set_title(f"{model_name}: Feature Importance")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_roc_curves(results, out_path):
    fig, ax = plt.subplots(figsize=(6, 5.5))
    colors = {"Logistic Regression": "#1F4E5F", "Decision Tree": "#C6484E"}

    for model_name, result in results.items():
        fpr, tpr, _ = roc_curve(result["y_test"], result["y_proba"])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, label=f"{model_name} (AUC={roc_auc:.2f})",
                color=colors.get(model_name))

    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=0.8)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves: Predicting Pass/Fail")
    ax.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


def write_report(results, out_path):
    lines = ["PASS/FAIL PREDICTOR REPORT", "=" * 50, ""]

    for model_name, result in results.items():
        lines.append(f"--- {model_name} ---")
        lines.append(f"Accuracy: {result['accuracy']*100:.2f}%")
        lines.append("")
        lines.append("Feature importance (sorted by absolute weight):")
        importance = sorted(result["importance"].items(), key=lambda x: abs(x[1]), reverse=True)
        for name, value in importance:
            lines.append(f"  {name:25} {value:+.4f}")
        lines.append("")
        lines.append("Classification report:")
        lines.append(result["report"])
        lines.append("")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))

    print("\n".join(lines))


def main():
    predictor = PassFailPredictor("data/student_features.csv")
    results = predictor.train_and_evaluate()

    write_report(results, "output/report.txt")
    plot_confusion_matrices(results, "output/confusion_matrices.png")
    plot_feature_importance(results, "output/feature_importance.png")
    plot_roc_curves(results, "output/roc_curves.png")
    print("\nReport and charts written to output/")


if __name__ == "__main__":
    main()
