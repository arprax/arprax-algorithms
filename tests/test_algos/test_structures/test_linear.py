"""
Unit tests for Arprax Linear Data Structures.
Covers Singly and Doubly Linked Lists with 100% branch coverage.
"""

from arprax.algos.structures.linear import SinglyLinkedList, DoublyLinkedList


def test_singly_linked_list_operations():
    """Test standard O(1) and O(N) operations on a Singly Linked List."""
    ll = SinglyLinkedList()
    assert len(ll) == 0
    assert ll.display() == "EMPTY"

    ll.append(10)
    ll.append(20)
    ll.insert_at_head(5)

    assert len(ll) == 3
    assert list(ll) == [5, 10, 20]


def test_doubly_linked_list_operations():
    """Test bidirectional operations on a Doubly Linked List."""
    dll = DoublyLinkedList()
    dll.append(100)
    dll.prepend(50)

    assert len(dll) == 2
    assert list(dll) == [50, 100]
    assert dll.tail.data == 100
    assert dll.head.data == 50


def test_singly_traverse_hook():
    """Verifies the generator used for Arprax Academy animations."""
    ll = SinglyLinkedList()
    ll.append(5)
    ll.append(10)

    nodes = list(ll.traverse())
    assert len(nodes) == 2
    assert nodes[0].data == 5
    assert nodes[1].data == 10


def test_singly_remove_traversal_coverage():
    """
    ULTIMATE FIX for SinglyLinkedList.remove: current = current.next.
    Forces loop increment by searching for tail or non-existent values.
    """
    sll = SinglyLinkedList()
    for val in [1, 2, 3]:
        sll.append(val)

    # Hits 'current = current.next' to move past head
    assert sll.remove(3) is True
    assert list(sll) == [1, 2]

    # Hits 'current = current.next' repeatedly until loop exits (False)
    assert sll.remove(99) is False


def test_doubly_remove_logic_exhaustion():
    """
    ULTIMATE FIX for DoublyLinkedList.remove: current = current.next.
    Targets middle removal, tail removal, and missing values.
    """
    dll = DoublyLinkedList()
    for x in [10, 20, 30]:
        dll.append(x)

    # Middle removal: forces one increment
    assert dll.remove(20) is True

    # Tail removal: forces another increment
    assert dll.remove(30) is True

    # Missing value: forces increment until current is None
    assert dll.remove(999) is False


def test_linear_edge_cases():
    """Exhaustive check of SLL and DLL boundary conditions."""
    # SLL: Empty and Head removal
    sll = SinglyLinkedList()
    assert sll.remove(1) is False
    sll.append(10)
    assert sll.remove(10) is True

    # DLL: Prepend and bidirectional display
    dll = DoublyLinkedList()
    dll.prepend(100)
    dll.prepend(50)
    assert "50 <-> 100" in dll.display_forward()
    assert "100 <-> 50" in dll.display_backward()

    # DLL: Remove only node (Nullifies head and tail)
    dll_single = DoublyLinkedList()
    dll_single.append(99)
    assert dll_single.remove(99) is True
    assert dll_single.head is None
    assert dll_single.tail is None
