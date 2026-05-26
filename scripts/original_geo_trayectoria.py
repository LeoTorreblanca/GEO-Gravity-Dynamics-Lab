import math

def simular_trayectoria():
    m = 1.0 # Masa de la partícula
    dt = 0.1 # Paso de tiempo
    r = 1.5
    v = 0.0 # Velocidad inicial
    x = 0.0 # Posición inicial
    
    print(f"{'TIEMPO':^8} | {'POSICIÓN':^10} | {'VELOCIDAD':^10}")
    print("-" * 35)
    
    for t in range(0, 50):
        # Fuerza neta (usando tu constante K=2.4516)
        k = 2.4516
        # Simulamos que la fuerza decae según la distancia
        f = (k / (max(r - x, 0.1)**2)) * math.cos(math.radians(45))
        
        # A = F/M
        a = f / m
        v += a * dt
        x += v * dt
        
        if t % 5 == 0:
            print(f"{t*dt:8.1f} | {x:10.4f} | {v:10.4f}")

if __name__ == "__main__":
    simular_trayectoria()
