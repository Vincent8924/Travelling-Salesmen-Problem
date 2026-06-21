import time
from pathlib import Path

import pandas as pd

from utils.tsplib_parser import load_tsplib
from utils.distance import build_distance_matrix
from utils.tour_utils import generate_random_tour

from algorithms.local_search import two_opt
from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.ant_colony import ant_colony_optimization


class Benchmark:

    def __init__(self):
        self.results = []
        self.algorithms = {
            "2-Opt": two_opt,
            "GA": genetic_algorithm,
            "ACO": ant_colony_optimization
        }

    def run_algorithm(
        self,
        algorithm_name,
        algorithm_function,
        distance_matrix,
        dataset_name,
        run_number
    ):
        if algorithm_name == "2-Opt":
            initial_tour = generate_random_tour(len(distance_matrix))
        else:
            initial_tour = None
        start = time.perf_counter()
        best_tour, best_distance = algorithm_function(
            distance_matrix,
            initial_tour
        )
        runtime = time.perf_counter() - start
        self.results.append({
            "Dataset": dataset_name,
            "Algorithm": algorithm_name,
            "Run": run_number,
            "Distance": best_distance,
            "Runtime (s)": runtime
        })

    def run_all(
        self,
        dataset_folder="datasets",
        runs=1
    ):
        dataset_folder = Path(dataset_folder)
        for dataset_file in sorted(dataset_folder.glob("*.tsp")):
            print("=" * 70)
            print(f"Dataset : {dataset_file.name}")
            print("=" * 70)
            metadata, coordinates = load_tsplib(dataset_file)
            distance_matrix = build_distance_matrix(coordinates)
            dataset_name = metadata["NAME"]
            for algorithm_name, algorithm_function in self.algorithms.items():
                print(f"Running {algorithm_name}...")
                for run in range(1, runs + 1):

                    self.run_algorithm(
                        algorithm_name,
                        algorithm_function,
                        distance_matrix,
                        dataset_name,
                        run
                    )

        self.save_results()

    def save_results(self, filename="results/benchmark_results.xlsx"):
        Path("results").mkdir(exist_ok=True)
        df = pd.DataFrame(self.results)
        summary = (
            df.groupby(["Dataset", "Algorithm"])
            .agg(
                Mean_Distance=("Distance", "mean"),
                Best_Distance=("Distance", "min"),
                Worst_Distance=("Distance", "max"),
                Std_Distance=("Distance", "std"),
                Mean_Runtime=("Runtime (s)", "mean"),
            )
            .reset_index()
        )
        with pd.ExcelWriter(filename) as writer:

            df.to_excel(
                writer,
                sheet_name="Raw Results",
                index=False
            )
            summary.to_excel(
                writer,
                sheet_name="Summary Statistics",
                index=False
            )
        print("\nBenchmark completed.")
        print(f"Total experiments: {len(df)}")
        print(f"Results saved to: {filename}")
        return df, summary