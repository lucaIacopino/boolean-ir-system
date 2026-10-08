"""Retrieval of postings lists from the index stored on disk."""

from pathlib import Path

from irsys.storage import POSTINGS_FILE, load_dictionary, read_postings
from irsys.boolean import intersect, union
from irsys.skiplist import SkipList, intersect_with_skips


class Searcher:
    """Keeps the dictionary in memory and reads postings lists from disk."""

    def __init__(self, folder: Path) -> None:
        self.dictionary = load_dictionary(folder)
        self.postings_file = open(folder / POSTINGS_FILE, "rb")

    def postings(self, term: str) -> list[int]:
        """Return the postings list of 'term' (empty list if not in the index)."""
        if term not in self.dictionary:
            return []
        df, offset = self.dictionary[term]
        return read_postings(self.postings_file, df, offset)

    def document_frequency(self, term: str) -> int:
        """Number of documents containing 'term' (0 if not in the index)."""
        return self.dictionary[term][0] if term in self.dictionary else 0
    
    def search_and(
        self, terms: list[str], optimized: bool = True, use_skips: bool = True
    ) -> list[int]:
        """Conjunctive query: intersect the postings lists of all terms.

        If 'optimized' is True, terms are processed in order of
        increasing document frequency.
        If 'use_skips' is True, the intersection uses skip pointers.
        """
        if optimized:
            terms = sorted(terms, key=self.document_frequency)
        result = self.postings(terms[0])
        for term in terms[1:]:
            if not result:  # empty intersection: no need to go on
                break
            postings = self.postings(term)
            if use_skips:
                result = intersect_with_skips(SkipList(result), SkipList(postings))
            else:
                result = intersect(result, postings)
        return result

    def search_or(self, terms: list[str]) -> list[int]:
        """Disjunctive query: unite the postings lists of all terms."""
        result: list[int] = []
        for term in terms:
            result = union(result, self.postings(term))
        return result
    
    def close(self) -> None:
        self.postings_file.close()