import time
from arprax_algorithms import ArpraxProfiler


def test_stopwatch_context_manager():
    """Verify the stopwatch accurately tracks execution time."""
    profiler = ArpraxProfiler()
    label = "DB_Simulation"

    with profiler.stopwatch(label):
        time.sleep(0.05)

    assert label in profiler._profile_stats
    assert len(profiler._profile_stats[label]) == 1
    # Ensure recorded time is roughly equal to or greater than the sleep time
    assert profiler._profile_stats[label][0] >= 0.04