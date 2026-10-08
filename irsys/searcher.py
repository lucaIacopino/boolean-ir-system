"""Retrieval of postings lists from the index stored on disk."""

from pathlib import Path

from irsys.storage import POSTINGS_FILE, load_dictionary, read_postings
from irsys.boolean import intersect, union


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

    def search_and(self, terms: list[str]) -> list[int]:
        """Conjunctive query: intersect the postings lists of all terms."""
        result = self.postings(terms[0])
        for term in terms[1:]:
            if not result:  # empty intersection: no need to go on
                break
            result = intersect(result, self.postings(term))
        return result

    def search_or(self, terms: list[str]) -> list[int]:
        """Disjunctive query: unite the postings lists of all terms."""
        result: list[int] = []
        for term in terms:
            result = union(result, self.postings(term))
        return result
    
    def close(self) -> None:
        self.postings_file.close()