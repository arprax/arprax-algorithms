from .profiler.profiler import ArpraxProfiler
from .utils.generators import random_array, sorted_array, reverse_sorted_array
from . import algorithms

# Explicitly defining what is available for "from arprax_algorithms import *"
__all__ = [
    "ArpraxProfiler",
    "random_array",
    "sorted_array",
    "reverse_sorted_array",
    "algorithms"
]