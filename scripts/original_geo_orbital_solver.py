#!/usr/bin/env python3
import numpy as np
from geo_core_gravity_v3 import GeoGravityEngine

class OrbitalSolver:
    def __init__(self):
        self.engine = GeoGravityEngine()

    def obtener_paso(self, pos, vel, dt):
        """
        Calcula la siguiente posición y velocidad aplicando el freno 5D.
        """
        # 1. Obtener aceleración del núcleo GEO
        acel, estados = self.engine.calcular_aceleracion_vectorial(pos)
        
        # 2. Obtener freno angular (torque de acoplamiento al bulk)
        r = np.linalg.norm(pos)
        v_tan = np.linalg.norm(vel)
        freno = self.engine.calcular_freno_angular(r, v_tan)
        
        # 3. Aplicar dinámica: El freno resta momento angular visible
        vel_frenada = vel * (1.0 - freno * dt)
        nueva_vel = vel_frenada + acel * dt
        nueva_pos = pos + nueva_vel * dt
        
        return nueva_pos, nueva_vel, estados
