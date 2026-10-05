"""Retrieval of postings lists from the index stored on disk."""

from pathlib import Path

from irsys.storage import POSTINGS_FILE, load_dictionary, read_postings


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

    def close(self) -> None:
        self.postings_file.close()