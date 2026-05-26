import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ============================================================
# GEO ORBITAL DYNAMICS
# Rosette Orbital Analysis
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "data" / "trayectoria_roseta.csv"

PLOT_DIR = ROOT / "docs" / "plots"
CSV_DIR = ROOT / "resultados" / "csv"
LOG_DIR = ROOT / "resultados" / "logs"

PLOT_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

print("\n================================================")
print("GEO ORBITAL DYNAMICS — ROSETTE ANALYSIS")
print("================================================")

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

# ============================================================
# BASIC METRICS
# ============================================================

mean_radius = df["radio"].mean()
std_radius = df["radio"].std()

mean_force = df["f_net"].mean()
std_force = df["f_net"].std()

mean_gap = df["gap"].mean()
mean_brake = df["freno"].mean()

print("\n================================================")
print("BASIC ORBITAL METRICS")
print("================================================")

print(f"mean_radius = {mean_radius}")
print(f"std_radius  = {std_radius}")

print(f"mean_force  = {mean_force}")
print(f"std_force   = {std_force}")

print(f"mean_gap    = {mean_gap}")
print(f"mean_brake  = {mean_brake}")

# ============================================================
# SAVE SUMMARY
# ============================================================

summary = pd.DataFrame([{
    "mean_radius": mean_radius,
    "std_radius": std_radius,
    "mean_force": mean_force,
    "std_force": std_force,
    "mean_gap": mean_gap,
    "mean_brake": mean_brake
}])

summary.to_csv(
    CSV_DIR / "geo_rosette_summary.csv",
    index=False
)

# ============================================================
# ROSETTE ORBIT PLOT
# ============================================================

plt.figure(figsize=(8,8))

plt.plot(
    df["x"],
    df["y"],
    linewidth=1.2
)

plt.scatter(
    [0],
    [0],
    s=80
)

plt.xlabel("x")
plt.ylabel("y")

plt.title("GEO Orbital Dynamics — Rosette Orbit")

plt.axis("equal")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "geo_rosette_orbit.png",
    dpi=300
)

# ============================================================
# RADIUS EVOLUTION
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    df["paso"],
    df["radio"],
    linewidth=1.2
)

plt.xlabel("Simulation Step")
plt.ylabel("Radius")

plt.title("Orbital Radius Evolution")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "geo_rosette_radius.png",
    dpi=300
)

# ============================================================
# FORCE EVOLUTION
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    df["paso"],
    df["f_net"],
    linewidth=1.2
)

plt.xlabel("Simulation Step")
plt.ylabel("Net Force")

plt.title("Effective Orbital Force")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    PLOT_DIR / "geo_rosette_force.png",
    dpi=300
)

# ============================================================
# EXPORT CLEAN DATA
# ============================================================

df.to_csv(
    CSV_DIR / "geo_rosette_clean_dataset.csv",
    index=False
)

# ============================================================
# LOG
# ============================================================

with open(LOG_DIR / "geo_rosette_analysis.log", "w") as f:

    f.write("GEO ORBITAL DYNAMICS\n")
    f.write("====================\n\n")

    f.write(f"Dataset shape: {df.shape}\n")
    f.write(f"Mean radius: {mean_radius}\n")
    f.write(f"Radius std: {std_radius}\n")
    f.write(f"Mean force: {mean_force}\n")
    f.write(f"Force std: {std_force}\n")
    f.write(f"Mean gap: {mean_gap}\n")
    f.write(f"Mean brake: {mean_brake}\n")

print("\nOutputs:")
print(" - resultados/csv/geo_rosette_summary.csv")
print(" - resultados/csv/geo_rosette_clean_dataset.csv")
print(" - docs/plots/geo_rosette_orbit.png")
print(" - docs/plots/geo_rosette_radius.png")
print(" - docs/plots/geo_rosette_force.png")
print(" - resultados/logs/geo_rosette_analysis.log")
