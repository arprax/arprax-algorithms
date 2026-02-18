"""
String Symbol Tables (Tries).

This module provides specialized symbol table implementations where keys are strings.
Unlike generic hash tables or BSTs, these structures use the characters of the key
to guide the search, allowing for advanced operations like prefix matching.

Classes:
    1. TrieST: R-way Trie (Fastest search, high memory usage).
    2. TST: Ternary Search Trie (Balanced memory and speed, supports Unicode well).

Features:
    - O(L) search time where L is string length (independent of N keys).
    - Prefix matching (keys_with_prefix).
    - Longest prefix matching.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 5.2.
"""

from typing import Any, List, Optional


class TrieST:
    """
    R-way Trie Symbol Table.

    Uses an array of R links at every node. Fast access but consumes significant
    memory if keys are sparse or the alphabet is large.
    Default R=256 (Extended ASCII).
    """

    class _Node:
        def __init__(self, r: int):
            self.val: Optional[Any] = None
            self.next: List[Optional["TrieST._Node"]] = [None] * r

    def __init__(self, r: int = 256):
        """
        Initializes an empty R-way Trie.

        Args:
            r (int): Alphabet size. Default 256 (Extended ASCII).
        """
        self._R = r
        self._root: Optional["TrieST._Node"] = None
        self._n = 0

    def size(self) -> int:
        """Returns the number of keys in the trie."""
        return self._n

    def is_empty(self) -> bool:
        return self._n == 0

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def get(self, key: str) -> Optional[Any]:
        """
        Returns the value associated with the given string key.

        Args:
            key (str): The search key.
        """
        x = self._get(self._root, key, 0)
        if x is None:
            return None
        return x.val

    def _get(self, x: Optional[_Node], key: str, d: int) -> Optional[_Node]:
        if x is None:
            return None
        if d == len(key):
            return x
        c = ord(key[d])
        if c >= self._R:
            return None  # Character out of bounds for this Trie
        return self._get(x.next[c], key, d + 1)

    def put(self, key: str, val: Any) -> None:
        """
        Inserts key-value pair into the trie.
        """
        if val is None:
            self.delete(key)
            return
        self._root = self._put(self._root, key, val, 0)

    def _put(self, x: Optional[_Node], key: str, val: Any, d: int) -> _Node:
        if x is None:
            x = self._Node(self._R)

        if d == len(key):
            if x.val is None:
                self._n += 1
            x.val = val
            return x

        c = ord(key[d])
        if c >= self._R:
            raise ValueError(f"Character '{key[d]}' exceeds alphabet size {self._R}")

        x.next[c] = self._put(x.next[c], key, val, d + 1)
        return x

    def delete(self, key: str) -> None:
        """Removes the key and its value."""
        self._root = self._delete(self._root, key, 0)

    def _delete(self, x: Optional[_Node], key: str, d: int) -> Optional[_Node]:
        if x is None:
            return None

        if d == len(key):
            if x.val is not None:
                self._n -= 1
            x.val = None
        else:
            c = ord(key[d])
            x.next[c] = self._delete(x.next[c], key, d + 1)

        # Check if node is essentially empty (no val, no links)
        if x.val is not None:
            return x

        for link in x.next:
            if link is not None:
                return x

        return None

    def keys(self) -> List[str]:
        """Returns all keys in the trie."""
        return self.keys_with_prefix("")

    def keys_with_prefix(self, prefix: str) -> List[str]:
        """Returns all keys that start with the given prefix."""
        results: List[str] = []
        x = self._get(self._root, prefix, 0)
        self._collect(x, prefix, results)
        return results

    def _collect(self, x: Optional[_Node], prefix: str, results: List[str]) -> None:
        if x is None:
            return
        if x.val is not None:
            results.append(prefix)
        for c in range(self._R):
            if x.next[c] is not None:
                self._collect(x.next[c], prefix + chr(c), results)


class TST:
    """
    Ternary Search Trie (TST).

    A specialized trie where each node has 3 children (left, mid, right).
    More memory efficient than R-way tries for large alphabets (like Unicode).
    """

    class _Node:
        def __init__(self, c: str):
            self.c = c
            self.left: Optional["TST._Node"] = None
            self.mid: Optional["TST._Node"] = None
            self.right: Optional["TST._Node"] = None
            self.val: Optional[Any] = None

    def __init__(self, r: int = 256):  # Added r parameter
        self._R = r  # Store the limit
        self._root: Optional["TST._Node"] = None
        self._n = 0

    def size(self) -> int:
        return self._n

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def get(self, key: str) -> Optional[Any]:
        """Returns value associated with key."""
        if not key:
            raise ValueError("Key must not be empty")
        x = self._get(self._root, key, 0)
        if x is None:
            return None
        return x.val

    def _get(self, x: Optional[_Node], key: str, d: int) -> Optional[_Node]:
        if x is None:
            return None

        c = key[d]
        if c < x.c:
            return self._get(x.left, key, d)
        elif c > x.c:
            return self._get(x.right, key, d)
        elif d < len(key) - 1:
            return self._get(x.mid, key, d + 1)
        else:
            return x

    def put(self, key: str, val: Any) -> None:
        """Inserts key-value pair."""
        if not key:
            raise ValueError("Key must not be empty")

        # --- NEW VALIDATION GATE ---
        for char in key:
            if ord(char) >= self._R:
                raise ValueError(f"Character '{char}' exceeds alphabet size {self._R}")
        # ---------------------------

        self._root = self._put(self._root, key, val, 0)

    def _put(self, x: Optional[_Node], key: str, val: Any, d: int) -> _Node:
        c = key[d]
        if x is None:
            x = self._Node(c)

        if c < x.c:
            x.left = self._put(x.left, key, val, d)
        elif c > x.c:
            x.right = self._put(x.right, key, val, d)
        elif d < len(key) - 1:
            x.mid = self._put(x.mid, key, val, d + 1)
        else:
            if x.val is None:
                self._n += 1
            x.val = val
        return x

    def keys(self) -> List[str]:
        """Returns all keys."""
        results: List[str] = []
        self._collect(self._root, "", results)
        return results

    def keys_with_prefix(self, prefix: str) -> List[str]:
        """Returns keys starting with prefix."""
        if not prefix:
            return self.keys()

        results: List[str] = []
        x = self._get(self._root, prefix, 0)

        if x is None:
            return results

        # If prefix itself is a key
        if x.val is not None:
            results.append(prefix)

        # Collect everything in the middle child of the prefix end node
        self._collect(x.mid, prefix, results)
        return results

    def _collect(self, x: Optional[_Node], prefix: str, results: List[str]) -> None:
        if x is None:
            return

        self._collect(x.left, prefix, results)

        if x.val is not None:
            results.append(prefix + x.c)

        self._collect(x.mid, prefix + x.c, results)
        self._collect(x.right, prefix, results)
