"""Spelling correction based on the edit distance (Levenshtein)."""

MAX_DISTANCE = 2
MAX_SUGGESTIONS = 5


def edit_distance(s1: str, s2: str) -> int:
    """Minimum number of insertions, deletions and substitutions needed
    to turn s1 into s2 (dynamic programming, O(len(s1) * len(s2)))."""
    # table[i][j] = distance between the first i chars of s1 and the first j chars of s2
    table = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    for i in range(len(s1) + 1):
        table[i][0] = i
    for j in range(len(s2) + 1):
        table[0][j] = j
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            table[i][j] = min(
                table[i - 1][j] + 1,         # deletion
                table[i][j - 1] + 1,         # insertion
                table[i - 1][j - 1] + cost,  # substitution (or match)
            )
    return table[len(s1)][len(s2)]


def suggest(term: str, dictionary: dict[str, tuple[int, int]]) -> list[str]:
    """Return the dictionary terms closest to 'term' (at most MAX_DISTANCE away).

    Only terms starting with the same letter are compared (heuristic:
    errors rarely occur at the beginning of a word).
    Suggestions are sorted by document frequency (most common first).
    """
    candidates = [t for t in dictionary if t[0] == term[0]]
    distances = {t: edit_distance(term, t) for t in candidates}
    best = min(distances.values(), default=MAX_DISTANCE + 1)
    if best > MAX_DISTANCE:
        return []
    closest = [t for t, d in distances.items() if d == best]
    closest.sort(key=lambda t: dictionary[t][0], reverse=True)
    return closest[:MAX_SUGGESTIONS]