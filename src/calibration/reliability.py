"""Reliability diagrams. Axes are always [0, 1] x [0, 1]."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from calibration.metrics import reliability_table
from evaluation.plots import _save

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

METHOD_STYLE = {
    "raw": {"label": "RAW", "color": "#4d4d4d"},
    "platt": {"label": "Platt", "color": "#1f77b4"},
    "isotonic": {"label": "Isotonic", "color": "#d62728"},
}


def _points(y: np.ndarray, p: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs, ys, ns = [], [], []
    for row in reliability_table(y, p):
        if row["empty"]:
            continue
        xs.append(row["mean_predicted"])
        ys.append(row["observed_rate"])
        ns.append(row["n"])
    return np.asarray(xs), np.asarray(ys), np.asarray(ns)


def plot_reliability_panels(
    series: dict[str, tuple[np.ndarray, np.ndarray]],
    title: str,
    path_stem: Path,
    methods: list[str] | None = None,
) -> None:
    methods = methods or list(series.keys())
    fig, axes = plt.subplots(1, len(methods), figsize=(4.2 * len(methods), 4.2), sharey=True)
    if len(methods) == 1:
        axes = [axes]
    for ax, name in zip(axes, methods):
        y, p = series[name]
        x, obs, n = _points(y, p)
        style = METHOD_STYLE[name]
        sizes = 40 + 80 * (n / n.max())
        ax.plot([0, 1], [0, 1], color="0.6", linestyle="--", linewidth=1, label="Perfect")
        ax.scatter(x, obs, s=sizes, color=style["color"], zorder=3, label=style["label"])
        ax.plot(x, obs, color=style["color"], linewidth=1.5)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("Mean predicted probability")
        ax.set_title(style["label"])
        ax.legend(loc="upper left", frameon=False, fontsize=8)
    axes[0].set_ylabel("Observed default rate")
    fig.suptitle(title)
    fig.tight_layout()
    _save(fig, path_stem)


def plot_reliability_overlay(
    series: dict[str, tuple[np.ndarray, np.ndarray]],
    title: str,
    path_stem: Path,
    methods: list[str],
) -> None:
    fig, ax = plt.subplots(figsize=(5.4, 5.2))
    ax.plot([0, 1], [0, 1], color="0.6", linestyle="--", linewidth=1, label="Perfect")
    for name in methods:
        y, p = series[name]
        x, obs, n = _points(y, p)
        style = METHOD_STYLE[name]
        ax.plot(x, obs, color=style["color"], marker="o", linewidth=2, label=style["label"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed default rate")
    ax.set_title(title)
    ax.legend(loc="upper left", frameon=False)
    _save(fig, path_stem)


def plot_brier_comparison(val_rows: list[dict], test_rows: list[dict], path_stem: Path) -> None:
    methods = ["raw", "platt", "isotonic"]
    labels = [METHOD_STYLE[m]["label"] for m in methods]
    val_b = [next(r["brier"] for r in val_rows if r["method"] == m) for m in methods]
    test_b = [next(r["brier"] for r in test_rows if r["method"] == m) for m in methods]
    x = np.arange(len(methods))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.bar(x - width / 2, val_b, width, color="#9ecae1", label="Validation (selection)")
    ax.bar(x + width / 2, test_b, width, color="#3182bd", label="Test (reporting only)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Brier score (lower is better)")
    ax.set_title("Brier score by calibration method")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def plot_risk_range_gaps(rows: list[dict], path_stem: Path) -> None:
    methods = ["raw", "platt", "isotonic"]
    ranges = sorted({(r["range_left"], r["range_right"], r["range_label"]) for r in rows if r["method"] == "raw"})
    labels = [item[2] for item in ranges]
    x = np.arange(len(ranges))
    width = 0.24
    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.axhline(0, color="0.5", linewidth=1)
    for i, method in enumerate(methods):
        gaps = []
        for left, right, _ in ranges:
            match = [
                r["gap"]
                for r in rows
                if r["method"] == method and r["range_left"] == left and r["range_right"] == right
            ]
            gaps.append(match[0] if match and match[0] is not None else np.nan)
        ax.bar(
            x + (i - 1) * width,
            gaps,
            width,
            color=METHOD_STYLE[method]["color"],
            label=METHOD_STYLE[method]["label"],
        )
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Predicted-probability range")
    ax.set_ylabel("Observed rate − mean predicted")
    ax.set_title("Test calibration gap by probability range (not used for thresholds)")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def plot_temporal(rows: list[dict], path_stem: Path) -> None:
    years = [2017, 2018]
    methods = ["raw", "platt", "isotonic"]
    metrics = ["brier", "log_loss", "ece"]
    titles = {"brier": "Brier", "log_loss": "Log loss", "ece": "ECE"}
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.2), sharex=True)
    x = np.arange(len(years))
    width = 0.24
    for ax, metric in zip(axes, metrics):
        for i, method in enumerate(methods):
            vals = []
            for year in years:
                match = [r[metric] for r in rows if r["method"] == method and r["year"] == year]
                vals.append(match[0] if match else np.nan)
            ax.bar(
                x + (i - 1) * width,
                vals,
                width,
                color=METHOD_STYLE[method]["color"],
                label=METHOD_STYLE[method]["label"],
            )
        ax.set_xticks(x)
        ax.set_xticklabels([str(y) for y in years])
        ax.set_title(titles[metric])
        ax.set_xlabel("Test calendar year")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.02))
    fig.suptitle("Temporal calibration (descriptive; not used for tuning)")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    _save(fig, path_stem)
