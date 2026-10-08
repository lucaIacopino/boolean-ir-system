"""Tests for index construction, storage on disk, search and spelling."""

from irsys.indexer import build_index
from irsys.searcher import Searcher
from irsys.spelling import edit_distance, suggest
from irsys.storage import load_dictionary, save_index

DOCS = [
    (1, "Cocoa prices rise in Brazil"),
    (2, "Coffee and cocoa exports"),
    (3, "Brazil coffee harvest, coffee prices"),
]


def test_build_index():
    index = build_index(DOCS)
    assert index["cocoa"] == [1, 2]
    assert index["coffee"] == [2, 3]  # doc 3 is added only once
    assert "and" not in index         # stop word


def test_dictionary_document_frequency(tmp_path):
    save_index(build_index(DOCS), tmp_path)
    assert load_dictionary(tmp_path)["coffee"][0] == 2


def test_save_and_search(tmp_path):
    save_index(build_index(DOCS), tmp_path)
    searcher = Searcher(tmp_path)
    try:
        assert searcher.postings("brazil") == [1, 3]
        assert searcher.postings("missing") == []
        assert searcher.search_and(["coffee", "brazil"]) == [3]
        assert searcher.search_and(["coffee", "brazil"], use_skips=False) == [3]
        assert searcher.search_or(["cocoa", "harvest"]) == [1, 2, 3]
    finally:
        searcher.close()


def test_edit_distance():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("cocoa", "cocoa") == 0


def test_suggest():
    dictionary = {"coffee": (2, 0), "cocoa": (2, 8), "brazil": (2, 16)}
    assert suggest("coffe", dictionary) == ["coffee"]
    assert suggest("zzz", dictionary) == []