# Location: arprax-algorithms/demo_profiler.py
from arprax.algos import Profiler  # Updated name and path
from arprax.algos.utils import random_array  # Updated path
from arprax.algos.algorithms import sorting  # Better explicit access

# 1. Initialize the industrial profiler
profiler = Profiler(mode="min") # Renamed from ArpraxProfiler

# 2. Define the battle participants
contestants = {
    "Bubble Sort": sorting.bubble_sort, # Using the lifted API
    "Merge Sort": sorting.merge_sort
}

# 3. Run the battle for different N sizes
n_sizes = [500, 1000, 2000]
battle_results = profiler.run_stress_suite(
    contestants,
    random_array, # Using the imported generator function directly
    n_values=n_sizes
)

# 4. Print results
print(f"{'N':<10} | {'Bubble Sort (s)':<15} | {'Merge Sort (s)':<15}")
print("-" * 45)
for n in n_sizes:
    b_time = battle_results[n]['Bubble Sort']
    m_time = battle_results[n]['Merge Sort']
    print(f"{n:<10} | {b_time:<15.5f} | {m_time:<15.5f}")