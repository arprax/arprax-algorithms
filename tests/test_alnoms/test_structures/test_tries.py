import pytest
from alnoms.structures.tries import TrieST, TST


# --- SECTION 1: TrieST (R-way Trie) Tests ---


def test_trie_basic_ops():
    """Test put, get, contains, size, is_empty."""
    trie = TrieST()
    assert trie.is_empty()
    assert trie.size() == 0

    trie.put("she", 0)
    trie.put("sells", 1)
    trie.put("sea", 2)
    trie.put("shells", 3)

    assert trie.size() == 4
    assert trie.contains("she")
    assert trie.get("she") == 0
    assert trie.get("shells") == 3
    assert trie.get("missing") is None

    # Update value
    trie.put("she", 99)
    assert trie.get("she") == 99


def test_trie_prefix_matching():
    """Test keys() and keys_with_prefix()."""
    trie = TrieST()
    keys = ["she", "sells", "sea", "shells", "by", "the", "shore"]
    for i, k in enumerate(keys):
        trie.put(k, i)

    # keys() should return all
    all_keys = trie.keys()
    assert len(all_keys) == len(keys)
    assert "she" in all_keys

    # keys_with_prefix("sh") -> she, shells, shore
    sh_keys = trie.keys_with_prefix("sh")
    assert len(sh_keys) == 3
    assert "she" in sh_keys
    assert "shells" in sh_keys
    assert "shore" in sh_keys
    assert "sea" not in sh_keys

    # keys_with_prefix("se") -> sells, sea
    se_keys = trie.keys_with_prefix("se")
    assert len(se_keys) == 2

    # keys_with_prefix("z") -> empty
    assert trie.keys_with_prefix("z") == []


def test_trie_deletion():
    """Test deletion logic (removing nodes vs keeping internal nodes)."""
    trie = TrieST()
    trie.put("she", 1)
    trie.put("shells", 2)  # 'she' is a prefix of 'shells'

    # Delete 'shells'
    # Should remove 'l-l-s' nodes but KEEP 'she' because it has a value
    trie.delete("shells")
    assert trie.contains("she")
    assert not trie.contains("shells")
    assert trie.size() == 1

    # Delete 'she'
    # Should remove the value at 'she', and since it has no children, clean up up to root
    trie.delete("she")
    assert trie.is_empty()

    # Delete non-existent
    trie.put("a", 1)
    trie.delete("z")
    assert trie.size() == 1


def test_trie_validation():
    for TrieClass in [TrieST, TST]:  # It tests both!
        trie = TrieClass(r=128)
        with pytest.raises(ValueError):
            trie.put("invalid_char_ñ", 1)  # ñ is code 241, > 128

    # Try inserting a unicode character > 255
    with pytest.raises(ValueError):
        trie.put("café", 1)  # 'é' is usually > 255 depending on encoding/python

    # Custom small alphabet
    small_trie = TrieST(r=256)  # Digits only
    small_trie.put("123", 1)
    limit_trie = TrieST(r=50)
    with pytest.raises(ValueError):
        limit_trie.put("a", 1)  # 'a' is 97 > 10


# --- SECTION 2: TST (Ternary Search Trie) Tests ---


def test_tst_basic_ops():
    """Test put, get, contains, size."""
    tst = TST()
    assert tst.size() == 0

    tst.put("she", 1)
    tst.put("sells", 2)
    tst.put("sea", 3)

    assert tst.size() == 3
    assert tst.get("she") == 1
    assert tst.get("sea") == 3
    assert tst.get("shell") is None

    # Update
    tst.put("she", 99)
    assert tst.get("she") == 99


def test_tst_structure_branching():
    """
    Test that the TST splits correctly (Left, Mid, Right).
    'c' (root)
       /  |  \
     'a' 'h' 'u'
    """
    tst = TST()
    tst.put("cat", 1)  # c -> a -> t
    tst.put("cut", 2)  # c -> u (right of a) -> t
    tst.put("call", 3)

    assert tst.get("cat") == 1
    assert tst.get("cut") == 2
    assert tst.get("call") == 3


def test_tst_prefix_matching():
    """Test prefix collection logic."""
    tst = TST()
    tst.put("apple", 1)
    tst.put("app", 2)
    tst.put("apricot", 3)
    tst.put("banana", 4)

    # Prefix "ap" -> apple, app, apricot
    ap_keys = tst.keys_with_prefix("ap")
    assert len(ap_keys) == 3
    assert "banana" not in ap_keys

    # Prefix "" -> all keys
    assert len(tst.keys_with_prefix("")) == 4

    # Prefix "z" -> None
    assert tst.keys_with_prefix("z") == []


def test_tst_validation():
    """TST does not support empty keys well by definition."""
    tst = TST()
    with pytest.raises(ValueError):
        tst.put("", 1)
    with pytest.raises(ValueError):
        tst.get("")
