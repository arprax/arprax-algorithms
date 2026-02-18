# tests/test_algos/conftest.py
import pytest
from arprax.algos import Profiler  # Updated name

@pytest.fixture(scope="session")
def shared_profiler():
    """Provides a single profiler instance for the entire test session."""
    return Profiler(mode="min", warmup=0, repeats=1) # Updated name