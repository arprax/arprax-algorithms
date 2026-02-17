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
    Provides precision timing, statistical analysis, and OHPV2 complexity estimation.
    """
    def __init__(self, repeats: int = 5, warmup: int = 1, mode: str = "min"):
        self.repeats = repeats
        self.warmup = warmup
        self.mode = mode
        self._profile_stats = {}

    @contextmanager
    def stopwatch(self, label: str = "Block") -> Generator[None, None, None]:
        """Context manager for precision timing of a specific code block."""
        start = timeit.default_timer()
        try:
            yield
        finally:
            end = timeit.default_timer()
            elapsed = end - start
            if label not in self._profile_stats:
                self._profile_stats[label] = []
            self._profile_stats[label].append(elapsed)

    def benchmark(self, func: Callable, *args) -> float:
        """Runs function with GC disabled and returns the timing based on 'mode'."""
        for _ in range(self.warmup):
            safe_args = copy.deepcopy(args)
            func(*safe_args)

        times = []
        gc_old = gc.isenabled()
        gc.disable()
        try:
            for _ in range(self.repeats):
                safe_args = copy.deepcopy(args)
                start = timeit.default_timer()
                func(*safe_args)
                end = timeit.default_timer()
                times.append(end - start)
        finally:
            if gc_old:
                gc.enable()

        if self.mode == "median":
            return statistics.median(times)
        elif self.mode == "mean":
            return statistics.mean(times)
        return min(times)

    def run_doubling_test(self, func: Callable, input_gen: Callable[[int], Any],
                           start_n: int = 250, rounds: int = 6) -> List[Dict[str, Any]]:
        """Performs OHPV2 Analysis by doubling input sizes."""
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
                "N": n, "Time": curr_time, "Ratio": ratio, "Complexity": complexity
            })
            prev_time = curr_time
            n *= 2
        return results

    def profile(self, func: Callable):
        """Decorator to quick-profile any function during normal execution."""
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
        """Prints a summary of all functions tracked via @profile and stopwatch."""
        print("\n📝 ARPRAX PROFILE REPORT")
        print(f"{'Label/Function':<20} | {'Calls':<6} | {'Avg Time (s)':<12} | {'Total Time'}")
        print("-" * 65)
        for fname, times in self._profile_stats.items():
            avg_t = statistics.mean(times)
            total_t = sum(times)
            print(f"{fname:<20} | {len(times):<6} | {avg_t:<12.5f} | {total_t:.5f}")

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
        """Prints a formatted table of the doubling test results."""
        print(f"\n🔬 ANALYSIS: {func_name} (Mode: {self.mode})")
        print(f"{'N':<10} | {'Time (s)':<12} | {'Ratio':<8} | {'Est. Complexity':<15}")
        print("-" * 55)
        for row in results:
            r_str = f"{row['Ratio']:.2f}" if row['Ratio'] > 0 else "-"
            print(f"{row['N']:<10} | {row['Time']:<12.5f} | {r_str:<8} | {row['Complexity']:<15}")

    def run_stress_suite(
            self,
            funcs: Dict[str, Callable],
            input_gen: Callable[[int], Any],
            n_values: List[int] = [1000, 2000, 4000]
    ) -> Dict[int, Dict[str, float]]:
        """Runs multiple algorithms against multiple input sizes for comparison."""
        suite_results = {}
        for n in n_values:
            suite_results[n] = {}
            data = input_gen(n)
            args = data if isinstance(data, tuple) else (data,)

            for name, func in funcs.items():
                suite_results[n][name] = self.benchmark(func, *args)
        return suite_results