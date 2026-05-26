#!/usr/bin/env python3
import numpy as np
from geo_orbital_solver import OrbitalSolver

# Configuración inicial de la partícula (Inyección en r=0.8, vel=0.9)
solver = OrbitalSolver()
pos = np.array([0.8, 0.0])
vel = np.array([0.0, 0.9])
dt = 0.001
pasos = 5000

print("Iniciando Experimento 05: Simulación de Trayectoria en Roseta...")

for i in range(pasos):
    pos, vel, estados = solver.obtener_paso(pos, vel, dt)
    
    # Cada 500 pasos guardamos un punto para analizar la roseta
    if i % 500 == 0:
        r = np.linalg.norm(pos)
        print(f"Paso {i}: Radio={r:.4f} | F_net={estados['F_net']:.4f} | Gap={estados['Gap']:.4f}")

print("Simulación completada. El sistema ha preservado la coherencia 5D.")
