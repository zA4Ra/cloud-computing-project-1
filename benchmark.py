# Task 5: compare the old way of loading the data vs the optimized way
# Run with: python benchmark.py All_Diets.csv
import pandas as pd
import io
import sys
import time
from datetime import datetime
import lambda_function

if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = "All_Diets.csv"

with open(file_path, "rb") as file:
    csv_data = file.read()


def old_version():
    # Original code: load every column with default types
    df = pd.read_csv(io.BytesIO(csv_data))
    df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
    return df


def new_version():
    # Optimized code from lambda_function.py
    df = lambda_function.clean_data(csv_data)
    lambda_function.get_average_macros(df)
    return df


def test_speed(function, runs=10):
    times = []
    for i in range(runs):
        start = time.perf_counter()
        df = function()
        times.append((time.perf_counter() - start) * 1000)
    average_time = sum(times) / len(times)
    memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    return average_time, memory


old_time, old_memory = test_speed(old_version)
new_time, new_memory = test_speed(new_version)

print("Benchmark run at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(f"Old version: {old_time:.1f} ms, {old_memory:.2f} MB of memory")
print(f"New version: {new_time:.1f} ms, {new_memory:.2f} MB of memory")
print(f"Time saved: {(1 - new_time / old_time) * 100:.0f}%")
print(f"Memory saved: {(1 - new_memory / old_memory) * 100:.0f}%")
