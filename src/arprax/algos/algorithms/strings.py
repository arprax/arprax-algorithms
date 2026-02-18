"""
String Processing Algorithms.

This module provides efficient algorithms for sorting strings, searching for
substring patterns, and compressing data.

Features:
    - LSD Sort: Least-Significant-Digit radix sort (Stable, for fixed-length strings).
    - MSD Sort: Most-Significant-Digit radix sort (General purpose string sort).
    - KMP Search: Knuth-Morris-Pratt substring search (Linear time, no backup).
    - Boyer-Moore: Substring search with character skipping (Sub-linear average time).
    - Huffman: Prefix-free coding for lossless compression.

Reference:
    Algorithms, 4th Edition by Sedgewick and Wayne, Chapter 5.
"""

from typing import List, Optional, Tuple, Dict
import heapq
from collections import Counter


# --- Section 1: String Sorts ---


def lsd_sort(a: List[str], w: int) -> None:
    """
    Sorts an array of fixed-length strings using Least-Significant-Digit Radix Sort.

    Time Complexity: O(W * N) where W is width, N is number of strings.
    Space Complexity: O(N + R) where R is alphabet size.
    Stability: Stable.

    Args:
        a (List[str]): List of strings, all of length w.
        w (int): The fixed length of the strings.
    """
    n = len(a)
    r = 256  # Extended ASCII size
    aux = [""] * n

    # Sort by key-indexed counting on d-th char
    for d in range(w - 1, -1, -1):
        count = [0] * (r + 1)

        # Compute frequency counts
        for i in range(n):
            c = ord(a[i][d])
            count[c + 1] += 1

        # Transform counts to indices
        for i in range(r):
            count[i + 1] += count[i]

        # Distribute
        for i in range(n):
            c = ord(a[i][d])
            aux[count[c]] = a[i]
            count[c] += 1

        # Copy back
        for i in range(n):
            a[i] = aux[i]


def msd_sort(a: List[str]) -> None:
    """
    Sorts an array of strings using Most-Significant-Digit Radix Sort.

    Suitable for variable-length strings. Recursive implementation.

    Time Complexity: O(N * W) worst case, much faster for random strings.
    Space Complexity: O(N + R) per recursion level.
    Stability: Stable.

    Args:
        a (List[str]): List of strings to sort.
    """
    n = len(a)
    aux = [""] * n
    _msd_sort(a, 0, n - 1, 0, aux)


def _msd_sort(a: List[str], lo: int, hi: int, d: int, aux: List[str]) -> None:
    # Cutoff to insertion sort for small subarrays (omitted for brevity, pure recursive here)
    if hi <= lo:
        return

    r = 256
    count = [0] * (r + 2)  # +2 for end-of-string handling (-1 index)

    # Compute frequency counts
    for i in range(lo, hi + 1):
        c = _char_at(a[i], d)
        count[c + 2] += 1

    # Transform counts to indices
    for i in range(r + 1):
        count[i + 1] += count[i]

    # Distribute
    for i in range(lo, hi + 1):
        c = _char_at(a[i], d)
        aux[count[c + 1]] = a[i]
        count[c + 1] += 1

    # Copy back
    for i in range(lo, hi + 1):
        a[i] = aux[i - lo]

    # Recursively sort for each character value
    # Note: We do NOT recurse for the -1 (end of string) bin
    for i in range(r):
        _msd_sort(a, lo + count[i], lo + count[i + 1] - 1, d + 1, aux)


def _char_at(s: str, d: int) -> int:
    """Returns char value at d, or -1 if d >= len(s)."""
    if d < len(s):
        return ord(s[d])
    return -1


# --- Section 2: Substring Search ---


class KMP:
    """
    Knuth-Morris-Pratt Substring Search.

    Precomputes a Deterministic Finite Automaton (DFA) from the pattern
    to allow searching without backing up the text pointer.
    """

    def __init__(self, pat: str):
        self._pat = pat
        self._m = len(pat)
        self._r = 256
        self._dfa = [[0] * self._m for _ in range(self._r)]

        # Build DFA
        self._dfa[ord(pat[0])][0] = 1
        x = 0
        for j in range(1, self._m):
            for c in range(self._r):
                self._dfa[c][j] = self._dfa[c][x]  # Copy mismatch cases
            self._dfa[ord(pat[j])][j] = j + 1  # Set match case
            x = self._dfa[ord(pat[j])][x]  # Update restart state

    def search(self, txt: str) -> int:
        """
        Searches for the pattern in the given text.

        Returns:
            int: The index of the first occurrence, or -1 if not found.
        """
        n = len(txt)
        m = self._m
        i, j = 0, 0

        while i < n and j < m:
            j = self._dfa[ord(txt[i])][j]
            i += 1

        if j == m:
            return i - m
        return -1


class BoyerMoore:
    """
    Boyer-Moore Substring Search (Bad Character Rule).

    Skips sections of text by analyzing the character that caused a mismatch.
    """

    def __init__(self, pat: str):
        self._pat = pat
        self._r = 256
        self._right = [-1] * self._r

        # Compute last occurrence of each char in pattern
        for j in range(len(pat)):
            self._right[ord(pat[j])] = j

    def search(self, txt: str) -> int:
        n = len(txt)
        m = len(self._pat)
        skip = 0

        i = 0
        while i <= n - m:
            skip = 0
            for j in range(m - 1, -1, -1):
                if self._pat[j] != txt[i + j]:
                    skip = max(1, j - self._right[ord(txt[i + j])])
                    break
            if skip == 0:
                return i  # Found
            i += skip
        return -1


# --- Section 3: Compression (Huffman) ---


class Huffman:
    """
    Huffman Compression.

    Constructs an optimal prefix-free code for a given string based on character frequency.
    Returns the binary string representation and the decoding tree.
    """

    class _Node:
        def __init__(self, ch: Optional[str], freq: int, left=None, right=None):
            self.ch = ch
            self.freq = freq
            self.left = left
            self.right = right

        def is_leaf(self) -> bool:
            return self.left is None and self.right is None

        def __lt__(self, other):
            return self.freq < other.freq

    @staticmethod
    def compress(s: str) -> Tuple[str, Dict[str, str]]:
        """
        Compresses string s using Huffman coding.

        Returns:
            Tuple[str, Dict]: (Binary String, Code Map)
        """
        if not s:
            return "", {}

        # 1. Frequency count
        freqs = Counter(s)

        # 2. Build trie
        pq = [Huffman._Node(ch, freq) for ch, freq in freqs.items()]
        heapq.heapify(pq)

        while len(pq) > 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            parent = Huffman._Node(None, left.freq + right.freq, left, right)
            heapq.heappush(pq, parent)

        root = pq[0]

        # 3. Build code table
        codes: Dict[str, str] = {}
        Huffman._build_code(root, "", codes)

        # 4. Encode
        encoded = "".join(codes[ch] for ch in s)
        return encoded, codes

    @staticmethod
    def _build_code(x: _Node, s: str, codes: Dict[str, str]) -> None:
        if x.is_leaf():
            codes[x.ch] = s if s else "0"  # Handle single char case
            return
        Huffman._build_code(x.left, s + "0", codes)
        Huffman._build_code(x.right, s + "1", codes)


class LZW:
    """
    Lempel-Ziv-Welch (LZW) Compression.

    A dictionary-based compression algorithm that is particularly effective for
    data with repeated patterns. It builds a dictionary of substrings encountered
    in the data and represents them with shorter codes.

    Reference:
        Algorithms, 4th Edition by Sedgewick and Wayne, Section 5.5.
    """

    @staticmethod
    def compress(s: str) -> List[int]:
        """
        Compresses a string into a list of dictionary indices.

        Time Complexity: O(N) where N is the length of the string.
        Space Complexity: O(K) where K is the number of unique substrings.

        Args:
            s (str): The input string to compress.

        Returns:
            List[int]: A list of integer codes representing the compressed data.
        """
        if not s:
            return []

        # Initialize dictionary with individual characters (Extended ASCII)
        r = 256
        st = {chr(i): i for i in range(r)}
        dict_size = r

        w = ""
        result = []
        for c in s:
            wc = w + c
            if wc in st:
                w = wc
            else:
                result.append(st[w])
                # Add new substring to the dictionary
                st[wc] = dict_size
                dict_size += 1
                w = c

        # Append code for the remaining prefix
        if w:
            result.append(st[w])
        return result

    @staticmethod
    def decompress(compressed: List[int]) -> str:
        """
        Decompresses a list of LZW codes back into the original string.

        Args:
            compressed (List[int]): The list of integer codes to decompress.

        Returns:
            str: The original uncompressed string.

        Raises:
            ValueError: If an invalid or corrupted code is encountered.
        """
        if not compressed:
            return ""

        # Initialize dictionary with individual characters
        r = 256
        st = {i: chr(i) for i in range(r)}
        dict_size = r

        # Clone list to avoid modifying the input
        codes = list(compressed)
        w = st[codes.pop(0)]
        result = [w]

        for k in codes:
            if k in st:
                entry = st[k]
            elif k == dict_size:
                # Handle the special case: w + w[0] (e.g., ABABA)
                entry = w + w[0]
            else:
                raise ValueError(f"Invalid compressed code: {k}")

            result.append(entry)

            # Add new substring to the dictionary
            st[dict_size] = w + entry[0]
            dict_size += 1
            w = entry

        return "".join(result)
