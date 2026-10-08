# Boolean IR System

A simple Information Retrieval system developed for the *Information Retrieval* university course.
It builds an inverted index over the [Reuters-21578](https://archive.ics.uci.edu/dataset/137/reuters+21578+text+categorization+collection) collection and answers Boolean queries from the command line.

## Features

- **Inverted index**: dictionary (term → document frequency, offset) and postings lists, stored on disk
- **Single-term search**
- **Conjunctive and disjunctive queries** with more terms (`AND` / `OR`)
- **Optimized conjunctive queries**: terms processed by increasing document frequency
- **Skip pointers** (√P evenly spaced) for faster intersections, with a benchmark
- **Stop list**: very common words are not indexed and are ignored in queries
- **Spelling suggestions** based on the edit distance

Everything related to Information Retrieval is implemented from scratch: no external libraries are used by the system.

## Project structure

```
irsys/
├── parser.py      # reads the Reuters-21578 SGML files -> (docID, text)
├── tokenizer.py   # tokenization and normalization
├── stoplist.py    # stop words
├── indexer.py     # builds the inverted index in memory
├── storage.py     # saves / loads the index on disk
├── boolean.py     # intersection and union of postings lists
├── skiplist.py    # postings lists with skip pointers
├── query.py       # parsing of the user query
├── searcher.py    # runs the queries on the index
└── spelling.py    # edit distance and spelling suggestions
tests/             # unit tests (pytest)
main.py            # command line interface
benchmark.py       # skip pointers experiments
report/            # report and charts
```

## Setup

Requires Python 3.10 or newer.

```bash
git clone git@github.com:lucaIacopino/boolean-ir-system.git
cd boolean-ir-system
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # only needed for tests and benchmark
```

Download the dataset (it is not included in the repository):

```bash
mkdir -p data/reuters21578
curl -L https://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz -o data/reuters21578.tar.gz
tar -xzf data/reuters21578.tar.gz -C data/reuters21578
rm data/reuters21578.tar.gz
```

## Usage

Build the index (run once, in advance):

```bash
python main.py index
```

Search:

```bash
python main.py search
```

Query syntax:

| Query | Meaning |
|---|---|
| `cocoa` | documents containing *cocoa* |
| `cocoa AND brazil AND export` | documents containing all the terms |
| `cocoa OR coffee OR sugar` | documents containing at least one term |

Operators must be written in uppercase. `AND` and `OR` cannot be mixed in the same query.

Example:

```
> cocoa AND brazl
0 documents found
'brazl' not found. Did you mean: brazil, braz?
```

## Tests

```bash
python -m pytest
```

## Benchmark

Compares the intersection time with and without skip pointers (the index must be built first):

```bash
python benchmark.py
```

The chart is saved in `report/skip_benchmark.png`.