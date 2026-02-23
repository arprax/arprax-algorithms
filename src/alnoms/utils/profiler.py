"""
Alnoms: Performance Profiling Tools
Provides precision timing and algorithmic complexity analysis for research.
"""

import timeit
import gc
import copy
import sys
import statistics
import functools
from contextlib import contextmanager
from typing import Callable, List, Dict, Any, Generator


class Profiler:
    """
    Industrial-grade performance analyzer for Arprax Lab.

    Provides precision timing, statistical analysis, and doubling-test
    complexity estimation. Designed to work without external dependencies.

    Attributes:
        repeats (int): Number of times to run each benchmark.
        warmup (int): Number of discarded runs to prime the CPU cache.
        mode (str): Statistical mode for final result ('min', 'mean', 'median').
    """

    def __init__(self, repeats: int = 5, warmup: int = 1, mode: str = "min"):
        """Initializes the Profiler with user-defined benchmark settings."""
        self.repeats = max(1, repeats)  # Ensure at least one run occurs
        self.warmup = max(0, warmup)
        self.mode = mode
        self._profile_stats = {}

    @contextmanager
    def stopwatch(self, label: str = "Block") -> Generator[None, None, None]:
        """
        Context manager for precision timing of a specific code block.

        Args:
            label (str): Name of the block for the final report.
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

    def benchmark(self, func: Callable, *args: Any) -> float:
        """
        Runs a function with garbage collection disabled to ensure timing purity.

        Args:
            func (Callable): The function to measure.
            *args (Any): Arguments to pass to the function.

        Returns:
            float: The measured time in seconds based on the 'mode' setting.
        """
        # Warmup runs (not timed)
        for _ in range(self.warmup):
            safe_args = copy.deepcopy(args)
            func(*safe_args)

        times = []
        gc_old = gc.isenabled()
        gc.disable()
        try:
            for _ in range(self.repeats):
                # Deepcopy used to ensure input data isn't pre-sorted by previous runs
                safe_args = copy.deepcopy(args)
                start = timeit.default_timer()
                func(*safe_args)
                end = timeit.default_timer()
                times.append(end - start)
        finally:
            if gc_old:
                gc.enable()

        # Branch coverage fix: ensure all statistical modes are handled
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
        rounds: int = 6,
    ) -> List[Dict[str, Any]]:
        """
        Performs doubling analysis to estimate Big O complexity.

        Args:
            func (Callable): Algorithm to analyze.
            input_gen (Callable): Function that generates data for size N.
            start_n (int): Initial input size.
            rounds (int): How many times to double N.

        Returns:
            List[Dict[str, Any]]: A log of N, Time, Ratio, and estimated Complexity.
        """
        sys.setrecursionlimit(max(3000, sys.getrecursionlimit()))
        results = []
        prev_time = 0.0
        n = start_n

        for _ in range(rounds):
            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)
            curr_time = self.benchmark(func, *args)

            # Ratio is T(2N) / T(N). prev_time > 0 triggers the second round branch.
            ratio = curr_time / prev_time if prev_time > 0 else 0.0
            complexity = self._guess_complexity(ratio)

            results.append(
                {"N": n, "Time": curr_time, "Ratio": ratio, "Complexity": complexity}
            )
            prev_time = curr_time
            n *= 2
        return results

    def profile(self, func: Callable) -> Callable:
        """
        Decorator to track function execution time during normal program flow.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The wrapped function.
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

    def print_decorator_report(self) -> None:
        """Prints a summary table of all tracked functions and stopwatch blocks."""
        print("\n📝 ARPRAX PROFILE REPORT")
        print(
            f"{'Label/Function':<20} | {'Calls':<6} | {'Avg Time (s)':<12} | {'Total Time'}"
        )
        print("-" * 65)
        for fname, times in self._profile_stats.items():
            # statistics.mean requires at least one data point
            avg_t = statistics.mean(times) if times else 0.0
            total_t = sum(times)
            print(f"{fname:<20} | {len(times):<6} | {avg_t:<12.5f} | {total_t:.5f}")

    def _guess_complexity(self, ratio: float) -> str:
        """
        Heuristic to map doubling ratios to Big O notations.
        Ranges widened slightly to accommodate CPU frequency scaling and jitter.

        Args:
            ratio (float): The ratio of T(2N) / T(N).

        Returns:
            str: The guessed complexity string.
        """
        if ratio <= 0:
            return "Initial Round"
        if ratio < 1.4:
            return "O(1) / O(log N)"
        if ratio < 2.8:
            return "O(N)"
        if ratio < 5.5:
            return "O(N^2)"
        if ratio < 10.0:
            return "O(N^3)"
        return "High Growth / Exponential"

    def print_analysis(self, func_name: str, results: List[Dict[str, Any]]) -> None:
        """
        Prints a formatted results table from a doubling test.

        Args:
            func_name (str): Name of the analyzed algorithm.
            results (List[Dict]): Data from run_doubling_test.
        """
        print(f"\n🔬 ANALYSIS: {func_name} (Mode: {self.mode})")
        print(f"{'N':<10} | {'Time (s)':<12} | {'Ratio':<8} | {'Est. Complexity':<15}")
        print("-" * 55)
        for row in results:
            r_str = f"{row['Ratio']:.2f}" if row["Ratio"] > 0 else "-"
            print(
                f"{row['N']:<10} | {row['Time']:<12.5f} | {r_str:<8} | {row['Complexity']:<15}"
            )

    def run_stress_suite(
        self,
        funcs: Dict[str, Callable],
        input_gen: Callable[[int], Any],
        n_values: List[int] = [1000, 2000, 4000],
    ) -> Dict[int, Dict[str, float]]:
        """
        Runs multiple algorithms against multiple input sizes for head-to-head comparison.

        Args:
            funcs (Dict): Map of {'Name': Function}.
            input_gen (Callable): Data generator function.
            n_values (List[int]): List of N sizes to test.

        Returns:
            Dict[int, Dict[str, float]]: Nested mapping of {N: {Name: Time}}.
        """
        suite_results = {}
        for n in n_values:
            suite_results[n] = {}
            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)

            for name, func in funcs.items():
                suite_results[n][name] = self.benchmark(func, *args)
        return suite_results
