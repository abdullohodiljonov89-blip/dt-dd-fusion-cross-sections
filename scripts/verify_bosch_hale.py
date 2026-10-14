
import csv
import math
from pathlib import Path

from verify_bosch_hale import dt_cross_section_bosch_hale

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "dt_measurements_analysis.csv"

# Expected column names will be checked before calculation.
with DATA_FILE.open(newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    columns = reader.fieldnames or []

print("Columns found:", columns)
print("Number of rows:", len(rows))

if not rows:
    raise ValueError("The analysis CSV contains no rows.")

print("\nBefore calculating residuals, we must identify the energy and cross-section columns.")
print("No residuals have been calculated yet.")
