"""
Arprax Algorithms: Linked List Implementations
Provides industrial-grade Singly and Doubly Linked Lists.
"""

from typing import Any, Optional, Iterator


class Node:
    """A standard node for a Singly Linked List."""

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None


class DoublyNode:
    """A node for a Doubly Linked List containing prev and next references."""

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['DoublyNode'] = None
        self.prev: Optional['DoublyNode'] = None


class SinglyLinkedList:
    """
    A foundational Singly Linked List.
    Optimized for fast O(1) insertions at the head.
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def insert_at_head(self, data: Any) -> None:
        """Inserts a new node at the beginning of the list in O(1) time."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """Appends a node to the end of the list in O(N) time."""
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

    def display(self) -> str:
        """Returns a string representation of the list."""
        elements = [str(data) for data in self]
        return " -> ".join(elements) + " -> NULL"

    def remove(self, data: Any) -> bool:
        """Removes the first occurrence of data. Returns True if successful."""
        if not self.head:  # Missing line 68-69 logic
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


class DoublyLinkedList:
    """
    An advanced Doubly Linked List.
    Allows for bidirectional traversal and easier node deletion.
    """

    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def append(self, data: Any) -> None:
        """Appends a node to the end of the list in O(1) time."""
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
        """Inserts a node at the beginning of the list in O(1) time."""
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def display_forward(self) -> str:
        """Returns a string representation from head to tail."""
        elements = [str(data) for data in self]
        return " <-> ".join(elements)

    def display_backward(self) -> str:
        """Returns a string representation from tail to head."""
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.data))
            current = current.prev
        return " <-> ".join(elements)

    def remove(self, data: Any) -> bool:
        """Removes a node from the doubly linked list in O(N) time."""
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