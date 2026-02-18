from arprax.algos.algorithms.strings import lsd_sort, msd_sort, KMP, BoyerMoore, Huffman


# --- Sort Tests ---


def test_lsd_sort():
    a = ["4PGC938", "2IYE230", "3CIO720", "1ICK750", "1OHV845", "4JZY524", "1ICK750"]
    # LSD requires fixed width (W=7)
    lsd_sort(a, 7)
    assert a == sorted(a)

    # Stable check: 1ICK750 should remain in relative order if duplicated
    assert a[0] == "1ICK750"
    assert a[1] == "1ICK750"


def test_msd_sort():
    a = ["she", "sells", "seashells", "by", "the", "sea", "shore"]
    msd_sort(a)
    assert a == sorted(a)


# --- Search Tests ---


def test_kmp_search():
    pat = "ABABAC"
    txt = "BCBAABACAABABACAA"
    kmp = KMP(pat)

    idx = kmp.search(txt)
    assert idx == 9  # Matches at index 9

    assert kmp.search("NO MATCH") == -1


def test_boyer_moore_search():
    pat = "NEEDLE"
    txt = "HAYSTACKNEEDLEHAYSTACK"
    bm = BoyerMoore(pat)

    assert bm.search(txt) == 8
    assert bm.search("NOWHERE") == -1


# --- Compression Tests ---


def test_huffman_compression():
    text = "ABRACADABRA!"
    encoded_str, codes = Huffman.compress(text)

    # Check that A (most frequent) has shortest code
    assert len(codes["A"]) <= len(codes["R"])
    assert len(codes["A"]) <= len(codes["!"])

    # Verify prefix property (no code is prefix of another)
    code_list = list(codes.values())
    for i in range(len(code_list)):
        for j in range(len(code_list)):
            if i != j:
                assert not code_list[j].startswith(code_list[i])


def test_huffman_edge_cases():
    # Empty
    assert Huffman.compress("") == ("", {})

    # Single Char
    enc, codes = Huffman.compress("AAAA")
    assert codes["A"] == "0"
    assert enc == "0000"
