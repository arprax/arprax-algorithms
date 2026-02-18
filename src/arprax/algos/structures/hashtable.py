"""
Hash Table Implementations.

This module provides two standard hash table implementations for key-value storage:
1. SeparateChainingHashST: Uses a list of buckets to handle collisions.
2. LinearProbingHashST: Uses open addressing (probing) to handle collisions.

Features:
    - Generic Key-Value storage (Keys must be hashable).
    - Dynamic resizing (LinearProbing) to maintain O(1) average performance.
    - Efficient lookups, insertions, and deletions.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Section 3.4.
"""

from typing import Any, List, Optional, Tuple


class SeparateChainingHashST:
    """
    Symbol table implementation using a hash table with separate chaining.

    Each bucket contains a simple list of (key, value) tuples.
    If M is the number of buckets, average search time is O(N/M).
    """

    def __init__(self, m: int = 997):
        """
        Initializes the hash table.

        Args:
            m (int): Number of chains (buckets). Defaults to a prime number.
        """
        self._m = m
        self._n = 0  # Number of key-value pairs
        # Create M buckets, each initialized as an empty list
        self._st: List[List[Tuple[Any, Any]]] = [[] for _ in range(m)]

    def _hash(self, key: Any) -> int:
        """Computes the hash index for a key."""
        return (hash(key) & 0x7FFFFFFF) % self._m

    def size(self) -> int:
        """Returns the number of key-value pairs."""
        return self._n

    def is_empty(self) -> int:
        """Returns True if the table is empty."""
        return self._n == 0

    def contains(self, key: Any) -> bool:
        """Returns True if the table contains the given key."""
        return self.get(key) is not None

    def get(self, key: Any) -> Optional[Any]:
        """
        Returns the value associated with the key.

        Args:
            key: The key to search for.

        Returns:
            The value if found, otherwise None.
        """
        i = self._hash(key)
        for k, v in self._st[i]:
            if k == key:
                return v
        return None

    def put(self, key: Any, val: Any) -> None:
        """
        Inserts the key-value pair into the table.

        Updates the value if the key already exists.
        If the value is None, the key is removed from the table.

        Args:
            key: The key to insert.
            val: The value to associate with the key.
        """
        if val is None:
            self.delete(key)
            return

        i = self._hash(key)
        # Search for key in bucket i
        for idx, (k, v) in enumerate(self._st[i]):
            if k == key:
                self._st[i][idx] = (key, val)  # Update
                return

        # Not found, append new pair
        self._st[i].append((key, val))
        self._n += 1

    def delete(self, key: Any) -> None:
        """
        Removes the key and its associated value from the table.

        Args:
            key: The key to remove.
        """
        i = self._hash(key)
        bucket = self._st[i]

        for idx, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[idx]
                self._n -= 1
                return

    def keys(self) -> List[Any]:
        """
        Returns all keys in the table.

        Returns:
            List[Any]: A list of all keys currently in the table.
        """
        all_keys = []
        for bucket in self._st:
            for k, _ in bucket:
                all_keys.append(k)
        return all_keys


class LinearProbingHashST:
    """
    Symbol table implementation using a hash table with linear probing.

    Uses two parallel arrays for keys and values.
    Maintains a load factor between 1/8 and 1/2 by dynamic resizing.
    """

    def __init__(self, capacity: int = 16):
        """
        Initializes the linear probing hash table.

        Args:
            capacity (int): Initial capacity of the table.
        """
        self._m = capacity  # Size of table
        self._n = 0  # Number of pairs
        self._keys: List[Optional[Any]] = [None] * capacity
        self._vals: List[Optional[Any]] = [None] * capacity

    def size(self) -> int:
        """Returns the number of key-value pairs."""
        return self._n

    def is_empty(self) -> bool:
        """Returns True if the table is empty."""
        return self._n == 0

    def contains(self, key: Any) -> bool:
        """Returns True if the table contains the given key."""
        return self.get(key) is not None

    def _hash(self, key: Any) -> int:
        """Computes the hash index for a key."""
        return (hash(key) & 0x7FFFFFFF) % self._m

    def _resize(self, capacity: int) -> None:
        """
        Resizes the table to hold the given capacity.

        Re-inserts all existing items into the new, larger (or smaller) table.

        Args:
            capacity (int): The new size of the table.
        """
        temp = LinearProbingHashST(capacity)
        for i in range(self._m):
            if self._keys[i] is not None:
                temp.put(self._keys[i], self._vals[i])

        self._keys = temp._keys
        self._vals = temp._vals
        self._m = temp._m

    def put(self, key: Any, val: Any) -> None:
        """
        Inserts the key-value pair into the table.

        Handles collisions using linear probing.
        Automatically resizes the table if the load factor exceeds 1/2.
        If val is None, the key is deleted.

        Args:
            key: The key to insert.
            val: The value to associate with the key.
        """
        if val is None:
            self.delete(key)
            return

        # Double table size if 50% full
        if self._n >= self._m // 2:
            self._resize(2 * self._m)

        i = self._hash(key)
        while self._keys[i] is not None:
            if self._keys[i] == key:
                self._vals[i] = val
                return
            i = (i + 1) % self._m

        self._keys[i] = key
        self._vals[i] = val
        self._n += 1

    def get(self, key: Any) -> Optional[Any]:
        """
        Returns the value associated with the key.

        Follows the probe sequence to find the key.

        Args:
            key: The key to search for.

        Returns:
            The value if found, otherwise None.
        """
        i = self._hash(key)
        while self._keys[i] is not None:
            if self._keys[i] == key:
                return self._vals[i]
            i = (i + 1) % self._m
        return None

    def delete(self, key: Any) -> None:
        """
        Removes the key and its associated value.

        This method employs 'Cluster Re-hashing': when a key is deleted,
        all subsequent keys in the same cluster are removed and re-inserted
        to maintain the integrity of the probe sequence.

        Args:
            key: The key to remove.
        """
        if not self.contains(key):
            return

        # Find position i of key
        i = self._hash(key)
        while self._keys[i] != key:
            i = (i + 1) % self._m

        # Delete key and value
        self._keys[i] = None
        self._vals[i] = None

        # Rehash all keys in the same cluster
        i = (i + 1) % self._m
        while self._keys[i] is not None:
            # Save key/val to re-insert
            key_to_rehash = self._keys[i]
            val_to_rehash = self._vals[i]

            # Delete position
            self._keys[i] = None
            self._vals[i] = None
            self._n -= 1

            # Re-insert (will find new correct position)
            self.put(key_to_rehash, val_to_rehash)

            i = (i + 1) % self._m

        self._n -= 1

        # Halve size if 12.5% full
        if self._n > 0 and self._n <= self._m // 8:
            self._resize(self._m // 2)

    def keys(self) -> List[Any]:
        """
        Returns all keys in the table.

        Returns:
            List[Any]: A list of all keys currently in the table.
        """
        return [k for k in self._keys if k is not None]
