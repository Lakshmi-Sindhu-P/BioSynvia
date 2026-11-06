"""Inspect shapes and culture-age patterns without fitting any model."""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--data", type=Path, default=Path("data/processed/v3/processed_candidates.csv"))
parser.add_argument("--output", type=Path, default=Path("reports/preparation/relationships.png"))
args = parser.parse_args()
if args.output.exists():
    raise ValueError("Choose a new figure filename.")
df = pd.read_csv(args.data)
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), layout="constrained")
for ax, column, label in zip(axes,
        ["x__permittivity_pf_cm", "x__transmission_arb_unit", "x__dissolved_co2_sat"],
        ["Permittivity (pF/cm)", "Transmission (arbitrary unit)", "Dissolved CO2 (% saturation)"]):
    present = df.dropna(subset=[column, "y__vcd_cells_per_ml"])
    points = ax.scatter(present[column], present.y__vcd_cells_per_ml / 1e6,
                        c=present["Time (h)"], cmap="viridis", vmin=0, vmax=330, s=16, alpha=.7)
    zeros = present[present.y__vcd_cells_per_ml.eq(0)]
    ax.scatter(zeros[column], zeros.y__vcd_cells_per_ml, marker="x", color="black", s=55)
    ax.set(xlabel=label, ylabel="Recorded VCD (million cells/mL)", title=f"{len(present)} available pairs")
    ax.spines[["top", "right"]].set_visible(False)
fig.colorbar(points, ax=axes, label="Elapsed culture time (hours)", shrink=.85)
fig.suptitle("Exploratory shapes and time patterns; no fitted model or scientific label approval", fontsize=12)
args.output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output, dpi=180)
plt.close(fig)
