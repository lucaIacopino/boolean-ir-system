"""Command line interface.

Usage:
    python main.py index    # build the index (run once, in advance)
    python main.py search   # interactive search
"""

import argparse
import time
from pathlib import Path

from irsys.indexer import build_index
from irsys.parser import parse_collection
from irsys.searcher import Searcher
from irsys.storage import save_index
from irsys.query import parse_query
from irsys.spelling import suggest

DATA_FOLDER = Path("data/reuters21578")
INDEX_FOLDER = Path("index")


def run_indexing() -> None:
    start = time.perf_counter()
    index = build_index(parse_collection(DATA_FOLDER))
    save_index(index, INDEX_FOLDER)
    elapsed = time.perf_counter() - start
    print(f"Indexed {len(index)} terms in {elapsed:.1f} s")


def run_search() -> None:
    searcher = Searcher(INDEX_FOLDER)
    print("Type a query, e.g. 'cocoa AND brazil' or 'cocoa OR coffee' (empty line to quit).")
    try:
        while query := input("> ").strip():
            try:
                operator, terms = parse_query(query)
            except ValueError as error:
                print(f"Invalid query: {error}")
                continue
            if operator == "AND":
                results = searcher.search_and(terms)
            else:
                results = searcher.search_or(terms)
            print(f"{len(results)} documents found")
            if results:
                print(results)
            for term in terms:
                if term not in searcher.dictionary:
                    suggestions = suggest(term, searcher.dictionary)
                    if suggestions:
                        print(f"'{term}' not found. Did you mean: {', '.join(suggestions)}?")
                    else:
                        print(f"'{term}' not found.")
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        searcher.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Boolean IR system")
    parser.add_argument("command", choices=["index", "search"])
    args = parser.parse_args()
    if args.command == "index":
        run_indexing()
    else:
        run_search()


if __name__ == "__main__":
    main()