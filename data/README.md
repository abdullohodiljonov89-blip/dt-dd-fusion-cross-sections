# Data Directory

This directory will contain the experimental measurements used in the D–T and D–D fusion cross-section analysis.

## Planned files

- `dt_measurements.csv` — deuterium–tritium measurements, with original source values and documented screening decisions.
- `dd_measurements.csv` — deuterium–deuterium measurements, including the two principal reaction branches where available.

## Data integrity

Original published values will be distinguished from converted quantities and derived calculations. Each dataset will document its source, units, energy frame, and any excluded observations.

No placeholder values will be presented as experimental measurements. Files will be added after their contents have been checked against the cited sources.

### Laboratory-to-center-of-mass energy conversion

The original D–T measurements in LA-1479 Table VI are reported as deuteron laboratory energies, \(E_{\mathrm{lab}}\). For a deuteron incident on a stationary tritium target, the nonrelativistic center-of-mass energy is calculated as

\[
E_{\mathrm{cm}}=\frac{m_{\mathrm{T}}}{m_{\mathrm{D}}+m_{\mathrm{T}}}E_{\mathrm{lab}}
\approx \frac{3}{5}E_{\mathrm{lab}.
\]

The converted energy is used for plotting against center-of-mass energy. The original laboratory energies and source-reported cross sections are retained in the raw dataset. The conversion does not modify the cross-section values.

### Suspected anomalous measurements

Five measurements from LA-1479 Table VI were excluded from the provisional analysis dataset because their reported cross sections appear inconsistent with nearby measurements: 24.89, 24.91, 24.96, 49.60, and 49.62 keV. The original reported values are preserved unchanged in `dt_measurements.csv`. The exclusions are provisional and do not establish that the source measurements are erroneous; the cause of the apparent discrepancies has not been independently verified. These points are therefore treated as a limitation of the present analysis rather than silently corrected.
