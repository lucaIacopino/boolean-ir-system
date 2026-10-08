"""Benchmark: AND queries with and without skip pointers.

Run 'python main.py index' first, then: python benchmark.py
The chart is saved in report/skip_benchmark.png
"""

import timeit
from pathlib import Path

import matplotlib.pyplot as plt

from irsys.boolean import intersect
from irsys.searcher import Searcher
from irsys.skiplist import SkipList, intersect_with_skips

INDEX_FOLDER = Path("index")
CHART_FILE = Path("report/skip_benchmark.png")
REPEAT = 200  # each measure is repeated REPEAT times and averaged

# frequent + frequent, medium + medium, rare + rare, frequent + rare
PAIRS = [
    ("said", "mln"),
    ("oil", "price"),
    ("cocoa", "coffee"),
    ("said", "cocoa"),
    ("mln", "brazil"),
]
FIXED_SPANS = [2, 4, 8, 16, 32, 64]
LABELS = ["no skips", "sqrt(P)"] + [f"span {s}" for s in FIXED_SPANS]


def average_ms(function) -> float:
    """Average execution time of 'function', in milliseconds."""
    return timeit.timeit(function, number=REPEAT) / REPEAT * 1000


def main() -> None:
    searcher = Searcher(INDEX_FOLDER)
    results: dict[str, list[float]] = {}

    for a, b in PAIRS:
        p1, p2 = searcher.postings(a), searcher.postings(b)
        times = [average_ms(lambda: intersect(p1, p2))]
        for span in [None] + FIXED_SPANS:  # None means sqrt(P)
            s1, s2 = SkipList(p1, span), SkipList(p2, span)
            times.append(average_ms(lambda: intersect_with_skips(s1, s2)))

        query = f"{a} AND {b}"
        results[query] = times
        print(f"\n{query}  (df: {len(p1)} / {len(p2)})")
        for label, t in zip(LABELS, times):
            print(f"  {label:10} {t:.4f} ms")

    searcher.close()

    plt.figure(figsize=(9, 5))
    for query, times in results.items():
        plt.plot(LABELS, times, marker="o", label=query)
    plt.yscale("log")
    plt.ylabel("average time (ms, log scale)")
    plt.title("AND queries: intersection time with and without skip pointers")
    plt.xticks(rotation=30)
    plt.legend()
    plt.tight_layout()
    CHART_FILE.parent.mkdir(exist_ok=True)
    plt.savefig(CHART_FILE)
    print(f"\nChart saved in {CHART_FILE}")


if __name__ == "__main__":
    main()