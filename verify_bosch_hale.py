
"""
Verify the Bosch–Hale D-T cross-section parameterization.

Source:
Bosch, H.-S. & Hale, G. M. (1992),
Nuclear Fusion 32, 611–631, Table IV.

Energy input: center-of-mass energy, keV
Cross-section output: barns
Published S-factor coefficients give sigma in millibarns.
"""

import math

# Bosch–Hale D-T cross-section coefficients (Table IV)
BG = 34.3827

A1 = 6.927e4
A2 = 7.454e8
A3 = 2.050e6
A4 = 5.2002e4
A5 = 0.0

B1 = 6.38e1
B2 = -9.95e-1
B3 = 6.981e-5
B4 = 1.728e-4

E_MIN_KEV = 0.5
E_MAX_KEV = 550.0

# Independent implementation benchmark
BENCHMARK_ENERGY_KEV = 100.0
BENCHMARK_SIGMA_BARN = 3.42724517
BENCHMARK_TOLERANCE_BARN = 1e-6


def dt_cross_section_bosch_hale(energy_cm_kev):
    """Return Bosch–Hale D-T cross section in barns."""
    energy = float(energy_cm_kev)

    if not math.isfinite(energy):
        raise ValueError("Energy must be a finite number.")

    if not E_MIN_KEV <= energy <= E_MAX_KEV:
        raise ValueError(
            f"Energy must be within {E_MIN_KEV}–{E_MAX_KEV} keV CM."
        )

    s_numerator = A1 + energy * (
        A2 + energy * (
            A3 + energy * (A4 + energy * A5)
        )
    )

    s_denominator = 1.0 + energy * (
        B1 + energy * (
            B2 + energy * (B3 + energy * B4)
        )
    )

    if s_denominator == 0.0:
        raise ArithmeticError("S-factor denominator is zero.")

    s_factor_mb_keV = s_numerator / s_denominator

    sigma_mb = s_factor_mb_keV / (
        energy * math.exp(BG / math.sqrt(energy))
    )

    return sigma_mb / 1000.0  # millibarns -> barns


def main():
    print("Bosch–Hale D-T verification")
    print("Energy is center-of-mass energy.")
    print("Cross section is in barns.\n")

    # Benchmark test
    calculated = dt_cross_section_bosch_hale(
        BENCHMARK_ENERGY_KEV
    )

    print(f"At {BENCHMARK_ENERGY_KEV:.1f} keV:")
    print(f"Calculated: {calculated:.8f} barn")
    print(f"Reference:  {BENCHMARK_SIGMA_BARN:.8f} barn")
    difference = abs(calculated - BENCHMARK_SIGMA_BARN)
    print(f"Absolute difference: {difference:.3e} barn")

    if difference > BENCHMARK_TOLERANCE_BARN:
        raise AssertionError(
            "Benchmark failed. Do not use this implementation "
            "for research results until the discrepancy is resolved."
        )

    print("\nBenchmark passed.")

    # Additional values to inspect for plausible energy dependence.
    print("\nEnergy (keV CM) | Cross section (barn)")
    for energy in (0.5, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 550.0):
        sigma = dt_cross_section_bosch_hale(energy)
        print(f"{energy:15.3f} | {sigma:.8g}")


if __name__ == "__main__":
    main()
