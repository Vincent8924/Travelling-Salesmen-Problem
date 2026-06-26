# Travelling Salesman Problem (TSP) Solver

## Project Overview
This project implements and evaluates various metaheuristic and local search algorithms to solve the Travelling Salesman Problem (TSP). The algorithms implemented include **Genetic Algorithm (GA)**, **Ant Colony Optimization (ACO)**, and **2-Opt Local Search**. 

This project was developed as part of the TDA6323 Algorithm Design and Analysis course at Multimedia University (MMU).

## Authors
* **Vincent Tay Yong Jun**
* **Koh Chen Yap**
* **Lew Zixin**

## Features
* **Algorithms Implemented:**
    * Genetic Algorithm (GA)
    * Ant Colony Optimization (ACO)
    * Local Search (2-Opt)
* **Datasets:** Evaluated on standard TSPLIB benchmark instances (berlin52.tsp, eil101.tsp, kroA100.tsp, rat99.tsp, st70.tsp).
* **Benchmarking:** Built-in automated scripts evaluate execution time and tour length quality, exporting raw data and summary statistics to CSV and Excel files.

## Project Structure
- algorithms/
    - ant_colony.py         # Ant Colony Optimization implementation
    - genetic_algorithm.py  # Genetic Algorithm implementation
    - local_search.py       # 2-Opt Local Search implementation
- datasets/                 # TSPLIB benchmark datasets (.tsp format)
    -results/                  # Generated benchmark results and statistics (CSV/XLSX)
- utils/
    - benchmark.py          # Benchmarking utilities and metrics
    - distance.py           # Euclidean distance matrix calculations
    - tour_utils.py         # Tour length calculation and utility logic
    - tsplib_parser.py      # Parser for extracting node coordinates from .tsp files
- config.json               # Hyperparameters and algorithm configuration
- main.py                   # Main entry point to run algorithms and benchmarks
- README.md                 # Project documentation

## Getting Started

### Prerequisites
Ensure you have Python 3.x installed on your system. You may also need to install dependencies for data manipulation and exporting benchmark results (e.g., pandas, openpyxl).

pip install pandas openpyxl

### Usage
1.  **Configuration:** Modify the config.json file to adjust algorithm hyperparameters (such as population size, mutation rate for GA, or pheromone evaporation rates for ACO) or to select the specific datasets you wish to evaluate.
2.  **Execution:** Run the main Python script from the root directory to execute the solvers or start the benchmarking process:
    python main.py
3.  **Viewing Results:** After execution, check the results/ folder for exported CSV and Excel files containing the performance metrics, including summary statistics and raw results.

## Implementation Details
* **Genetic Algorithm (GA):** Utilizes selection, crossover, and mutation operations tailored specifically for permutation-based representations of TSP tours.
* **Ant Colony Optimization (ACO):** Simulates the foraging behavior of ants, updating pheromone trails on a graph to probabilistically construct optimal shortest paths.
* **2-Opt Local Search:** An iterative improvement heuristic that untangles crossing routes by systematically swapping pairs of edges until a local optimum (where no further improvements can be made) is reached.