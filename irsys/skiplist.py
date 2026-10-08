"""Postings lists with skip pointers."""

import math


class SkipList:
    """A postings list with evenly spaced skip pointers.

    skips[i] is the position reached by the skip pointer stored at
    position i, or None if there is no skip pointer at position i.
    """

    def __init__(self, postings: list[int], span: int | None = None) -> None:
        self.postings = postings
        if span is None:
            span = int(math.sqrt(len(postings)))  # heuristic: sqrt(P) pointers
        self.skips: list[int | None] = [None] * len(postings)
        if span > 1:
            for i in range(0, len(postings) - span, span):
                self.skips[i] = i + span


def _advance(lst: SkipList, i: int, target: int) -> int:
    """Move forward from position i, using skip pointers when possible.

    Skips are followed as long as they do not go past 'target';
    if no skip can be used, move forward by one position.
    """
    skipped = False
    while lst.skips[i] is not None and lst.postings[lst.skips[i]] <= target:
        i = lst.skips[i]
        skipped = True
    return i if skipped else i + 1


def intersect_with_skips(a: SkipList, b: SkipList) -> list[int]:
    """AND between two postings lists, using skip pointers."""
    p1, p2 = a.postings, b.postings
    answer = []
    i = j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i = _advance(a, i, p2[j])
        else:
            j = _advance(b, j, p1[i])
    return answer