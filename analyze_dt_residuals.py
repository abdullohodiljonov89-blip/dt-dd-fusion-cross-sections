
from pathlib import Path
import sys
import math
import csv

# Find the repository root when run from the Codespaces terminal.
ROOT = Path.cwd()
if not (ROOT / "data" / "dt_measurements_analysis.csv").exists():
    ROOT = ROOT.parent

SCRIPT_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from verify_bosch_hale import dt_cross_section_bosch_hale

DATA_FILE = ROOT / "data" / "dt_measurements_analysis.csv"
RESULTS_DIR = ROOT / "results"


def normalize(name):
    return "".join(c.lower() for c in name if c.isalnum())


def find_column(columns, candidates):
    lookup = {normalize(c): c for c in columns}
    for candidate in candidates:
        if normalize(candidate) in lookup:
            return lookup[normalize(candidate)]
    return None


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cannot find {DATA_FILE}. Run this script from your repository."
        )

    with DATA_FILE.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames or []

    print("Input:", DATA_FILE.relative_to(ROOT))
    print("Number of rows:", len(rows))
    print("Columns:", columns)

    if not rows:
        raise ValueError("The dataset contains no rows.")

    # Identify the energy and measured cross-section columns.
    cm_col = find_column(columns, [
        "E_cm_keV", "Ecm_keV", "energy_cm_keV",
        "center_of_mass_energy_keV", "E_cm"
    ])

    lab_col = find_column(columns, [
        "E_lab_keV", "Elab_keV", "energy_lab_keV",
        "laboratory_energy_keV", "E_lab"
    ])

    sigma_col = find_column(columns, [
        "sigma_b", "sigma_barn", "sigma_barns",
        "cross_section_b", "cross_section_barn",
        "sigma_barn_measured"
    ])

    # If the names do not match, stop instead of guessing.
    if cm_col is None and lab_col is None:
        raise ValueError(
            "Energy column not identified. Send me the printed column names."
        )

    if sigma_col is None:
        raise ValueError(
            "Cross-section column not identified. Send me the printed column names."
        )

    if cm_col is not None:
        energy_source = f"Existing CM column: {cm_col}"
        energy_is_cm = True
    else:
        energy_source = f"Laboratory energy column: {lab_col}"
        energy_is_cm = False

    print("Energy column:", cm_col if cm_col else lab_col)
    print("Cross-section column:", sigma_col)
    print("Energy source:", energy_source)

    # First pass: inspect the values and their plausible energy range.
    energies = []
    measured_values = []

    for row in rows:
        try:
            e = float(row[cm_col if cm_col else lab_col])
            s = float(row[sigma_col])
        except (TypeError, ValueError):
            energies.append(None)
            measured_values.append(None)
            continue

        energies.append(e)
        measured_values.append(s)

    print("\nFirst five energy values:", energies[:5])
    print("First five cross sections:", measured_values[:5])

    # Do not silently convert laboratory energies.
    if not energy_is_cm:
        raise ValueError(
            "The dataset has a laboratory-energy column but no recognized "
            "center-of-mass column. Confirm the experiment's beam and target "
            "before applying a frame conversion. No residuals were calculated."
        )

    output_rows = []
    residual_percent = []
    excluded = 0

    for i, row in enumerate(rows):
        e = energies[i]
        measured = measured_values[i]

        if (
            e is None or measured is None
            or not math.isfinite(e) or not math.isfinite(measured)
            or measured <= 0 or not (0.5 <= e <= 550.0)
        ):
            excluded += 1
            continue

        predicted = dt_cross_section_bosch_hale(e)
        residual = predicted - measured
        percent = 100.0 * residual / measured

        output = dict(row)
        output["analysis_E_cm_keV"] = e
        output["measured_sigma_b"] = measured
        output["bosch_hale_sigma_b"] = predicted
        output["residual_model_minus_data_b"] = residual
        output["percent_model_minus_data"] = percent
        output_rows.append(output)
        residual_percent.append(percent)

    if not output_rows:
        raise ValueError("No usable data points remained for analysis.")

    n = len(residual_percent)
    mean_residual = sum(residual_percent) / n
    mapr = sum(abs(x) for x in residual_percent) / n
    rms = math.sqrt(sum(x * x for x in residual_percent) / n)
    max_abs = max(abs(x) for x in residual_percent)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "dt_bosch_hale_residuals.csv"
    report_path = RESULTS_DIR / "dt_bosch_hale_residual_summary.txt"

    fieldnames = list(output_rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    report = f"""D-T Bosch-Hale residual analysis
================================
Input file: {DATA_FILE.relative_to(ROOT)}
Energy source: {energy_source}
Cross-section column: {sigma_col}

Input rows: {len(rows)}
Included rows: {n}
Excluded rows: {excluded}
Model range: 0.5–550 keV CM

Residual convention:
100 * (model - measured) / measured

Mean residual (%): {mean_residual:.8g}
MAPR (%): {mapr:.8g}
RMS residual (%): {rms:.8g}
Maximum absolute residual (%): {max_abs:.8g}

Statistics are unweighted. Verify source provenance, energy frame,
units, and model coefficients before using these results in the paper.
"""

    report_path.write_text(report, encoding="utf-8")

    print("\nRESIDUAL SUMMARY")
    print("----------------")
    print("Included points:", n)
    print(f"Mean residual: {mean_residual:.4f}%")
    print(f"MAPR: {mapr:.4f}%")
    print(f"RMS residual: {rms:.4f}%")
    print(f"Maximum absolute residual: {max_abs:.4f}%")
    print("\nCreated:", csv_path.relative_to(ROOT))
    print("Created:", report_path.relative_to(ROOT))


if __name__ == "__main__":
    main()

print("Residual analysis script is running.")
