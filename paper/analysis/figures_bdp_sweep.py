#!/usr/bin/env python3
"""Generate figures for the MBA BDP sweep paper.

The plotting workflow mirrors the paper-* projects: compute summary data from
Monte Carlo CSV artifacts, save publication figures as PNG, and let LaTeX only
include the rendered assets.

The main paper uses the central behavioral variant from the robustness grid:
lambda=0.5, 60 months, and 10 seeds per BDP level.
"""

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
TABLES_DIR = PAPER_DIR / "latex" / "tables"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("MPLCONFIGDIR", str(PAPER_DIR / ".mplconfig"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BDP_LEVELS = [0, 500, 1000, 1500, 2000, 2500, 3000]
TRANSITION_LEVELS = [0, 500, 2000, 3000]
METRICS = [
    "TotalAdoption",
    "AutoRatio",
    "HybridRatio",
    "PrivateGrossInvestmentToGdp",
    "Inflation",
    "RefRate",
    "BondYield",
    "CorpBondYield",
    "DebtToGdp",
    "DeficitToGdp",
    "Unemployment",
    "ExRate",
    "CurrentAccountToGdp",
    "SocialTransferSpend",
    "MonthlyGdpProxy",
]

HH_METRICS = [
    "MeanMonthlyIncome",
    "ConsumptionP50",
    "MeanSavings",
    "MedianSavings",
    "Gini_Individual",
    "Gini_Wealth",
    "PovertyRate_50pct",
    "PovertyRate_30pct",
    "BankruptcyRate",
]

COLORS = {
    "blue": "#1f77b4",
    "orange": "#ff7f0e",
    "green": "#2ca02c",
    "red": "#d62728",
    "purple": "#9467bd",
    "brown": "#8c564b",
    "gray": "#4d4d4d",
}

LEVEL_COLORS = {
    0: "#4d4d4d",
    500: "#1f77b4",
    2000: "#2ca02c",
    3000: "#d62728",
}


plt.rcParams.update(
    {
        "figure.dpi": 220,
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
        "font.size": 10.5,
        "axes.titlesize": 12,
        "axes.labelsize": 10.5,
        "legend.fontsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "-",
    }
)


def pct(value: float) -> float:
    return value * 100.0


def bn(value: float) -> float:
    return value / 1_000_000_000.0


def seed_files(level: int) -> list[Path]:
    if level == 0:
        pattern = "robust-bdp-0000_robust-bdp-0000-60m-10s_60m_seed*.csv"
    else:
        pattern = f"robust-l050-bdp-{level}_robust-l050-bdp-{level}-60m-10s_60m_seed*.csv"
    return sorted(MC_DIR.glob(pattern))


def hh_file(level: int) -> Path:
    if level == 0:
        pattern = "robust-bdp-0000_robust-bdp-0000-60m-10s_60m_hh.csv"
    else:
        pattern = f"robust-l050-bdp-{level}_robust-l050-bdp-{level}-60m-10s_60m_hh.csv"

    files = sorted(MC_DIR.glob(pattern))
    if len(files) != 1:
        raise FileNotFoundError(f"Expected one HH CSV for BDP={level}, found {len(files)}")
    return files[0]


def read_terminal_row(path: Path) -> dict[str, float]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    return {key: float(value) for key, value in rows[-1].items() if key != "Month"}


def read_monthly_rows(path: Path) -> list[dict[str, float]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    return [{key: float(value) for key, value in row.items()} for row in rows]


def read_hh_rows(path: Path) -> list[dict[str, float]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    return [{key: float(value) for key, value in row.items()} for row in rows]


def collect_summary() -> list[dict[str, float]]:
    summary: list[dict[str, float]] = []

    for level in BDP_LEVELS:
        files = seed_files(level)
        if not files:
            raise FileNotFoundError(f"No seed CSV files found for BDP={level}")

        terminal_rows = [read_terminal_row(path) for path in files]
        out: dict[str, float] = {"BDP": float(level), "Seeds": float(len(files))}

        for metric in METRICS:
            values = [row[metric] for row in terminal_rows]
            out[f"{metric}_mean"] = mean(values)
            out[f"{metric}_sd"] = stdev(values) if len(values) > 1 else 0.0

        summary.append(out)

    return summary


def collect_hh_summary() -> list[dict[str, float]]:
    summary: list[dict[str, float]] = []

    for level in BDP_LEVELS:
        rows = read_hh_rows(hh_file(level))
        out: dict[str, float] = {"BDP": float(level), "Seeds": float(len(rows))}

        for metric in HH_METRICS:
            values = [row[metric] for row in rows]
            out[f"{metric}_mean"] = mean(values)
            out[f"{metric}_sd"] = stdev(values) if len(values) > 1 else 0.0

        summary.append(out)

    return summary


def write_summary_csv(summary: list[dict[str, float]]) -> None:
    path = DATA_DIR / "bdp_sweep_terminal_summary.csv"
    fieldnames = ["BDP", "Seeds"]
    for metric in METRICS:
        fieldnames.extend([f"{metric}_mean", f"{metric}_sd"])

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(summary)


def write_hh_summary_csv(summary: list[dict[str, float]]) -> None:
    path = DATA_DIR / "bdp_hh_terminal_summary.csv"
    fieldnames = ["BDP", "Seeds"]
    for metric in HH_METRICS:
        fieldnames.extend([f"{metric}_mean", f"{metric}_sd"])

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(summary)


def collect_transition_summary(metrics: list[str]) -> dict[int, list[dict[str, float]]]:
    transition: dict[int, list[dict[str, float]]] = {}

    for level in TRANSITION_LEVELS:
        files = seed_files(level)
        if not files:
            raise FileNotFoundError(f"No seed CSV files found for BDP={level}")

        seed_rows = [read_monthly_rows(path) for path in files]
        months = [int(row["Month"]) for row in seed_rows[0]]
        rows: list[dict[str, float]] = []

        for idx, month in enumerate(months):
            out: dict[str, float] = {
                "BDP": float(level),
                "Month": float(month),
                "Seeds": float(len(seed_rows)),
            }
            for metric in metrics:
                values = [rows_for_seed[idx][metric] for rows_for_seed in seed_rows]
                out[f"{metric}_mean"] = mean(values)
                out[f"{metric}_sd"] = stdev(values) if len(values) > 1 else 0.0
            rows.append(out)

        transition[level] = rows

    return transition


def write_transition_csv(transition: dict[int, list[dict[str, float]]], metrics: list[str]) -> None:
    path = DATA_DIR / "bdp_transition_firm_panel.csv"
    fieldnames = ["BDP", "Month", "Seeds"]
    for metric in metrics:
        fieldnames.extend([f"{metric}_mean", f"{metric}_sd"])

    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for level in TRANSITION_LEVELS:
            writer.writerows(transition[level])


def pl(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def pct_pm(row: dict[str, float], metric: str) -> str:
    mean_value = pl(row[f"{metric}_mean"] * 100.0)
    sd_value = pl(row[f"{metric}_sd"] * 100.0)
    return rf"{mean_value} \(\pm\) {sd_value}"


def write_terminal_latex_tables(summary: list[dict[str, float]]) -> None:
    path = TABLES_DIR / "terminal_results.tex"
    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\scriptsize",
        r"\caption{Wariant centralny: metryki firmowe i rynku pracy po 10 seedach}",
        r"\label{tab:terminal-results-real}",
        r"\begin{tabular}{@{}rccc@{}}",
        r"\toprule",
        r"BDP & AI/hybrid & Inwestycje/PKB & Bezrobocie \\",
        r"PLN/mies. & \multicolumn{3}{c}{średnia \(\pm\) odchylenie standardowe między seedami, \%} \\",
        r"\midrule",
    ]
    for row in summary:
        lines.append(
            f"{int(row['BDP'])} & "
            f"{pct_pm(row, 'TotalAdoption')} & "
            f"{pct_pm(row, 'PrivateGrossInvestmentToGdp')} & "
            f"{pct_pm(row, 'Unemployment')} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            "",
            r"\begin{table}[H]",
            r"\centering",
            r"\scriptsize",
            r"\caption{Wariant centralny: metryki makro-fiskalne po 10 seedach}",
            r"\label{tab:terminal-results-macro}",
            r"\begin{tabular}{@{}rcccc@{}}",
            r"\toprule",
            r"BDP & Inflacja & Stopa NBP & Dług/PKB & Deficyt/PKB \\",
            r"PLN/mies. & \multicolumn{4}{c}{średnia \(\pm\) odchylenie standardowe między seedami, \%} \\",
            r"\midrule",
        ]
    )
    for row in summary:
        lines.append(
            f"{int(row['BDP'])} & "
            f"{pct_pm(row, 'Inflation')} & "
            f"{pct_pm(row, 'RefRate')} & "
            f"{pct_pm(row, 'DebtToGdp')} & "
            f"{pct_pm(row, 'DeficitToGdp')} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}", ""])

    path.write_text("\n".join(lines), encoding="utf-8")


def series(summary: list[dict[str, float]], metric: str, transform=lambda x: x) -> tuple[list[float], list[float], list[float]]:
    x = [row["BDP"] for row in summary]
    y = [transform(row[f"{metric}_mean"]) for row in summary]
    err = [transform(row[f"{metric}_sd"]) for row in summary]
    return x, y, err


def plot_line(
    ax: plt.Axes,
    summary: list[dict[str, float]],
    metric: str,
    label: str,
    color: str,
    marker: str,
    transform=lambda value: value,
) -> None:
    x, y, err = series(summary, metric, transform)
    ax.errorbar(
        x,
        y,
        yerr=err,
        color=color,
        marker=marker,
        linewidth=1.9,
        capsize=2.5,
        label=label,
    )


def finish(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / filename)
    plt.close(fig)
    print(f"Saved {filename}")


def plot_adoption_investment(summary: list[dict[str, float]]) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    x, y, err = series(summary, "TotalAdoption", pct)
    ax.errorbar(
        x,
        y,
        yerr=err,
        color=COLORS["blue"],
        marker="o",
        linewidth=2.4,
        capsize=3,
        label="Adopcja AI/hybrid",
    )

    x, y, err = series(summary, "PrivateGrossInvestmentToGdp", pct)
    ax.errorbar(
        x,
        y,
        yerr=err,
        color=COLORS["orange"],
        marker="s",
        linewidth=2.4,
        capsize=3,
        label="Inwestycje prywatne / PKB",
    )

    ax.axvline(2000, color=COLORS["gray"], linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(2025, 10.25, "lokalny szczyt adopcji", color=COLORS["gray"], fontsize=9)
    ax.set_title("BDP, automatyzacja i zdolność inwestycyjna firm")
    ax.set_xlabel("BDP w modelu (PLN miesięcznie na agenta HH)")
    ax.set_ylabel("Wartość terminalna po 60 miesiącach (%)")
    ax.set_xticks(BDP_LEVELS)
    ax.set_ylim(6.8, 10.6)
    ax.legend(loc="lower left", frameon=False)
    finish(fig, "fig01_bdp_adoption_investment.png")


def plot_fiscal(summary: list[dict[str, float]]) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    x, y, err = series(summary, "DebtToGdp", pct)
    ax.errorbar(
        x,
        y,
        yerr=err,
        color=COLORS["red"],
        marker="o",
        linewidth=2.4,
        capsize=3,
        label="Dług / PKB",
    )

    x, y, err = series(summary, "DeficitToGdp", pct)
    ax.errorbar(
        x,
        y,
        yerr=err,
        color=COLORS["purple"],
        marker="s",
        linewidth=2.4,
        capsize=3,
        label="Deficyt / PKB",
    )

    ax2 = ax.twinx()
    x, y, err = series(summary, "SocialTransferSpend", bn)
    ax2.plot(
        x,
        y,
        color=COLORS["green"],
        marker="^",
        linewidth=2.0,
        linestyle=":",
        label="Transfery społeczne (mld PLN/mies.)",
    )
    ax2.set_ylabel("Transfery społeczne (mld PLN miesięcznie)")
    ax2.spines["right"].set_visible(True)

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="upper left", frameon=False)

    ax.set_title("Kanał fiskalno-dłużny")
    ax.set_xlabel("BDP w modelu (PLN miesięcznie na agenta HH)")
    ax.set_ylabel("Relacja do PKB (%)")
    ax.set_xticks(BDP_LEVELS)
    ax.set_ylim(0, 112)
    finish(fig, "fig02_bdp_fiscal_stress.png")


def plot_capital_cost(summary: list[dict[str, float]]) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    specs = [
        ("Inflation", "Inflacja", COLORS["green"], "o"),
        ("RefRate", "Stopa referencyjna NBP", COLORS["blue"], "s"),
        ("BondYield", "Rentowność długu publicznego", COLORS["orange"], "^"),
        ("CorpBondYield", "Koszt długu korporacyjnego", COLORS["red"], "D"),
    ]

    for metric, label, color, marker in specs:
        x, y, err = series(summary, metric, pct)
        ax.errorbar(
            x,
            y,
            yerr=err,
            color=color,
            marker=marker,
            linewidth=2.0,
            capsize=3,
            label=label,
        )

    ax.set_title("Kanał inflacyjno-monetarny i koszt kapitału")
    ax.set_xlabel("BDP w modelu (PLN miesięcznie na agenta HH)")
    ax.set_ylabel("Wartość terminalna (%)")
    ax.set_xticks(BDP_LEVELS)
    ax.set_ylim(1.5, 15.0)
    ax.legend(loc="upper left", frameon=False)
    finish(fig, "fig03_bdp_cost_of_capital.png")


def plot_external(summary: list[dict[str, float]]) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))

    x, y, _ = series(summary, "CurrentAccountToGdp", pct)
    ax.plot(
        x,
        y,
        color=COLORS["brown"],
        marker="o",
        linewidth=2.4,
        label="Rachunek bieżący / PKB",
    )
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.6)
    ax.set_ylabel("Rachunek bieżący / PKB (%)")
    ax.set_ylim(-14.5, -9.0)

    ax2 = ax.twinx()
    x, y, _ = series(summary, "ExRate")
    ax2.plot(
        x,
        y,
        color=COLORS["blue"],
        marker="s",
        linewidth=2.0,
        linestyle="--",
        label="Kurs PLN/EUR",
    )
    ax2.set_ylabel("Kurs PLN/EUR")
    ax2.spines["right"].set_visible(True)

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc="lower left", frameon=False)

    ax.set_title("Kanał zewnętrzny")
    ax.set_xlabel("BDP w modelu (PLN miesięcznie na agenta HH)")
    ax.set_xticks(BDP_LEVELS)
    finish(fig, "fig04_bdp_external_channel.png")


def plot_firm_transition_panel() -> None:
    metrics = [
        "TotalAdoption",
        "PrivateGrossInvestmentToGdp",
        "FirmBirths",
        "FirmDeaths",
        "NetEntry",
        "LivingFirmCount",
    ]
    transition = collect_transition_summary(metrics)
    write_transition_csv(transition, metrics)

    specs = [
        ("TotalAdoption", "Adopcja AI/hybrid", "Udział firm (%)", pct),
        ("PrivateGrossInvestmentToGdp", "Inwestycje prywatne / PKB", "Relacja do PKB (%)", pct),
        ("FirmBirths", "Narodziny firm", "Firmy / mies.", lambda value: value),
        ("FirmDeaths", "Zgony firm", "Firmy / mies.", lambda value: value),
        ("NetEntry", "Wejście netto firm", "Firmy / mies.", lambda value: value),
        ("LivingFirmCount", "Liczba żyjących firm", "Firmy", lambda value: value),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(8.2, 9.4), sharex=True)
    axes_flat = axes.flatten()

    for ax, (metric, title, ylabel, transform) in zip(axes_flat, specs):
        for level in TRANSITION_LEVELS:
            rows = transition[level]
            months = [row["Month"] for row in rows]
            values = [transform(row[f"{metric}_mean"]) for row in rows]
            ax.plot(
                months,
                values,
                color=LEVEL_COLORS[level],
                linewidth=2.0,
                label=f"BDP {level}",
            )

        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xlim(1, 60)
        ax.set_xticks([1, 12, 24, 36, 48, 60])

    for ax in axes_flat[-2:]:
        ax.set_xlabel("Miesiąc symulacji")

    handles, labels = axes_flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.995), ncols=4, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(FIGURES_DIR / "fig06_firm_transition_panel.png")
    plt.close(fig)
    print("Saved fig06_firm_transition_panel.png")


def plot_hh_control_panel(summary: list[dict[str, float]]) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(8.2, 9.2), sharex=True)
    axes_flat = axes.flatten()

    ax = axes_flat[0]
    plot_line(ax, summary, "MeanMonthlyIncome", "Średni dochód HH", COLORS["blue"], "o")
    plot_line(ax, summary, "ConsumptionP50", "Mediana konsumpcji", COLORS["orange"], "s")
    ax.set_title("Dochód i konsumpcja")
    ax.set_ylabel("PLN miesięcznie")
    ax.legend(loc="upper left", frameon=False)

    ax = axes_flat[1]
    plot_line(ax, summary, "MeanSavings", "Średnie oszczędności", COLORS["purple"], "o")
    plot_line(ax, summary, "MedianSavings", "Mediana oszczędności", COLORS["green"], "s")
    ax.axhline(0, color="black", linewidth=0.8, alpha=0.6)
    ax.set_title("Bilans gospodarstw")
    ax.set_ylabel("PLN")
    ax.legend(loc="upper left", frameon=False)

    ax = axes_flat[2]
    plot_line(ax, summary, "Gini_Individual", "Gini dochodowy", COLORS["red"], "o")
    ax.set_title("Nierówności dochodowe")
    ax.set_ylabel("Indeks")
    ax.set_ylim(0.275, 0.295)
    ax.legend(loc="upper left", frameon=False)

    ax = axes_flat[3]
    plot_line(ax, summary, "Gini_Wealth", "Gini majątkowy", COLORS["brown"], "o")
    ax.set_title("Nierówności majątkowe")
    ax.set_ylabel("Indeks modelowy")
    ax.legend(loc="upper left", frameon=False)

    ax = axes_flat[4]
    plot_line(ax, summary, "PovertyRate_50pct", "Ubóstwo 50% mediany", COLORS["blue"], "o", pct)
    plot_line(ax, summary, "PovertyRate_30pct", "Ubóstwo 30% mediany", COLORS["orange"], "s", pct)
    ax.set_title("Ubóstwo względne")
    ax.set_ylabel("Udział HH (%)")
    ax.legend(loc="upper left", frameon=False)

    ax = axes_flat[5]
    plot_line(ax, summary, "BankruptcyRate", "Bankructwa HH", COLORS["gray"], "o", pct)
    ax.set_title("Bankructwa gospodarstw")
    ax.set_ylabel("Udział HH (%)")
    ax.set_ylim(-0.02, 0.25)
    ax.legend(loc="upper left", frameon=False)

    for ax in axes_flat:
        ax.set_xticks(BDP_LEVELS)

    for ax in axes_flat[-2:]:
        ax.set_xlabel("BDP w modelu (PLN miesięcznie na agenta HH)")

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig07_hh_control_panel.png")
    plt.close(fig)
    print("Saved fig07_hh_control_panel.png")


def main() -> None:
    summary = collect_summary()
    hh_summary = collect_hh_summary()
    write_summary_csv(summary)
    write_hh_summary_csv(hh_summary)
    write_terminal_latex_tables(summary)
    plot_adoption_investment(summary)
    plot_fiscal(summary)
    plot_capital_cost(summary)
    plot_external(summary)
    plot_firm_transition_panel()
    plot_hh_control_panel(hh_summary)


if __name__ == "__main__":
    main()
