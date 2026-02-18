from arprax.algos.utils.profiler import Profiler


def test_benchmark_modes():
    """Hits lines 82->86 by testing all statistical modes."""

    def work():
        return None

    for mode in ["min", "mean", "median"]:
        p = Profiler(repeats=3, mode=mode)
        assert p.benchmark(work) >= 0


def test_full_doubling_logic():
    """Hits lines 143-154 and line 151 (the ratio branch)."""
    p = Profiler(repeats=1, warmup=0)

    # Simple linear work to produce a measurable ratio
    def mock_algo(n):
        return sum(range(n))

    def mock_gen(n):
        return n

    # Must use rounds >= 2 to trigger the 'prev_time > 0' branch (Line 151)
    results = p.run_doubling_test(mock_algo, mock_gen, start_n=100, rounds=2)

    assert len(results) == 2
    assert results[0]["Ratio"] == 0.0
    assert results[1]["Ratio"] >= 0.0


def test_reporting_and_decorators():
    """Hits lines 200-205 by tracking a decorated function and printing."""
    p = Profiler()

    @p.profile
    def sample_task(n):
        return n * 2

    sample_task(10)

    # This call triggers the loop and printing in lines 200-205
    p.print_decorator_report()

    # Also test print_analysis for coverage of the doubling test display
    mock_res = [{"N": 10, "Time": 0.1, "Ratio": 2.0, "Complexity": "O(N)"}]
    p.print_analysis("SampleTask", mock_res)


def test_complexity_heuristic_sweep():
    """Hits lines 226-234 by testing every if/elif/else branch."""
    p = Profiler()
    # Initial round
    assert p._guess_complexity(0) == "Initial Round"
    # O(log N)
    assert p._guess_complexity(1.2) == "O(1) / O(log N)"
    # O(N)
    assert p._guess_complexity(2.0) == "O(N)"
    # O(N^2)
    assert p._guess_complexity(4.0) == "O(N^2)"
    # O(N^3)
    assert p._guess_complexity(8.0) == "O(N^3)"
    # High Growth
    assert p._guess_complexity(15.0) == "High Growth / Exponential"


def test_stopwatch_internal_logic():
    """Covers label initialization and appending to existing lists."""
    p = Profiler()
    # First time initializes the label list
    with p.stopwatch("Task"):
        pass
    # Second time appends to it
    with p.stopwatch("Task"):
        pass
    assert len(p._profile_stats["Task"]) == 2


def test_stress_suite_and_gc_restoration():
    """
    Covers the run_stress_suite method and ensures GC restoration
    logic in benchmark() is executed.
    """
    p = Profiler(repeats=1, warmup=0)

    # 1. Test run_stress_suite (Covers the nested loops and data tuple logic)
    funcs = {"Linear": lambda n: sum(range(n))}

    def mock_gen(n):
        return (n,)  # Returns a tuple to trigger the 'isinstance' branch

    results = p.run_stress_suite(funcs, mock_gen, n_values=[10, 20])
    assert 10 in results
    assert "Linear" in results[10]

    # 2. Test GC restoration (Covers 'if gc_old: gc.enable()')
    # We ensure GC is enabled before the call to trigger that specific branch
    import gc

    gc.enable()
    p.benchmark(lambda: None)
    assert gc.isenabled()


def test_decorator_recall_logic():
    """
    Covers the decorator branch where the function name already exists
    in the profile stats dictionary.
    """
    p = Profiler()

    @p.profile
    def repeat_me():
        return True

    # First call: triggers 'if func.__name__ not in self._profile_stats'
    repeat_me()
    # Second call: triggers the 'else' path (appending to existing list)
    repeat_me()

    assert len(p._profile_stats["repeat_me"]) == 2


def test_benchmark_statistical_modes_coverage():
    """
    Surgically targets the branch at lines 82->86.
    Ensures mean and median paths in benchmark() are fully covered.
    """

    def dummy_task():
        return True

    # 1. Test 'mean' mode
    p_mean = Profiler(mode="mean", repeats=3)
    result_mean = p_mean.benchmark(dummy_task)
    assert isinstance(result_mean, float)

    # 2. Test 'median' mode
    p_median = Profiler(mode="median", repeats=3)
    result_median = p_median.benchmark(dummy_task)
    assert isinstance(result_median, float)
