"""
Arprax Algorithms: Linear Data Structures
Provides industrial-grade Singly and Doubly Linked Lists with generator support for visualization.
"""

from typing import Any, Optional, Iterator, Generator


class Node:
    """
    A standard node for a Singly Linked List.

    Attributes:
        data (Any): The value stored in the node.
        next (Optional[Node]): Reference to the next node in the sequence.
    """

    def __init__(self, data: Any):
        """Initializes a new Singly Linked List node."""
        self.data = data
        self.next: Optional["Node"] = None


class DoublyNode:
    """
    A node for a Doubly Linked List containing prev and next references.

    Attributes:
        data (Any): The value stored in the node.
        next (Optional[DoublyNode]): Reference to the next node.
        prev (Optional[DoublyNode]): Reference to the previous node.
    """

    def __init__(self, data: Any):
        """Initializes a new Doubly Linked List node."""
        self.data = data
        self.next: Optional["DoublyNode"] = None
        self.prev: Optional["DoublyNode"] = None


class SinglyLinkedList:
    """
    A foundational Singly Linked List.
    Optimized for fast O(1) insertions at the head and linear traversals.
    """

    def __init__(self):
        """Initializes an empty Singly Linked List with a head pointer and size counter."""
        self.head: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Returns the current number of nodes in the list in O(1) time."""
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

    def traverse(self) -> Generator[Optional[Node], None, None]:
        """
        Yields the actual Node objects for visualization purposes.

        Complexity: O(N)

        Yields:
            Optional[Node]: The current node being visited during a traversal.
        """
        current = self.head
        while current:
            yield current
            current = current.next

    def insert_at_head(self, data: Any) -> None:
        """
        Inserts a new node at the beginning of the list.

        Complexity: O(1)

        Args:
            data (Any): The data to store in the new node.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """
        Appends a node to the very end of the list.

        Complexity: O(N) because it must traverse to find the last node.

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

    def display(self) -> str:
        """
        Returns a string representation of the list for debugging.

        Returns:
            str: A formatted string like '1 -> 2 -> NULL'.
        """
        elements = [str(data) for data in self]
        return " -> ".join(elements) + " -> NULL" if elements else "EMPTY"

    def remove(self, data: Any) -> bool:
        """
        Removes the first occurrence of a specific value from the list.

        Complexity: O(N)

        Args:
            data (Any): The value to search for and remove.

        Returns:
            bool: True if the element was found and removed, False otherwise.
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


class DoublyLinkedList:
    """
    An advanced Doubly Linked List.
    Supports bidirectional traversal and O(1) tail operations.
    """

    def __init__(self):
        """Initializes an empty list with head, tail, and size attributes."""
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        """Returns the total node count in O(1) time."""
        return self._size

    def __iter__(self) -> Iterator[Any]:
        """
        Iterates through the list in forward direction (Head to Tail).

        Yields:
            Any: The data stored in each node.
        """
        current = self.head
        while current:
            yield current.data
            current = current.next

    def append(self, data: Any) -> None:
        """
        Appends a node to the end of the list.

        Complexity: O(1) because we maintain a tail pointer.

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
        Inserts a node at the very beginning of the list.

        Complexity: O(1)

        Args:
            data (Any): The data to prepend at the head.
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

    def display_forward(self) -> str:
        """
        Returns a string representation from head to tail.

        Returns:
            str: Elements separated by bidirectional arrows.
        """
        elements = [str(data) for data in self]
        return " <-> ".join(elements) if elements else "EMPTY"

    def display_backward(self) -> str:
        """
        Traverses and returns a string representation from tail to head.

        Returns:
            str: Reversed list representation.
        """
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.data))
            current = current.prev
        return " <-> ".join(elements) if elements else "EMPTY"

    def remove(self, data: Any) -> bool:
        """
        Removes a specific node by value.

        Complexity: O(N) to locate the node.

        Args:
            data (Any): The value to remove.

        Returns:
            bool: True if removed, False if not found.
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
