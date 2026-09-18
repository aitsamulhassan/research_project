"""Stage 8 figures. Each figure answers a stated research question."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

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
        "grid.alpha": 0.3,
    }
)


def figure1_cost_curve(rows: list[dict], selected_t: float, path_stem: Path) -> None:
    t = np.array([r["t_low"] for r in rows], dtype=float)
    cost = np.array([r["expected_normalized_cost"] for r in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.plot(t, cost, color="#1f77b4", linewidth=2)
    ax.axvline(selected_t, color="#d62728", linestyle="--", linewidth=1.2, label=f"selected t={selected_t:.2f}")
    ax.set_xlabel("Single threshold on calibrated default probability")
    ax.set_ylabel("Expected normalized cost (validation)")
    ax.set_title("Figure 1. Validation expected cost vs threshold")
    ax.grid(True)
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def figure2_cost_ratio(rows: list[dict], path_stem: Path) -> None:
    names = [r["scenario"] for r in rows]
    costs = [r["expected_normalized_cost"] for r in rows]
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.plot(range(len(names)), costs, marker="o", color="#d62728")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names)
    ax.set_xlabel("ASSUMED RELATIVE COST SCENARIO (FN:FP)")
    ax.set_ylabel("Selected expected normalized cost (validation)")
    ax.set_title("Figure 2. Cost-ratio sensitivity of selected policy")
    ax.grid(True)
    fig.tight_layout()
    _save(fig, path_stem)


def figure3_action_rates(rows: list[dict], path_stem: Path) -> None:
    names = [r["scenario"] for r in rows]
    approve = np.array([r["approval_rate"] for r in rows])
    review = np.array([r["review_rate"] for r in rows])
    reject = np.array([r["rejection_rate"] for r in rows])
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.bar(x, approve, label="APPROVE", color="#2ca02c")
    ax.bar(x, review, bottom=approve, label="HUMAN_REVIEW", color="#ffbf00")
    ax.bar(x, reject, bottom=approve + review, label="REJECT", color="#d62728")
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylabel("Share of validation applications")
    ax.set_xlabel("ASSUMED RELATIVE COST SCENARIO (FN:FP)")
    ax.set_title("Figure 3. Action mix by cost scenario (credit-only selected policy)")
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    _save(fig, path_stem)


def _bars_with_ci(ax, rows: list[dict], color: str) -> None:
    names = [r["band"] for r in rows]
    rates = [0.0 if r["default_rate"] != r["default_rate"] else r["default_rate"] for r in rows]
    lo = [0.0 if not r["n"] or r["default_rate"] != r["default_rate"] else r["default_rate"] - r["default_rate_ci_lower"] for r in rows]
    hi = [0.0 if not r["n"] or r["default_rate"] != r["default_rate"] else r["default_rate_ci_upper"] - r["default_rate"] for r in rows]
    ax.bar(names, rates, color=color, yerr=np.vstack([lo, hi]), capsize=4)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Observed default rate")


def figure4_default_by_band(credit_rows: list[dict], decision_rows: list[dict], path_stem: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4))
    _bars_with_ci(axes[0], credit_rows, "#1f77b4")
    axes[0].set_xlabel("Credit-risk band")
    axes[0].set_title("Calibrated-risk bands")
    _bars_with_ci(axes[1], decision_rows, "#ff7f0e")
    axes[1].set_xlabel("Fused policy action")
    axes[1].set_title("Simulated operational decision")
    fig.suptitle("Figure 4. Default rate by band (frozen test; Wilson 95% CI)")
    fig.tight_layout()
    _save(fig, path_stem)


def figure5_heatmap(index: list[str], columns: list[str], values: np.ndarray, path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    im = ax.imshow(values, cmap="Blues")
    ax.set_xticks(range(len(columns)))
    ax.set_xticklabels(columns, rotation=25, ha="right")
    ax.set_yticks(range(len(index)))
    ax.set_yticklabels(index)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            ax.text(j, i, f"{int(values[i, j])}", ha="center", va="center", fontsize=8)
    ax.set_title("Figure 5. Credit-risk band × governance status (test counts)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Count")
    fig.tight_layout()
    _save(fig, path_stem)


def _box(ax, xy, w, h, text, color, fontsize=8):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.015", facecolor=color, edgecolor="#222"
        )
    )
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)


def figure6_architecture(path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.4, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Figure 6. Evidence-separated decision architecture")
    _box(ax, (0.36, 0.88), 0.28, 0.08, "Application data", "#eeeeee")
    _box(ax, (0.04, 0.68), 0.28, 0.12, "Credit-risk model\n→ raw p → frozen Platt\n→ p_calibrated", "#cce5ff")
    _box(ax, (0.36, 0.68), 0.28, 0.12, "Explainability evidence\n(attribution; not an\nindependent approve rule)", "#d9ead3")
    _box(ax, (0.68, 0.68), 0.28, 0.12, "Shariah-oriented\ngovernance evidence\n(no numeric score)", "#ffe8cc")
    _box(ax, (0.22, 0.42), 0.56, 0.16, "Final decision policy\n(hard constraints + cost-sensitive bands)\nAPPROVE / HUMAN_REVIEW / REJECT", "#e2d5f1")
    _box(ax, (0.08, 0.18), 0.24, 0.12, "APPROVE", "#c6efce")
    _box(ax, (0.38, 0.18), 0.24, 0.12, "HUMAN_REVIEW\n(simulated band)", "#fff2cc")
    _box(ax, (0.68, 0.18), 0.24, 0.12, "REJECT", "#f4cccc")
    _box(ax, (0.36, 0.03), 0.28, 0.10, "Audit record", "#d0e0e3")
    ax.annotate("", xy=(0.18, 0.80), xytext=(0.45, 0.88), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.80), xytext=(0.50, 0.88), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.82, 0.80), xytext=(0.55, 0.88), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.58), xytext=(0.18, 0.68), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.58), xytext=(0.50, 0.68), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.58), xytext=(0.82, 0.68), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.20, 0.30), xytext=(0.40, 0.42), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.30), xytext=(0.50, 0.42), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.80, 0.30), xytext=(0.60, 0.42), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(0.50, 0.13), xytext=(0.50, 0.18), arrowprops=dict(arrowstyle="->"))
    fig.tight_layout()
    _save(fig, path_stem)


def figure7_audit_lifecycle(path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.4, 3.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Figure 7. Audit-trail lifecycle")
    steps = [
        (0.02, "Frozen\ninputs"),
        (0.22, "Evidence\nlayers"),
        (0.42, "Policy\nevaluation"),
        (0.62, "Logic hash\n(decision_id)"),
        (0.82, "Event\ntimestamp"),
    ]
    for x, text in steps:
        _box(ax, (x, 0.35), 0.16, 0.32, text, "#d9edf7", fontsize=9)
    for x in (0.18, 0.38, 0.58, 0.78):
        ax.annotate("", xy=(x + 0.04, 0.51), xytext=(x, 0.51), arrowprops=dict(arrowstyle="->"))
    ax.text(0.5, 0.12, "Timestamp is attached after logic hashing and cannot change the decision.", ha="center", fontsize=9)
    fig.tight_layout()
    _save(fig, path_stem)
