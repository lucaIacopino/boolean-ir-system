"""Tokenization and normalization of text."""

import re
import unicodedata

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def normalize(text: str) -> str:
    """Lowercase the text and remove accents (e.g. 'Café' -> 'cafe')."""
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def tokenize(text: str) -> list[str]:
    """Split the text into normalized terms (letters and digits only)."""
    return TOKEN_PATTERN.findall(normalize(text))