"""Operations on postings lists (sorted lists of docIDs)."""


def intersect(p1: list[int], p2: list[int]) -> list[int]:
    """AND: docIDs present in both lists. Linear merge, O(len(p1) + len(p2))."""
    answer = []
    i = j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    return answer


def union(p1: list[int], p2: list[int]) -> list[int]:
    """OR: docIDs present in at least one list. Linear merge, O(len(p1) + len(p2))."""
    answer = []
    i = j = 0
    while i < len(p1) and j < len(p2):
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            answer.append(p1[i])
            i += 1
        else:
            answer.append(p2[j])
            j += 1
    answer.extend(p1[i:])  # what is left in one of the two lists
    answer.extend(p2[j:])
    return answer