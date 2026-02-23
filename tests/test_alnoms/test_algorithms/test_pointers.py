"""
Unit tests for Arprax Pointer Algorithms.
Validates cycle detection and cycle start identification logic.
"""

from alnoms.algorithms import has_cycle, find_cycle_start
from alnoms.structures.linear import SinglyLinkedList


def test_no_cycle_behavior():
    """
    Verifies that standard linear lists return False/None.
    Covers the 'if not cycle_exists' early exit.
    """
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    assert has_cycle(sll.head) is False
    assert find_cycle_start(sll.head) is None


def test_cycle_start_node_index_2():
    """
    Verifies Floyd's Phase 2 identifies a cycle starting mid-list.
    This specifically targets and forces the execution of Line 68.
    """
    sll = SinglyLinkedList()
    for i in [10, 20, 30, 40, 50]:
        sll.append(i)

    # 10 -> 20 -> 30 -> 40 -> 50 -> (back to 30)
    # Cycle starts at index 2 (value 30)
    start_node = sll.head.next.next  # Node with 30
    tail_node = start_node.next.next  # Node with 50
    tail_node.next = start_node  # Close the loop

    # Phase 1 verification
    assert has_cycle(sll.head) is True

    # Phase 2 verification: This forces the slow/fast walk and Line 68 return
    detected_start = find_cycle_start(sll.head)
    assert detected_start is start_node
    assert detected_start.data == 30


def test_pointers_empty_and_single_node():
    """Ensures cycle detection handles None and single node inputs (Line 23 & 51)."""
    # Empty list
    assert has_cycle(None) is False
    assert find_cycle_start(None) is None

    # Single node (no next)
    sll = SinglyLinkedList()
    sll.append(100)
    assert has_cycle(sll.head) is False
    assert find_cycle_start(sll.head) is None
