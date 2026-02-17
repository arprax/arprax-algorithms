import pytest
from arprax.algos.structures import SinglyLinkedList, DoublyLinkedList
from arprax.algos.algorithms import has_cycle, find_cycle_start


def test_singly_linked_list_operations():
    """Test standard O(1) and O(N) operations on a Singly Linked List."""
    ll = SinglyLinkedList()
    assert len(ll) == 0

    ll.append(10)
    ll.append(20)
    ll.insert_at_head(5)

    assert len(ll) == 3
    assert list(ll) == [5, 10, 20]  # Tests the __iter__ dunder method


def test_doubly_linked_list_operations():
    """Test bidirectional operations on a Doubly Linked List."""
    dll = DoublyLinkedList()
    dll.append(100)
    dll.prepend(50)

    assert len(dll) == 2
    assert list(dll) == [50, 100]
    assert dll.tail.data == 100
    assert dll.head.data == 50


def test_cycle_detection_and_resolution():
    """Test Floyd's Tortoise and Hare algorithm."""
    ll = SinglyLinkedList()
    for i in range(1, 6):
        ll.append(i)

    # 1. No cycle should exist yet
    assert has_cycle(ll.head) is False
    assert find_cycle_start(ll.head) is None

    # 2. Create a cycle: Node(5) points back to Node(3)
    # List: 1 -> 2 -> 3 -> 4 -> 5 -> (back to 3)
    node_3 = ll.head.next.next
    node_5 = ll.head.next.next.next.next
    node_5.next = node_3

    # 3. Test cycle detection
    assert has_cycle(ll.head) is True
    cycle_start = find_cycle_start(ll.head)
    assert cycle_start is not None
    assert cycle_start.data == 3


def test_linear_edge_cases():
    from arprax.algos.structures.linear import SinglyLinkedList, DoublyLinkedList

    # Singly Linked List Gaps
    sll = SinglyLinkedList()
    assert sll.remove(99) is False  # Hits empty list branch

    sll.append(10)
    sll.append(20)
    assert sll.remove(10) is True  # Hits head deletion
    assert sll.remove(20) is True  # Hits tail deletion

    # Doubly Linked List Gaps
    dll = DoublyLinkedList()
    dll.append(100)
    dll.append(200)
    dll.append(300)
    assert dll.remove(200) is True  # Hits mid-node deletion
    assert dll.remove(300) is True  # Hits tail deletion (updates self.tail)


def test_linear_exhaustive():
    from arprax.algos.structures.linear import SinglyLinkedList, DoublyLinkedList

    # 1. Singly Linked List Gaps
    sll = SinglyLinkedList()
    assert sll.remove(99) is False  # Line 68-69: Empty list
    sll.append(10)
    assert sll.remove(10) is True  # Line 71-74: Head removal
    sll.append(20)
    sll.append(30)
    assert sll.remove(30) is True  # Line 81-88: Mid/Tail removal
    assert "20 -> NULL" in sll.display()  # Line 61-63: Display logic

    # 2. Doubly Linked List Gaps
    dll = DoublyLinkedList()
    dll.prepend(100)  # Line 128-129: Prepend empty
    dll.prepend(50)  # Line 131-134: Prepend existing

    dll.append(200)
    assert dll.remove(50) is True  # Line 152-155: Head removal (updates dll.head)
    assert dll.remove(200) is True  # Line 158: Tail removal (updates dll.tail)

    # Line 143-148: Forward/Backward display
    assert "100" in dll.display_forward()
    assert "100" in dll.display_backward()


def test_remove_not_found():
    from arprax.algos.structures.linear import SinglyLinkedList, DoublyLinkedList

    # Hits Lines 87-88: Value not in Singly List
    sll = SinglyLinkedList()
    sll.append(1)
    assert sll.remove(999) is False

    # Hits Line 168: Value not in Doubly List
    dll = DoublyLinkedList()
    dll.append(1)
    assert dll.remove(999) is False

def test_singly_remove_final_line():
    from arprax.algos.structures.linear import SinglyLinkedList
    sll = SinglyLinkedList()
    sll.append(1)
    sll.append(2)
    # This must fail to find the value and skip the head check to hit Line 87
    assert sll.remove(999) is False