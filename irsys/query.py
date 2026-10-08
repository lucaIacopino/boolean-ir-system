"""Parsing of the user query.

Supported queries:
    term
    term1 AND term2 AND ... AND termN
    term1 OR term2 OR ... OR termN
Operators must be written in uppercase, so that "and" / "or" can still be
searched as normal terms. AND and OR cannot be mixed in the same query.
"""

from irsys.tokenizer import tokenize

OPERATORS = {"AND", "OR"}


def parse_query(query: str) -> tuple[str, list[str]]:
    """Return (operator, terms). For a single-term query the operator is 'AND'."""
    words = query.split()
    raw_terms = words[0::2]        # positions 0, 2, 4, ... must be terms
    operators = set(words[1::2])   # positions 1, 3, 5, ... must be operators

    if len(words) % 2 == 0 or not operators <= OPERATORS:
        raise ValueError("terms and operators must alternate (e.g. a AND b AND c)")
    if len(operators) > 1:
        raise ValueError("AND and OR cannot be mixed in the same query")
    if any(word in OPERATORS for word in raw_terms):
        raise ValueError("an operator is missing a term")

    terms = []
    for raw in raw_terms:
        tokens = tokenize(raw)  # same normalization used for the documents
        if len(tokens) != 1:
            raise ValueError(f"'{raw}' is not a valid term")
        terms.append(tokens[0])

    operator = operators.pop() if operators else "AND"
    return operator, terms