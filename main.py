# main.py
"""
Programa principal del proyecto.
Ejecuta los tres algoritmos de rutas mínimas (Dijkstra, A*, Bidireccional)
sobre un grafo generado automáticamente.

Este archivo sirve como DEMO rápida para verificar que todo funciona.
"""

from src.graph import generar_grafo_geometrico
from src.dijkstra import dijkstra
from src.astar import astar
from src.dijkstra_bi import bidirectional_dijkstra
from src.utils import run_with_timing


def print_result(name, result):
    print(f"\n===== {name} =====")
    print(f"Ruta: {result.path}")
    print(f"Costo total: {result.cost}")
    print(f"Nodos expandidos: {result.nodes_expanded}")
    print(f"Tiempo: {result.elapsed_ms:.3f} ms")


def main():
    # ======================================================
    # 1. GENERAR GRAFO DE DEMO
    # ======================================================
    print("🧱 Generando grafo de demostración...")

    # Grafo pequeño: 15 nodos, densidad 0.20
    graph = generar_grafo_geometrico(num_nodos=15, densidad=0.20, seed=1)

    # Elegimos un origen y destino de forma fija para la demo
    start = "0"
    goal = "10"

    print(f"Probando ruta: {start} → {goal}")

    # ======================================================
    # 2. Probar algoritmos
    # ======================================================
    algorithms = {
        "Dijkstra": dijkstra,
        "A* (A-star)": astar,
        "Dijkstra Bidireccional": bidirectional_dijkstra,
    }

    for name, alg in algorithms.items():
        print(f"\nEjecutando {name} ...")
        result = run_with_timing(alg, graph, start, goal)
        print_result(name, result)

    print("\n🎉 DEMO COMPLETADA.")


if __name__ == "__main__":
    main()
