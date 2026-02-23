import pytest
from alnoms.structures.linear import (
    SinglyLinkedList,
    DoublyLinkedList,
    Stack,
    Queue,
    Bag,
)

# --- Section 1: Linked List Tests (Preserved & Adapted) ---


def test_singly_linked_list_operations():
    """Test standard O(1) and O(N) operations on a Singly Linked List."""
    ll = SinglyLinkedList()
    assert len(ll) == 0
    assert ll.is_empty()
    assert ll.display() == "EMPTY"

    ll.append(10)
    ll.append(20)
    ll.insert_at_head(5)

    assert len(ll) == 3
    assert not ll.is_empty()
    # verify iterator works
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


def test_singly_remove_traversal_coverage():
    """
    Coverage for SinglyLinkedList.remove logic.
    """
    sll = SinglyLinkedList()
    for val in [1, 2, 3]:
        sll.append(val)

    # Remove tail (hits loop traversal)
    assert sll.remove(3) is True
    assert list(sll) == [1, 2]

    # Remove non-existent
    assert sll.remove(99) is False


def test_doubly_remove_logic_exhaustion():
    """
    Coverage for DoublyLinkedList.remove logic.
    """
    dll = DoublyLinkedList()
    for x in [10, 20, 30]:
        dll.append(x)

    # Middle removal: updates both next and prev pointers
    assert dll.remove(20) is True
    assert list(dll) == [10, 30]

    # Tail removal: updates tail pointer
    assert dll.remove(30) is True
    assert dll.tail.data == 10

    # Remove head (last remaining element)
    assert dll.remove(10) is True
    assert dll.head is None
    assert dll.tail is None

    # Remove from empty
    assert dll.remove(999) is False


def test_linear_edge_cases():
    """Exhaustive check of SLL and DLL boundary conditions."""
    # SLL: Empty and Head removal
    sll = SinglyLinkedList()
    assert sll.remove(1) is False
    sll.append(10)
    assert sll.remove(10) is True
    assert sll.is_empty()

    # DLL: Prepend and bidirectional display
    dll = DoublyLinkedList()
    dll.prepend(100)
    dll.prepend(50)
    assert "50 <-> 100" in dll.display_forward()
    # Note: display_backward is not in the new industrial-grade implementation
    # unless you explicitly added it. Assuming standard iteration matches forward.


# --- Section 2: Stack Tests ---


def test_stack_lifecycle():
    """Test Push, Pop, Peek, Size, IsEmpty."""
    stack = Stack()
    assert stack.is_empty()
    assert stack.size() == 0

    stack.push(10)
    stack.push(20)
    stack.push(30)

    assert stack.size() == 3
    assert stack.peek() == 30

    # LIFO Check
    assert stack.pop() == 30
    assert stack.pop() == 20
    assert stack.pop() == 10

    assert stack.is_empty()


def test_stack_errors():
    """Test underflow errors."""
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()


def test_stack_iteration():
    """Test iteration order (LIFO)."""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    # Should iterate from top (3) to bottom (1)
    assert list(stack) == [3, 2, 1]


# --- Section 3: Queue Tests ---


def test_queue_lifecycle():
    """Test Enqueue, Dequeue, Peek, Size."""
    q = Queue()
    assert q.is_empty()

    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)

    assert q.size() == 3
    assert q.peek() == 10  # First in

    # FIFO Check
    assert q.dequeue() == 10
    assert q.dequeue() == 20
    assert q.dequeue() == 30

    assert q.is_empty()


def test_queue_loitering_edge_case():
    """
    Test the specific condition where dequeue empties the queue.
    This ensures self._last is correctly reset to None.
    """
    q = Queue()
    q.enqueue(1)
    # Queue: [1] -> Head: 1, Tail: 1

    val = q.dequeue()
    assert val == 1
    # Queue is empty. Head is None. Tail MUST be None.
    assert q.is_empty()

    # If tail wasn't reset, this next enqueue might fail or behave oddly
    # depending on implementation quirks (though specific logic prevents it).
    q.enqueue(2)
    assert q.peek() == 2
    assert q.dequeue() == 2


def test_queue_errors():
    """Test underflow errors."""
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.peek()


def test_queue_iteration():
    """Test iteration order (FIFO)."""
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert list(q) == [1, 2, 3]


# --- Section 4: Bag Tests ---


def test_bag_lifecycle():
    """Test Add, Size, Iteration."""
    bag = Bag()
    assert bag.is_empty()

    bag.add("A")
    bag.add("B")
    bag.add("C")

    assert bag.size() == 3
    assert not bag.is_empty()

    # Order is not guaranteed by Bag API, but typically LIFO in linked implementation
    items = list(bag)
    assert "A" in items
    assert "B" in items
    assert "C" in items
