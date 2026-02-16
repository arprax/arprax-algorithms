from arprax_algorithms.structures import SinglyLinkedList, DoublyLinkedList
from arprax_algorithms.algorithms.pointers import has_cycle, find_cycle_start


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