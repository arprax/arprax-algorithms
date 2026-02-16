from .profiler import ArpraxProfiler
from .utils import random_array, sorted_array, reverse_sorted_array
from . import algorithms
from . import structures  # <-- NEW: Exposing your milestone work!

# Explicitly defining what is available for "from arprax_algorithms import *"
__all__ = [
    "ArpraxProfiler",
    "random_array",
    "sorted_array",
    "reverse_sorted_array",
    "algorithms",
    "structures"          # <-- NEW
]