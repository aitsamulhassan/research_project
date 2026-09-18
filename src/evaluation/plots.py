"""Publication-style ROC/PR plots. No axis manipulation to inflate appearance."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import auc, average_precision_score

from evaluation.metrics import pr_curve_points, roc_curve_points

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
    }
)

MODEL_STYLE = {
    "logistic_regression": {"label": "Logistic regression", "color": "#1f77b4"},
    "random_forest": {"label": "Random forest", "color": "#ff7f0e"},
    "xgboost": {"label": "XGBoost", "color": "#2ca02c"},
    "explainable_boosting_machine": {"label": "EBM", "color": "#d62728"},
}


def _save(fig: plt.Figure, path_stem: Path) -> None:
    path_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path_stem.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def plot_roc(series: dict[str, tuple[np.ndarray, np.ndarray]], title: str, path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    ax.plot([0, 1], [0, 1], color="0.6", linestyle="--", linewidth=1, label="Chance")
    for name, (y, p) in series.items():
        fpr, tpr = roc_curve_points(y, p)
        style = MODEL_STYLE[name]
        ax.plot(fpr, tpr, color=style["color"], linewidth=2, label=f"{style['label']} (AUC={auc(fpr, tpr):.3f})")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title(title)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="lower right", frameon=False)
    ax.set_aspect("equal", adjustable="box")
    _save(fig, path_stem)


def plot_pr(series: dict[str, tuple[np.ndarray, np.ndarray]], title: str, path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    for name, (y, p) in series.items():
        recall, precision = pr_curve_points(y, p)
        style = MODEL_STYLE[name]
        ap = float(average_precision_score(y, p))
        ax.plot(recall, precision, color=style["color"], linewidth=2, label=f"{style['label']} (AP={ap:.3f})")
    prevalence = float(np.mean(next(iter(series.values()))[0]))
    ax.axhline(prevalence, color="0.6", linestyle="--", linewidth=1, label=f"Prevalence={prevalence:.3f}")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(title)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="best", frameon=False)
    _save(fig, path_stem)


def plot_temporal(rows: list[dict], path_stem: Path) -> None:
    years = sorted({r["year"] for r in rows})
    models = list(MODEL_STYLE.keys())
    metrics = ["roc_auc", "pr_auc", "brier"]
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.0), sharex=True)
    x = np.arange(len(years))
    width = 0.18
    for ax, metric in zip(axes, metrics):
        for i, model in enumerate(models):
            vals = []
            for year in years:
                match = [r[metric] for r in rows if r["model"] == model and r["year"] == year]
                vals.append(match[0] if match else np.nan)
            ax.bar(
                x + (i - 1.5) * width,
                vals,
                width=width,
                color=MODEL_STYLE[model]["color"],
                label=MODEL_STYLE[model]["label"],
            )
        ax.set_xticks(x)
        ax.set_xticklabels([str(y) for y in years])
        titles = {"roc_auc": "ROC-AUC", "pr_auc": "PR-AUC", "brier": "Brier"}
        ax.set_title(titles[metric])
        if metric != "brier":
            ax.set_ylim(0, 1)
        ax.set_xlabel("Test calendar year")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 0.02))
    fig.suptitle("Test performance by calendar year (descriptive; not used for tuning)")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    _save(fig, path_stem)
