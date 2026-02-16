import timeit
import gc
import copy
import sys
import statistics
import functools
from contextlib import contextmanager
from typing import Callable, List, Dict, Any, Generator


class ArpraxProfiler:
    def __init__(self, repeats: int = 5, warmup: int = 1, mode: str = "min"):
        """
        Initializes the industrial profiler.

        Args:
            repeats (int): Number of runs per benchmark.
            warmup (int): Warmup runs to stabilize CPU cache.
            mode (str): 'min' (noise-free), 'mean' (statistical), or 'median' (robust).
        """
        self.repeats = repeats
        self.warmup = warmup
        self.mode = mode
        self._profile_stats = {}

    @contextmanager
    def stopwatch(self, label: str = "Block") -> Generator[None, None, None]:
        """
        Context manager for precision timing of a specific code block.

        Example:
            with profiler.stopwatch("Database Query"):
                # run expensive code here
        """
        start = timeit.default_timer()
        try:
            yield
        finally:
            end = timeit.default_timer()
            elapsed = end - start

            if label not in self._profile_stats:
                self._profile_stats[label] = []
            self._profile_stats[label].append(elapsed)

            print(f"⏱️ [{label}] execution time: {elapsed:.6f}s")

    def benchmark(self, func: Callable, *args) -> float:
        """
        Runs the function with GC disabled and returns the timing based on 'mode'.

        Args:
            func (Callable): The function to analyze.
            *args: Arguments to pass to the function.

        Returns:
            float: The measured time in seconds.
        """
        # 1. WARMUP: Stabilize JIT and CPU cache
        for _ in range(self.warmup):
            safe_args = copy.deepcopy(args)
            func(*safe_args)

        times = []
        gc_old = gc.isenabled()
        gc.disable()

        try:
            for _ in range(self.repeats):
                # Critical: Deepcopy ensures sorting algorithms don't run on sorted data
                safe_args = copy.deepcopy(args)

                start = timeit.default_timer()
                func(*safe_args)
                end = timeit.default_timer()

                times.append(end - start)
        finally:
            if gc_old:
                gc.enable()

        # 2. STATISTICAL MODES
        if self.mode == "median":
            return statistics.median(times)
        elif self.mode == "mean":
            return statistics.mean(times)
        return min(times)

    def run_doubling_test(
            self,
            func: Callable,
            input_gen: Callable[[int], Any],
            start_n: int = 250,
            rounds: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Performs OHPV2 Analysis by doubling input sizes and measuring time ratios.

        Args:
            func (Callable): Target function to profile.
            input_gen (Callable): Generator that returns data given an N.
            start_n (int): Initial input size.
            rounds (int): How many times to double N.

        Returns:
            List[Dict[str, Any]]: List of results with N, Time, Ratio, and Complexity.
        """
        sys.setrecursionlimit(max(3000, sys.getrecursionlimit()))
        results = []
        prev_time = 0
        n = start_n

        for _ in range(rounds):
            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)

            curr_time = self.benchmark(func, *args)
            ratio = curr_time / prev_time if prev_time > 0 else 0.0
            complexity = self._guess_complexity(ratio)

            results.append({
                "N": n,
                "Time": curr_time,
                "Ratio": ratio,
                "Complexity": complexity
            })

            prev_time = curr_time
            n *= 2

        return results

    def run_stress_suite(
            self,
            funcs: Dict[str, Callable],
            input_gen: Callable[[int], Any],
            n_values: List[int] = [1000, 2000, 4000]
    ) -> Dict[int, Dict[str, float]]:
        """
        Runs multiple algorithms against multiple input sizes for a 'battle' comparison.

        Args:
            funcs (Dict[str, Callable]): Dictionary of algorithm names and functions.
            input_gen (Callable): Input generator function.
            n_values (List[int]): List of N values to test.

        Returns:
            Dict: Nested dictionary containing timing results for each N.
        """
        suite_results = {}
        for n in n_values:
            suite_results[n] = {}
            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)

            for name, func in funcs.items():
                suite_results[n][name] = self.benchmark(func, *args)
        return suite_results

    def profile(self, func: Callable):
        """
        Decorator to quick-profile any function during normal execution.

        Args:
            func (Callable): The function to wrap.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = timeit.default_timer()
            result = func(*args, **kwargs)
            end = timeit.default_timer()

            elapsed = end - start
            if func.__name__ not in self._profile_stats:
                self._profile_stats[func.__name__] = []
            self._profile_stats[func.__name__].append(elapsed)

            return result

        return wrapper

    def print_decorator_report(self):
        """Prints a summary of all functions tracked via the @profile decorator and stopwatch."""
        print("\n📝 DECORATOR & STOPWATCH PROFILE REPORT")
        print(f"{'Label/Function':<20} | {'Calls':<6} | {'Avg Time (s)':<12} | {'Total Time'}")
        print("-" * 55)
        for fname, times in self._profile_stats.items():
            avg_t = statistics.mean(times)
            total_t = sum(times)
            print(f"{fname:<20} | {len(times):<6} | {avg_t:<12.5f} | {total_t:.5f}")

    def plot_analysis(self, results: List[Dict[str, Any]], title: str = "Algorithm Growth"):
        """
        Visualizes N vs Time from doubling test results using Matplotlib.

        Args:
            results (List[Dict]): Data from run_doubling_test.
            title (str): Title of the generated chart.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("⚠️ Matplotlib not found. Install it to enable plotting: pip install matplotlib")
            return

        ns = [row['N'] for row in results]
        times = [row['Time'] for row in results]

        plt.figure(figsize=(10, 6))
        plt.plot(ns, times, marker='o', linestyle='-', color='#008080', label='Measured Time')

        plt.title(f"Arprax Analysis: {title}")
        plt.xlabel("Input Size (N)")
        plt.ylabel("Time (seconds)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

    def _guess_complexity(self, ratio: float) -> str:
        """Internal heuristic to determine Big O based on doubling ratios."""
        if ratio < 1.4:
            return "O(1) / O(log N)"
        if 1.6 <= ratio <= 2.5:
            return "O(N)"
        if 3.5 <= ratio <= 4.8:
            return "O(N^2)"
        if 7.0 <= ratio <= 9.0:
            return "O(N^3)"
        return "High Growth"

    def print_analysis(self, func_name: str, results: List[Dict[str, Any]]):
        """
        Prints a formatted table of the doubling test results.

        Args:
            func_name (str): Name of the function analyzed.
            results (List[Dict]): Data from the doubling test.
        """
        print(f"\n🔬 ANALYSIS: {func_name} (Mode: {self.mode})")
        print(f"{'N':<10} | {'Time (s)':<12} | {'Ratio':<8} | {'Est. Complexity':<15}")
        print("-" * 55)
        for row in results:
            r_str = f"{row['Ratio']:.2f}" if row['Ratio'] > 0 else "-"
            print(f"{row['N']:<10} | {row['Time']:<12.5f} | {r_str:<8} | {row['Complexity']:<15}")


# ==========================================
# 🧪 DEMO USAGE
# ==========================================
if __name__ == "__main__":
    import random
    import time

    profiler = ArpraxProfiler(mode="min")

    # --- 1. Stopwatch Test ---
    print("--- 1. Stopwatch Context Manager ---")
    with profiler.stopwatch("Data Loading Simulation"):
        time.sleep(0.1)  # Simulate loading 100k records

    with profiler.stopwatch("Data Processing Simulation"):
        time.sleep(0.05)  # Simulate processing those records


    # --- 2. Doubling Test (Multi-Arg) ---
    def two_sum(arr, target):
        for x in arr:
            if x == target:
                return True
        return False


    def two_sum_gen(n):
        # Returns TUPLE: (arr, target)
        return ([random.randint(0, 100) for _ in range(n)], -1)


    print("\n--- 2. Doubling Test (Multi-Arg) ---")
    results = profiler.run_doubling_test(two_sum, two_sum_gen, rounds=5)
    profiler.print_analysis("Two Sum", results)

    # --- 3. Decorator Test ---
    print("\n--- 3. Decorator Test ---")


    @profiler.profile
    def sleepy_algo(x):
        time.sleep(x)


    sleepy_algo(0.1)
    sleepy_algo(0.1)

    # Note how the report now includes BOTH the decorated functions AND the stopwatch blocks!
    profiler.print_decorator_report()