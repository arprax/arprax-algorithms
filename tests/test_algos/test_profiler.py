"""
Unit tests for the Arprax Profiler utility.
Ensures 100% coverage of timing, statistics, and Big O heuristics.
"""

import time
from arprax.algos.profiler import Profiler


def test_stopwatch_context_manager():
    """Verify the stopwatch accurately tracks execution time."""
    profiler = Profiler()
    label = "DB_Simulation"

    with profiler.stopwatch(label):
        time.sleep(0.02)

    assert label in profiler._profile_stats
    assert len(profiler._profile_stats[label]) == 1
    assert profiler._profile_stats[label][0] >= 0.01


def test_benchmark_modes():
    """Verify standard benchmark logic flow and default return type."""
    profiler = Profiler(repeats=3, warmup=0, mode="min")

    def dummy_func():
        return None

    result = profiler.benchmark(dummy_func)
    assert isinstance(result, float)
    assert result >= 0


def test_doubling_test_logic():
    """Verify the doubling test returns the correct structure and doubles N."""
    profiler = Profiler(repeats=1, warmup=0)

    def mock_algo(n):
        return n * n

    def mock_gen(n):
        return n

    results = profiler.run_doubling_test(mock_algo, mock_gen, start_n=10, rounds=3)

    assert len(results) == 3
    assert "N" in results[0]
    assert "Complexity" in results[0]
    assert results[1]["N"] == 20  # Verifies N *= 2


def test_profiler_decorator():
    """Verify the @profile decorator captures function timing in _profile_stats."""
    profiler = Profiler()

    @profiler.profile
    def decorated_func():
        time.sleep(0.01)
        return "done"

    val = decorated_func()
    assert val == "done"
    assert "decorated_func" in profiler._profile_stats


def test_complexity_heuristic():
    """Verify the internal _guess_complexity ratios for Big O estimation."""
    profiler = Profiler()
    # O(N) ratio is ~2.0
    assert profiler._guess_complexity(2.0) == "O(N)"
    # O(N^2) ratio is ~4.0
    assert profiler._guess_complexity(4.0) == "O(N^2)"
    # O(N^3) ratio is ~8.0
    assert profiler._guess_complexity(8.0) == "O(N^3)"
    # High growth fallback
    assert profiler._guess_complexity(15.0) == "High Growth"


def test_statistical_branches_comprehensive(shared_profiler):
    """Forces execution of median and mean branches in the benchmark method."""

    def dummy():
        pass

    # Coverage for 'median' branch
    shared_profiler.mode = "median"
    shared_profiler.benchmark(dummy)

    # Coverage for 'mean' branch
    shared_profiler.mode = "mean"
    shared_profiler.benchmark(dummy)

    # Reset to default
    shared_profiler.mode = "min"


def test_reporting_loops(shared_profiler):
    """Executes printing loops for decorator reports and doubling analysis."""
    # Populate stats for decorator report loop
    shared_profiler._profile_stats["MockAlgo"] = [0.001, 0.002]
    shared_profiler.print_decorator_report()

    # Populate data for analysis table loop
    mock_results = [
        {"N": 100, "Time": 0.05, "Ratio": 2.0, "Complexity": "O(N)"},
        {
            "N": 200,
            "Time": 0.05,
            "Ratio": 0.0,
            "Complexity": "O(1)",
        },  # Tests ratio=0 branch
    ]
    shared_profiler.print_analysis("Merge Sort", mock_results)


def test_warmup_execution():
    """Verifies that the warmup loop actually executes."""
    p = Profiler(warmup=1, repeats=1)

    # Using a list to verify the function was called during warmup
    call_count = [0]

    def count_calls():
        call_count[0] += 1

    p.benchmark(count_calls)
    # 1 warmup + 1 repeat = 2 calls
    assert call_count[0] == 2
