"""
Arprax Algorithms: Linear Data Structures.

This module provides fundamental linear data structures optimized for performance.
It includes node-based implementations of Lists, Stacks, Queues, and Bags to
ensure O(1) time complexity for core operations, avoiding the overhead of
dynamic array resizing found in standard Python lists.

Classes:
    1. SinglyLinkedList: Basic node-based list (Forward traversal).
    2. DoublyLinkedList: Bidirectional node-based list.
    3. Stack: LIFO (Last-In First-Out) structure.
    4. Queue: FIFO (First-In First-Out) structure.
    5. Bag: Unordered collection for collecting items.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 1.3.
"""

from typing import Any, Optional, Iterator, TypeVar, Generic

T = TypeVar("T")


class Node:
    """
    A standard node for Singly Linked structures.

    Attributes:
        data (Any): The value stored in the node.
        next (Optional[Node]): Reference to the next node in the sequence.
    """

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional["Node"] = None


class DoublyNode:
    """
    A node for Doubly Linked structures.

    Attributes:
        data (Any): The value stored in the node.
        next (Optional[DoublyNode]): Reference to the next node.
        prev (Optional[DoublyNode]): Reference to the previous node.
    """

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional["DoublyNode"] = None
        self.prev: Optional["DoublyNode"] = None


# --- Section 1: Linked Lists ---


class SinglyLinkedList:
    """
    A foundational Singly Linked List.
    Optimized for fast O(1) insertions at the head and linear traversals.
    """

    def __init__(self):
        """Initializes an empty Singly Linked List."""
        self.head: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """
        Iterates through the list data from head to tail.

        Yields:
            Any: The data stored in each node.
        """
        current = self.head
        while current:
            yield current.data
            current = current.next

    def is_empty(self) -> bool:
        """Returns True if the list contains no elements."""
        return self.head is None

    def insert_at_head(self, data: Any) -> None:
        """
        Inserts a new node at the beginning of the list.

        Time Complexity: O(1)

        Args:
            data (Any): The data to store.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """
        Appends a node to the very end of the list.

        Time Complexity: O(N)

        Args:
            data (Any): The data to append.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self._size += 1
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        self._size += 1

    def remove(self, data: Any) -> bool:
        """
        Removes the first occurrence of a specific value from the list.

        Time Complexity: O(N)

        Args:
            data (Any): The value to remove.

        Returns:
            bool: True if removed, False otherwise.
        """
        if not self.head:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def display(self) -> str:
        """
        Returns a string representation of the list for debugging.

        Returns:
            str: Format '1 -> 2 -> NULL'.
        """
        elements = [str(data) for data in self]
        return " -> ".join(elements) + " -> NULL" if elements else "EMPTY"


class DoublyLinkedList:
    """
    An advanced Doubly Linked List.
    Supports bidirectional traversal and O(1) tail operations.
    """

    def __init__(self):
        """Initializes an empty Doubly Linked List."""
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """Iterates through the list from Head to Tail."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def is_empty(self) -> bool:
        """Returns True if the list contains no elements."""
        return self.head is None

    def append(self, data: Any) -> None:
        """
        Appends a node to the end of the list.

        Time Complexity: O(1)

        Args:
            data (Any): The data to append.
        """
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            if self.tail:
                self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def prepend(self, data: Any) -> None:
        """
        Inserts a node at the beginning of the list.

        Time Complexity: O(1)

        Args:
            data (Any): The data to prepend.
        """
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def remove(self, data: Any) -> bool:
        """
        Removes the first occurrence of a specific value.

        Time Complexity: O(N)

        Args:
            data (Any): The value to remove.

        Returns:
            bool: True if removed, False otherwise.
        """
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                self._size -= 1
                return True
            current = current.next
        return False

    def display_forward(self) -> str:
        """Returns a string representation from Head to Tail."""
        elements = [str(data) for data in self]
        return " <-> ".join(elements) if elements else "EMPTY"


# --- Section 2: Fundamental Abstract Data Types ---


class Bag(Generic[T]):
    """
    A collection where removing items is not supported.
    Its purpose is to provide the ability to collect items and then iterate over them.

    Time Complexity:
        add: O(1)
        iterate: O(N)
    """

    def __init__(self):
        """Initializes an empty Bag."""
        self._first: Optional[Node] = None
        self._n: int = 0

    def is_empty(self) -> bool:
        """Returns True if the bag is empty."""
        return self._first is None

    def size(self) -> int:
        """Returns the number of items in the bag."""
        return self._n

    def add(self, item: T) -> None:
        """
        Adds an item to the bag.

        Args:
            item (T): The item to add.
        """
        old_first = self._first
        self._first = Node(item)
        self._first.next = old_first
        self._n += 1

    def __iter__(self) -> Iterator[T]:
        """Iterates over the items in the bag (order is LIFO but irrelevant)."""
        current = self._first
        while current:
            yield current.data
            current = current.next


class Stack(Generic[T]):
    """
    A LIFO (Last-In First-Out) stack.
    Implemented using a linked list to ensure O(1) worst-case time for push/pop,
    avoiding the resizing overhead of array-based stacks.
    """

    def __init__(self):
        """Initializes an empty Stack."""
        self._first: Optional[Node] = None
        self._n: int = 0

    def is_empty(self) -> bool:
        """Returns True if the stack is empty."""
        return self._first is None

    def size(self) -> int:
        """Returns the number of items in the stack."""
        return self._n

    def push(self, item: T) -> None:
        """
        Adds an item to the top of the stack.

        Time Complexity: O(1)

        Args:
            item (T): The item to push.
        """
        old_first = self._first
        self._first = Node(item)
        self._first.next = old_first
        self._n += 1

    def pop(self) -> T:
        """
        Removes and returns the item most recently added to the stack.

        Time Complexity: O(1)

        Returns:
            T: The item from the top of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack underflow")

        item = self._first.data
        self._first = self._first.next
        self._n -= 1
        return item

    def peek(self) -> T:
        """
        Returns the item at the top of the stack without removing it.

        Returns:
            T: The item at the top.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Stack underflow")
        return self._first.data

    def __iter__(self) -> Iterator[T]:
        """Iterates from top to bottom."""
        current = self._first
        while current:
            yield current.data
            current = current.next


class Queue(Generic[T]):
    """
    A FIFO (First-In First-Out) queue.
    Maintains pointers to both head (first) and tail (last) to ensure
    O(1) enqueue and dequeue operations.
    """

    def __init__(self):
        """Initializes an empty Queue."""
        self._first: Optional[Node] = None  # Beginning of queue
        self._last: Optional[Node] = None  # End of queue
        self._n: int = 0

    def is_empty(self) -> bool:
        """Returns True if the queue is empty."""
        return self._first is None

    def size(self) -> int:
        """Returns the number of items in the queue."""
        return self._n

    def enqueue(self, item: T) -> None:
        """
        Adds an item to the end of the queue.

        Time Complexity: O(1)

        Args:
            item (T): The item to add.
        """
        old_last = self._last
        self._last = Node(item)
        self._last.next = None

        if self.is_empty():
            self._first = self._last
        else:
            old_last.next = self._last
        self._n += 1

    def dequeue(self) -> T:
        """
        Removes and returns the item least recently added to the queue.

        Time Complexity: O(1)

        Returns:
            T: The item from the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue underflow")

        item = self._first.data
        self._first = self._first.next
        self._n -= 1

        if self.is_empty():
            self._last = None  # Avoid loitering

        return item

    def peek(self) -> T:
        """
        Returns the item at the front of the queue without removing it.

        Returns:
            T: The item at the front.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue underflow")
        return self._first.data

    def __iter__(self) -> Iterator[T]:
        """Iterates from front to back."""
        current = self._first
        while current:
            yield current.data
            current = current.next
