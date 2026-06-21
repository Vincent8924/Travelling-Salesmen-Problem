import json
from utils.benchmark import Benchmark
import random
random.seed(42)

def load_config(config_file="config.json"):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_file}' not found. Using default settings.")
        return {}

if __name__ == "__main__":
    config = load_config()
    benchmark = Benchmark()
    
    benchmark.run_all(
        dataset_folder=config.get("dataset_folder", "datasets"), 
        runs=config.get("runs", 1)
    )