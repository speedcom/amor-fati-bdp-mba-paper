#!/usr/bin/env python3
"""Generate the lambda robustness figure for the MBA BDP paper."""

from __future__ import annotations

import csv
import os
from pathlib import Path
from statistics import mean, stdev


PAPER_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = Path(__file__).resolve().parents[2]
MC_DIR = REPO_DIR / "mc"
FIGURES_DIR = PAPER_DIR / "latex" / "figures"
DATA_DIR = PAPER_DIR / "latex" / "data"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("MPLCONFIGDIR", str(PAPER_DIR / ".mplconfig"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BDP_LEVELS = [0, 500, 1000, 1500, 2000, 2500, 3000]
LAMBDA_SPECS = [
    ("000", 0.00, "#4d4d4d", "o"),
    ("025", 0.25, "#1f77b4", "s"),
    ("050", 0.50, "#2ca02c", "^"),
    ("075", 0.75, "#ff7f0e", "D"),
    ("100", 1.00, "#d62728", "v"),
]
METRICS = [
    "TotalAdoption",
    "AutoRatio",
    "HybridRatio",
    "PrivateGrossInvestmentToGdp",
    "Inflation",
    "RefRate",
    "MarketWage",
    "Unemployment",
    "DebtToGdp",
    "DeficitToGdp",
]


plt.rcParams.update(
    {
        "figure.dpi": 220,
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
        "font.size": 10.5,
        "axes.titlesize": 12,
        "axes.labelsize": 10.5,
        "legend.fontsize": 8.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "-",
    }
)


def pct(value: float) -> float:
    return value * 100.0


def seed_files(tag: str, level: int) -> list[Path]:
    if level == 0:
        pattern = "robust-bdp-0000_robust-bdp-0000-60m-10s_60m_seed*.csv"
    else:
        pattern = f"robust-l{tag}-bdp-{level}_robust-l{tag}-bdp-{level}-60m-10s_60m_seed*.csv"
    return sorted(MC_DIR.glob(pattern))


def read_terminal_row(path: Path) -> dict[str, float]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    return {key: float(value) for key, value in rows[-1].items() if key != "Month"}


def collect_summary() -> list[dict[str, float]]:
    summary: list[dict[str, float]] = []

    for tag, lambda_value, _, _ in LAMBDA_SPECS:
        for level in BDP_LEVELS:
            files = seed_files(tag, level)
            if not files:
                raise FileNotFoundError(f"No seed CSV files found for lambda={lambda_value}, BDP={level}")

            terminal_rows = [read_terminal_row(path) for path in files]
            out: dict[str, float] = {
                "Lambda": lambda_value,
                "BDP": float(level),
                "Seeds": float(len(files)),
            }

            for metric in METRICS:
                values = [row[metric] for row in terminal_rows]
                out[f"{metric}_mean"] = mean(values)
                out[f"{metric}_sd"] = stdev(values) if len(values) > 1 else 0.0

            summary.append(out)

    return summary


def write_summary_csv(summary: list[dict[str, float]]) -> None:
    path = DATA_DIR / "bdp_lambda_robustness_terminal_summary.csv"
    fieldnames = ["Lambda", "BDP", "Seeds"]
    for metric in METRICS:
        fieldnames.extend([f"{metric}_mean", f"{metric}_sd"])

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(summary)


def plot_lambda_robustness(summary: list[dict[str, float]]) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.9))

    for _, lambda_value, color, marker in LAMBDA_SPECS:
        rows = [row for row in summary if row["Lambda"] == lambda_value]
        rows.sort(key=lambda row: row["BDP"])

        x = [row["BDP"] for row in rows]
        y = [pct(row["TotalAdoption_mean"]) for row in rows]
        err = [pct(row["TotalAdoption_sd"]) for row in rows]

        ax.errorbar(
            x,
            y,
            yerr=err,
            color=color,
            marker=marker,
            linewidth=2.0,
            capsize=2.5,
            label=rf"$\lambda={lambda_value:.2f}$",
        )

    ax.set_title("Odporność wyniku: kanał płacy rezerwowej")
    ax.set_xlabel("BDP w modelu (PLN miesięcznie na agenta HH)")
    ax.set_ylabel("Adopcja AI/hybrid po 60 miesiącach (%)")
    ax.set_xticks(BDP_LEVELS)
    ax.legend(loc="lower left", ncols=2, frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig05_lambda_robustness.png")
    plt.close(fig)
    print("Saved fig05_lambda_robustness.png")


def main() -> None:
    summary = collect_summary()
    write_summary_csv(summary)
    plot_lambda_robustness(summary)


if __name__ == "__main__":
    main()
