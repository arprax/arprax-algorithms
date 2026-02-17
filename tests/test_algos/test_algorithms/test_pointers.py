from arprax.algos.algorithms import has_cycle, find_cycle_start
from arprax.algos.structures.linear import SinglyLinkedList

def test_no_cycle():
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    # Line 24/53 is likely the 'return False' when no cycle exists
    assert has_cycle(sll.head) is False


def test_no_cycle_execution():
    sll = SinglyLinkedList()
    sll.append(1)
    # Hits the return False/None when fast pointer hits null (Lines 24, 53)
    assert has_cycle(sll.head) is False
    assert find_cycle_start(sll.head) is None