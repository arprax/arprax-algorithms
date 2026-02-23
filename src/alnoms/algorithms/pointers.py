"""
Alnoms: Pointer Utilities
Contains two-pointer algorithms like Floyd's Cycle Detection (Tortoise & Hare).
"""

from typing import Optional
from alnoms.structures.linear import Node


def has_cycle(head: Optional[Node]) -> bool:
    """
    Detects if a Singly Linked List contains a cycle using Floyd's Tortoise and Hare algorithm.

    Time Complexity: O(N)
    Space Complexity: O(1)

    Args:
        head (Node): The head node of the linked list.

    Returns:
        bool: True if a cycle exists, False otherwise.
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next  # Tortoise moves 1 step
        fast = fast.next.next  # Hare moves 2 steps

        if slow is fast:  # They meet!
            return True

    return False


def find_cycle_start(head: Optional[Node]) -> Optional[Node]:
    """
    Locates the exact node where a cycle begins in a Singly Linked List.

    Time Complexity: O(N)
    Space Complexity: O(1)

    Args:
        head (Node): The head node of the linked list.

    Returns:
        Node: The node where the cycle begins, or None if no cycle exists.
    """
    if not head or not head.next:
        return None

    slow = head
    fast = head
    cycle_exists = False

    # Phase 1: Detect Cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            cycle_exists = True
            break

    if not cycle_exists:
        return None

    # Phase 2: Find the starting node
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next

    return slow
