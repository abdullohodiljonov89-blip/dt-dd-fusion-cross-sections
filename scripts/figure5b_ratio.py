
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Resolve paths from the repository root.
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "figure5b_ratio.csv"
OUTPUT_FILE = ROOT / "figures" / "figure5b_ratio.png"

# Load the previously calculated ratio dataset.
df = pd.read_csv(DATA_FILE)

required = {
    "E_cm_keV",
    "sigma_DT_interpolated_b",
    "sigma_DD_total_b",
    "ratio_DT_to_DDtotal",
}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

# Check the stored ratio against the component cross sections.
calculated_ratio = (
    df["sigma_DT_interpolated_b"] / df["sigma_DD_total_b"]
)
if not (
    (calculated_ratio - df["ratio_DT_to_DDtotal"]).abs() < 0.002
).all():
    raise ValueError("Stored ratios do not match the cross-section values.")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.plot(
    df["E_cm_keV"],
    df["ratio_DT_to_DDtotal"],
    marker="o",
    linestyle="-",
)

ax.set_xscale("log")
ax.set_xlabel(r"Center-of-mass energy $E_{\mathrm{cm}}$ (keV)")
ax.set_ylabel(
    r"Cross-section ratio "
    r"$\sigma_{DT}/\sigma_{DD,\mathrm{total}}$"
)
ax.set_title("D–T to total D–D fusion cross-section ratio")
ax.grid(True, which="both", linestyle="--", linewidth=0.5)

fig.text(
    0.5,
    0.01,
    "Provisional data; D–D source matching and uncertainty validation pending.",
    ha="center",
    fontsize=8,
)
fig.tight_layout(rect=[0, 0.04, 1, 1])
fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {OUTPUT_FILE}")
