from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "data" / "trayectoria_roseta.csv"

PLOT_DIR = ROOT / "docs" / "plots"
CSV_DIR = ROOT / "resultados" / "csv"
LOG_DIR = ROOT / "resultados" / "logs"

for d in [PLOT_DIR, CSV_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print("\n================================================")
print("GEO ORBITAL DYNAMICS — NEWTON VS GEO")
print("================================================")

df = pd.read_csv(DATA_PATH)

# ============================================================
# NEWTONIAN REFERENCE
# ============================================================

n = len(df)

theta = np.linspace(0, 2 * np.pi, n)

r0 = df["radio"].iloc[0]

newton_x = r0 * np.cos(theta)
newton_y = r0 * np.sin(theta)

comparison = pd.DataFrame({
    "paso": df["paso"],
    "geo_x": df["x"],
    "geo_y": df["y"],
    "geo_radio": df["radio"],
    "newton_x": newton_x,
    "newton_y": newton_y,
    "newton_radio": r0,
    "delta_radio": df["radio"] - r0,
})

comparison_path = CSV_DIR / "geo_newton_vs_geo_comparison.csv"
comparison.to_csv(comparison_path, index=False)

# ============================================================
# METRICS
# ============================================================

radial_drift_mean = float(comparison["delta_radio"].mean())
radial_drift_std = float(comparison["delta_radio"].std())
radial_drift_max = float(comparison["delta_radio"].abs().max())

x0, y0 = df["x"].iloc[0], df["y"].iloc[0]
x1, y1 = df["x"].iloc[-1], df["y"].iloc[-1]

closure_error = float(np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))

angle_start = float(np.arctan2(y0, x0))
angle_end = float(np.arctan2(y1, x1))
angle_shift = float(angle_end - angle_start)

summary = pd.DataFrame([{
    "n_points": n,
    "reference_radius": r0,
    "radial_drift_mean": radial_drift_mean,
    "radial_drift_std": radial_drift_std,
    "radial_drift_max_abs": radial_drift_max,
    "closure_error": closure_error,
    "angle_start_rad": angle_start,
    "angle_end_rad": angle_end,
    "angle_shift_rad": angle_shift,
    "angle_shift_deg": angle_shift * 180 / np.pi,
}])

summary_path = CSV_DIR / "geo_newton_vs_geo_summary.csv"
summary.to_csv(summary_path, index=False)

print("\nMetrics:")
print(summary.to_string(index=False))

# ============================================================
# PLOT 1 — GEO VS NEWTON
# ============================================================

plt.figure(figsize=(8, 8))

plt.plot(
    newton_x,
    newton_y,
    linestyle="--",
    linewidth=1.5,
    label="Newtonian closed reference"
)

plt.plot(
    df["x"],
    df["y"],
    linewidth=1.8,
    label="GEO rosette trajectory"
)

plt.scatter([0], [0], s=90, label="central body")

plt.xlabel("x")
plt.ylabel("y")

plt.title("Newtonian closed orbit vs GEO rosette trajectory")

plt.axis("equal")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_newton_vs_geo_orbit.png", dpi=300)
plt.close()

# ============================================================
# PLOT 2 — RADIAL DRIFT
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    comparison["paso"],
    comparison["delta_radio"],
    linewidth=1.4
)

plt.axhline(0, linestyle="--")

plt.xlabel("Simulation step")
plt.ylabel("GEO radius - Newtonian reference radius")

plt.title("Radial deviation from Newtonian closed reference")

plt.grid(True)
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_newton_vs_geo_radial_drift.png", dpi=300)
plt.close()

# ============================================================
# PLOT 3 — FORCE / GAP / BRAKE
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(df["paso"], df["f_net"], label="f_net", linewidth=1.4)
plt.plot(df["paso"], df["gap"], label="gap", linewidth=1.4)
plt.plot(df["paso"], df["freno"], label="freno", linewidth=1.4)

plt.xlabel("Simulation step")
plt.ylabel("value")

plt.title("GEO orbital operators: force, gap and brake")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_orbital_operators.png", dpi=300)
plt.close()

# ============================================================
# LOG
# ============================================================

log_path = LOG_DIR / "geo_newton_vs_geo.log"

with open(log_path, "w") as f:
    f.write("GEO ORBITAL DYNAMICS — NEWTON VS GEO\n")
    f.write("====================================\n\n")
    f.write(summary.to_string(index=False))
    f.write("\n\n")
    f.write(f"Comparison CSV: {comparison_path}\n")
    f.write(f"Summary CSV: {summary_path}\n")
    f.write("Plots:\n")
    f.write(" - docs/plots/geo_newton_vs_geo_orbit.png\n")
    f.write(" - docs/plots/geo_newton_vs_geo_radial_drift.png\n")
    f.write(" - docs/plots/geo_orbital_operators.png\n")

print("\nOutputs:")
print(" - resultados/csv/geo_newton_vs_geo_comparison.csv")
print(" - resultados/csv/geo_newton_vs_geo_summary.csv")
print(" - docs/plots/geo_newton_vs_geo_orbit.png")
print(" - docs/plots/geo_newton_vs_geo_radial_drift.png")
print(" - docs/plots/geo_orbital_operators.png")
print(" - resultados/logs/geo_newton_vs_geo.log")
