"""Save the inverted index on disk and read it back.

Two files are used:
- dictionary.txt: one line per term -> "term df offset"
- postings.bin:   all postings lists one after the other,
                  each docID stored as a 4-byte unsigned integer
"""

import struct
from pathlib import Path
from typing import BinaryIO

DICTIONARY_FILE = "dictionary.txt"
POSTINGS_FILE = "postings.bin"
INT_SIZE = 4  # bytes used for each docID


def save_index(index: dict[str, list[int]], folder: Path) -> None:
    """Write the dictionary and the postings lists into 'folder'."""
    folder.mkdir(parents=True, exist_ok=True)
    offset = 0
    with (
        open(folder / DICTIONARY_FILE, "w", encoding="utf-8") as dict_file,
        open(folder / POSTINGS_FILE, "wb") as postings_file,
    ):
        for term in sorted(index):
            postings = index[term]
            postings_file.write(struct.pack(f"<{len(postings)}I", *postings))
            dict_file.write(f"{term} {len(postings)} {offset}\n")
            offset += len(postings) * INT_SIZE


def load_dictionary(folder: Path) -> dict[str, tuple[int, int]]:
    """Load the dictionary: term -> (document frequency, offset)."""
    dictionary = {}
    with open(folder / DICTIONARY_FILE, encoding="utf-8") as dict_file:
        for line in dict_file:
            term, df, offset = line.split()
            dictionary[term] = (int(df), int(offset))
    return dictionary


def read_postings(postings_file: BinaryIO, df: int, offset: int) -> list[int]:
    """Read one postings list from the (already open) postings file."""
    postings_file.seek(offset)
    data = postings_file.read(df * INT_SIZE)
    return list(struct.unpack(f"<{df}I", data))