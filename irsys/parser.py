"""Parser for the Reuters-21578 collection (SGML files)."""

import html
import re
from pathlib import Path
from typing import Iterator

# One article: <REUTERS ... NEWID="123"> ... </REUTERS>
DOC_PATTERN = re.compile(r'<REUTERS[^>]*NEWID="(\d+)"[^>]*>(.*?)</REUTERS>', re.DOTALL)
TEXT_PATTERN = re.compile(r"<TEXT[^>]*>(.*?)</TEXT>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")


def parse_file(path: Path) -> Iterator[tuple[int, str]]:
    """Yield (doc_id, text) pairs for every article in one .sgm file."""
    # latin-1 because a few files contain bytes that are not valid UTF-8
    content = path.read_text(encoding="latin-1")
    for match in DOC_PATTERN.finditer(content):
        doc_id = int(match.group(1))
        text_match = TEXT_PATTERN.search(match.group(2))
        text = text_match.group(1) if text_match else ""
        text = TAG_PATTERN.sub(" ", text)
        yield doc_id, html.unescape(text)


def parse_collection(folder: Path) -> Iterator[tuple[int, str]]:
    """Yield (doc_id, text) pairs for the whole collection, file by file."""
    for path in sorted(folder.glob("reut2-*.sgm")):
        yield from parse_file(path)