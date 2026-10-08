"""Tests for operations on postings lists (with and without skip pointers)."""

from irsys.boolean import intersect, union
from irsys.skiplist import SkipList, intersect_with_skips

BRUTUS = [2, 4, 8, 16, 19, 23, 28, 43]
CAESAR = [1, 2, 3, 5, 8, 41, 51, 60, 71]


def test_intersect():
    assert intersect(BRUTUS, CAESAR) == [2, 8]


def test_intersect_with_empty_list():
    assert intersect(BRUTUS, []) == []


def test_union():
    assert union([1, 3, 5], [2, 3, 6]) == [1, 2, 3, 5, 6]


def test_union_with_empty_list():
    assert union(BRUTUS, []) == BRUTUS


def test_skip_pointers_positions():
    # 8 elements -> span int(sqrt(8)) = 2
    assert SkipList(BRUTUS).skips == [2, None, 4, None, 6, None, None, None]


def test_intersect_with_skips_gives_same_result():
    long_list = list(range(0, 1000, 3))
    short_list = [3, 300, 301, 999]
    expected = intersect(long_list, short_list)
    for span in [None, 2, 5, 50]:
        result = intersect_with_skips(SkipList(long_list, span), SkipList(short_list, span))
        assert result == expected