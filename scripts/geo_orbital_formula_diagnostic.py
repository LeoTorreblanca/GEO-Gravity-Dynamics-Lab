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
print("GEO ORBITAL DYNAMICS — FORMULA DIAGNOSTIC")
print("================================================")

df = pd.read_csv(DATA_PATH)

# ============================================================
# NORMALIZED PUBLIC MODEL
# ============================================================
# This script does NOT expose the internal GEO engine.
# It applies a public effective diagnostic formula:
#
# Newton:
#   F_N(r) = 1 / r²
#
# GEO public effective diagnostic:
#   F_GEO(r, theta) = (1 / r²) * cos(2 theta)
#
# Extended symbolic form:
#   F_GDD(r, theta) = [G * M_eff(r) / r²] * cos(2 theta)
#
# In this public diagnostic:
#   G = 1
#   M_eff = 1
# ============================================================

eps = 1e-12

x = df["x"].to_numpy(dtype=float)
y = df["y"].to_numpy(dtype=float)
r = df["radio"].to_numpy(dtype=float)

theta = np.unwrap(np.arctan2(y, x))

force_newton = 1.0 / np.maximum(r**2, eps)
phase_operator = np.cos(2.0 * theta)
force_geo_public = force_newton * phase_operator

force_ratio = force_geo_public / np.maximum(force_newton, eps)

# derivatives / diagnostics
dr = np.gradient(r)
dtheta = np.gradient(theta)
curvature_proxy = np.gradient(dtheta)

energy_like_newton = -1.0 / np.maximum(r, eps)
energy_like_geo = energy_like_newton * phase_operator

df_out = df.copy()

df_out["theta_rad"] = theta
df_out["theta_deg"] = theta * 180.0 / np.pi
df_out["F_newton_norm"] = force_newton
df_out["phase_cos_2theta"] = phase_operator
df_out["F_GEO_public_norm"] = force_geo_public
df_out["ratio_GEO_Newton"] = force_ratio
df_out["dr_step"] = dr
df_out["dtheta_step"] = dtheta
df_out["curvature_proxy"] = curvature_proxy
df_out["E_newton_like"] = energy_like_newton
df_out["E_GEO_like"] = energy_like_geo

diagnostic_path = CSV_DIR / "geo_orbital_formula_diagnostic.csv"
df_out.to_csv(diagnostic_path, index=False)

# ============================================================
# SUMMARY
# ============================================================

summary = pd.DataFrame([{
    "n_points": len(df_out),
    "radius_min": float(np.min(r)),
    "radius_max": float(np.max(r)),
    "radius_mean": float(np.mean(r)),
    "theta_start_rad": float(theta[0]),
    "theta_end_rad": float(theta[-1]),
    "theta_span_rad": float(theta[-1] - theta[0]),
    "theta_span_deg": float((theta[-1] - theta[0]) * 180.0 / np.pi),
    "F_newton_mean": float(np.mean(force_newton)),
    "F_newton_std": float(np.std(force_newton)),
    "F_GEO_public_mean": float(np.mean(force_geo_public)),
    "F_GEO_public_std": float(np.std(force_geo_public)),
    "phase_mean": float(np.mean(phase_operator)),
    "phase_std": float(np.std(phase_operator)),
    "ratio_mean": float(np.mean(force_ratio)),
    "ratio_std": float(np.std(force_ratio)),
    "curvature_proxy_mean": float(np.mean(curvature_proxy)),
    "curvature_proxy_std": float(np.std(curvature_proxy)),
    "gap_mean": float(df["gap"].mean()) if "gap" in df.columns else np.nan,
    "freno_mean": float(df["freno"].mean()) if "freno" in df.columns else np.nan,
    "f_net_mean": float(df["f_net"].mean()) if "f_net" in df.columns else np.nan,
}])

summary_path = CSV_DIR / "geo_orbital_formula_summary.csv"
summary.to_csv(summary_path, index=False)

print("\nSummary:")
print(summary.to_string(index=False))

# ============================================================
# PLOT 1 — FORCE LAW COMPARISON
# ============================================================

plt.figure(figsize=(11, 6))

plt.plot(df["paso"], force_newton, label="Newton normalized: 1/r²", linewidth=1.4)
plt.plot(df["paso"], force_geo_public, label="GEO public: (1/r²) cos(2θ)", linewidth=1.4)

plt.xlabel("Simulation step")
plt.ylabel("normalized force")

plt.title("Public force diagnostic: Newton vs GEO phase-modulated law")

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_force_law_comparison.png", dpi=300)
plt.close()

# ============================================================
# PLOT 2 — PHASE OPERATOR
# ============================================================

plt.figure(figsize=(11, 6))

plt.plot(df["paso"], phase_operator, linewidth=1.4)

plt.axhline(0.0, linestyle="--")

plt.xlabel("Simulation step")
plt.ylabel("cos(2θ)")

plt.title("GEO phase operator")

plt.grid(True)
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_phase_operator.png", dpi=300)
plt.close()

# ============================================================
# PLOT 3 — GEO / NEWTON RATIO
# ============================================================

plt.figure(figsize=(11, 6))

plt.plot(df["paso"], force_ratio, linewidth=1.4)

plt.axhline(1.0, linestyle="--")
plt.axhline(0.0, linestyle="--")

plt.xlabel("Simulation step")
plt.ylabel("F_GEO / F_Newton")

plt.title("GEO effective force ratio")

plt.grid(True)
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_force_ratio.png", dpi=300)
plt.close()

# ============================================================
# PLOT 4 — ORBIT COLORED BY PHASE
# ============================================================

plt.figure(figsize=(8, 8))

scatter = plt.scatter(
    df["x"],
    df["y"],
    c=phase_operator,
    s=8
)

plt.scatter([0], [0], s=90)

plt.xlabel("x")
plt.ylabel("y")

plt.title("GEO rosette trajectory colored by phase operator")

plt.axis("equal")
plt.grid(True)
plt.colorbar(scatter, label="cos(2θ)")
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_rosette_phase_colormap.png", dpi=300)
plt.close()

# ============================================================
# PLOT 5 — GAP / BRAKE / PHASE
# ============================================================

if "gap" in df.columns and "freno" in df.columns:
    plt.figure(figsize=(11, 6))

    gap_norm = df["gap"] / max(abs(df["gap"]).max(), eps)
    brake_norm = df["freno"] / max(abs(df["freno"]).max(), eps)

    plt.plot(df["paso"], phase_operator, label="cos(2θ)", linewidth=1.2)
    plt.plot(df["paso"], gap_norm, label="gap normalized", linewidth=1.2)
    plt.plot(df["paso"], brake_norm, label="brake normalized", linewidth=1.2)

    plt.xlabel("Simulation step")
    plt.ylabel("normalized value")

    plt.title("GEO operators: phase, gap and brake")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(PLOT_DIR / "geo_phase_gap_brake.png", dpi=300)
    plt.close()

# ============================================================
# PLOT 6 — CURVATURE PROXY
# ============================================================

plt.figure(figsize=(11, 6))

plt.plot(df["paso"], curvature_proxy, linewidth=1.4)

plt.axhline(0.0, linestyle="--")

plt.xlabel("Simulation step")
plt.ylabel("curvature proxy")

plt.title("Trajectory curvature proxy")

plt.grid(True)
plt.tight_layout()

plt.savefig(PLOT_DIR / "geo_curvature_proxy.png", dpi=300)
plt.close()

# ============================================================
# LOG
# ============================================================

log_path = LOG_DIR / "geo_orbital_formula_diagnostic.log"

with open(log_path, "w") as f:
    f.write("GEO ORBITAL DYNAMICS — FORMULA DIAGNOSTIC\n")
    f.write("=========================================\n\n")
    f.write("Public diagnostic formula:\n")
    f.write("F_N(r) = 1 / r^2\n")
    f.write("F_GEO(r,theta) = (1 / r^2) * cos(2 theta)\n")
    f.write("F_GDD(r,theta) = [G * M_eff(r) / r^2] * cos(2 theta)\n\n")
    f.write(summary.to_string(index=False))
    f.write("\n\n")
    f.write(f"Diagnostic CSV: {diagnostic_path}\n")
    f.write(f"Summary CSV: {summary_path}\n")
    f.write("Plots:\n")
    f.write(" - docs/plots/geo_force_law_comparison.png\n")
    f.write(" - docs/plots/geo_phase_operator.png\n")
    f.write(" - docs/plots/geo_force_ratio.png\n")
    f.write(" - docs/plots/geo_rosette_phase_colormap.png\n")
    f.write(" - docs/plots/geo_phase_gap_brake.png\n")
    f.write(" - docs/plots/geo_curvature_proxy.png\n")

print("\nOutputs:")
print(" - resultados/csv/geo_orbital_formula_diagnostic.csv")
print(" - resultados/csv/geo_orbital_formula_summary.csv")
print(" - docs/plots/geo_force_law_comparison.png")
print(" - docs/plots/geo_phase_operator.png")
print(" - docs/plots/geo_force_ratio.png")
print(" - docs/plots/geo_rosette_phase_colormap.png")
print(" - docs/plots/geo_phase_gap_brake.png")
print(" - docs/plots/geo_curvature_proxy.png")
print(" - resultados/logs/geo_orbital_formula_diagnostic.log")
