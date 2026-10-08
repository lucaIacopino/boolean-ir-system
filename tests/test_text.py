"""Tests for tokenization and query parsing."""

import pytest

from irsys.query import parse_query
from irsys.tokenizer import tokenize


def test_tokenize_lowercase_and_punctuation():
    assert tokenize("Bahia COCOA review: bags!") == ["bahia", "cocoa", "review", "bags"]


def test_tokenize_removes_accents():
    assert tokenize("Café") == ["cafe"]


def test_parse_single_term():
    assert parse_query("Cocoa") == ("AND", ["cocoa"])


def test_parse_and_query():
    assert parse_query("cocoa AND Brazil") == ("AND", ["cocoa", "brazil"])


def test_parse_or_query():
    assert parse_query("cocoa OR coffee OR sugar") == ("OR", ["cocoa", "coffee", "sugar"])


def test_stop_words_are_removed_from_query():
    assert parse_query("the AND cocoa") == ("AND", ["cocoa"])


@pytest.mark.parametrize(
    "query",
    ["cocoa AND coffee OR sugar", "cocoa AND", "cocoa coffee", "the"],
)
def test_invalid_queries(query):
    with pytest.raises(ValueError):
        parse_query(query)