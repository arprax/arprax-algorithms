"""
Core algorithms for Arprax Lab, including sorting and pointer logic.
"""
from . import sorting
from . import pointers

# Lifted Exports (The Facade Pattern)
from .sorting import merge_sort, bubble_sort
from .pointers import has_cycle, find_cycle_start

__all__ = [
    "sorting",
    "pointers",
    "merge_sort",
    "bubble_sort",
    "has_cycle",
    "find_cycle_start"
]