# experiments/plots/plot_results.py

import os
import glob

import pandas as pd
import matplotlib.pyplot as plt


def load_latest_results():
    """
    Busca el archivo más reciente tipo:
    experiments/results/resultados_*.csv
    y lo carga en un DataFrame de pandas.
    """
    pattern = os.path.join("experiments", "results", "resultados_*.csv")
    files = glob.glob(pattern)

    if not files:
        raise FileNotFoundError("No se encontraron archivos resultados_*.csv en experiments/results/")

    # Tomar el más reciente por fecha de modificación
    latest = max(files, key=os.path.getmtime)
    print(f"Usando archivo de resultados: {latest}")

    df = pd.read_csv(latest)

    # Asegurar tipos numéricos
    df["time_ms"] = pd.to_numeric(df["time_ms"], errors="coerce")
    df["nodes_expanded"] = pd.to_numeric(df["nodes_expanded"], errors="coerce")
    df["path_cost"] = pd.to_numeric(df["path_cost"], errors="coerce")

    return df, latest


def plot_time_vs_nodes(df: pd.DataFrame, output_dir: str):
    """
    Gráfica 1: Tiempo promedio vs número de nodos (una línea por algoritmo).
    """
    # Promedio de tiempo por (num_nodes, algorithm)
    grouped = (
        df.groupby(["num_nodes", "algorithm"])["time_ms"]
        .mean()
        .reset_index()
    )

    # Pivot para tener columnas por algoritmo
    pivot = grouped.pivot(index="num_nodes", columns="algorithm", values="time_ms")

    plt.figure()
    pivot.plot(marker="o")
    plt.xlabel("Número de nodos")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Tiempo promedio vs tamaño del grafo")
    plt.grid(True)
    plt.tight_layout()

    out_path = os.path.join(output_dir, "tiempo_vs_nodos.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✔ Gráfica guardada: {out_path}")


def plot_expanded_vs_nodes(df: pd.DataFrame, output_dir: str):
    """
    Gráfica 2: Nodos expandidos promedio vs número de nodos (una línea por algoritmo).
    """
    grouped = (
        df.groupby(["num_nodes", "algorithm"])["nodes_expanded"]
        .mean()
        .reset_index()
    )

    pivot = grouped.pivot(index="num_nodes", columns="algorithm", values="nodes_expanded")

    plt.figure()
    pivot.plot(marker="o")
    plt.xlabel("Número de nodos")
    plt.ylabel("Nodos expandidos promedio")
    plt.title("Nodos expandidos promedio vs tamaño del grafo")
    plt.grid(True)
    plt.tight_layout()

    out_path = os.path.join(output_dir, "nodos_expandidos_vs_nodos.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✔ Gráfica guardada: {out_path}")


def plot_time_boxplot(df: pd.DataFrame, output_dir: str):
    """
    Gráfica 3: Boxplot de tiempos por algoritmo (todas las instancias).
    """
    plt.figure()
    df.boxplot(column="time_ms", by="algorithm")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tiempo (ms)")
    plt.title("Distribución de tiempos por algoritmo")
    plt.suptitle("")  # quitar título automático de pandas
    plt.grid(True, axis="y")
    plt.tight_layout()

    out_path = os.path.join(output_dir, "boxplot_tiempos_por_algoritmo.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✔ Gráfica guardada: {out_path}")


def main():
    plots_dir = os.path.join("experiments", "plots")
    os.makedirs(plots_dir, exist_ok=True)

    df, filename = load_latest_results()

    print(f"Registros totales: {len(df)}")
    print("Algoritmos:", df["algorithm"].unique())
    print("Tamaños de grafo:", df["num_nodes"].unique())

    plot_time_vs_nodes(df, plots_dir)
    plot_expanded_vs_nodes(df, plots_dir)
    plot_time_boxplot(df, plots_dir)

    print("\nTodas las gráficas están listas en:", plots_dir)


if __name__ == "__main__":
    main()
