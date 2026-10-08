"""Construction of the inverted index (dictionary + postings lists)."""

from typing import Iterable

from irsys.tokenizer import tokenize
from irsys.stoplist import STOP_WORDS


def build_index(docs: Iterable[tuple[int, str]]) -> dict[str, list[int]]:
    """Build the inverted index: term -> sorted list of docIDs (postings list)."""
    index: dict[str, list[int]] = {}
    for doc_id, text in docs:
        for term in set(tokenize(text)) - STOP_WORDS:  # stop words are dropped            
            index.setdefault(term, []).append(doc_id)
    for postings in index.values():
        postings.sort()
    return index