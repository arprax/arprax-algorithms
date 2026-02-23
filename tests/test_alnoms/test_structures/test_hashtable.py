from alnoms.structures.hashtable import (
    SeparateChainingHashST,
    LinearProbingHashST,
)


# --- Separate Chaining Tests (Already Passing) ---


def test_sc_basic_ops():
    st = SeparateChainingHashST(m=5)
    assert st.is_empty()
    st.put("A", 1)
    st.put("B", 2)
    assert st.size() == 2
    assert st.get("A") == 1

    # Update
    st.put("A", 10)
    assert st.get("A") == 10


def test_sc_collision_handling():
    st = SeparateChainingHashST(m=1)  # Force collisions
    st.put("A", 1)
    st.put("B", 2)
    st.delete("A")
    assert st.get("A") is None
    assert st.get("B") == 2


def test_sc_put_none_deletes():
    st = SeparateChainingHashST()
    st.put("A", 1)
    st.put("A", None)
    assert not st.contains("A")


def test_sc_keys():
    st = SeparateChainingHashST()
    st.put("A", 1)
    assert "A" in st.keys()


# --- Linear Probing Tests (The Fixes) ---


def test_lp_update_existing():
    """
    Hits Lines 156-157.
    We MUST put the same key twice to trigger the update block.
    """
    st = LinearProbingHashST(capacity=4)
    st.put("A", 1)

    # This specific line triggers: if keys[i] == key: vals[i] = val
    st.put("A", 2)

    assert st.get("A") == 2
    assert st.size() == 1  # Size should not increase


def test_lp_shrink_trigger():
    """
    Hits Line 215.
    We need to delete items until n > 0 but n <= m/8.
    """
    # Start with capacity 16.
    # Resize threshold is 16 // 8 = 2.
    st = LinearProbingHashST(capacity=16)

    # Add 3 items (n=3)
    st.put("A", 1)
    st.put("B", 2)
    st.put("C", 3)

    # Delete "A" -> n=2. (2 <= 2) is True.
    # This should trigger resize(8).
    st.delete("A")

    # We can't easily check private _m, but we verify state is valid
    assert st.size() == 2
    assert st.get("B") == 2
    assert st.get("C") == 3
    assert st.get("A") is None


def test_lp_cluster_management():
    """
    Ensures delete re-hashing works (Lines 200+).
    """
    st = LinearProbingHashST(capacity=10)
    # Create cluster: 1, 11, 21 (all likely hash to 1)
    st.put(1, "one")
    st.put(11, "eleven")
    st.put(21, "twenty-one")

    # Delete middle of cluster
    st.delete(11)

    # Verify tail is preserved
    assert st.get(21) == "twenty-one"
    assert st.get(1) == "one"
    assert st.get(11) is None


def test_lp_resize_grow():
    """Ensures growing works (Line 149)."""
    st = LinearProbingHashST(capacity=4)
    st.put("A", 1)
    st.put("B", 2)  # n=2, m=4. 2 >= 2. Resize -> 8.
    assert st.get("A") == 1
    # If we add more, it should accommodate
    st.put("C", 3)
    st.put("D", 4)
    st.put("E", 5)
    assert st.size() == 5


def test_lp_edge_cases():
    st = LinearProbingHashST()
    st.delete("Ghost")  # Delete missing
    st.put("A", None)  # Put None
    assert st.is_empty()
