"""Compare selection strategies on the fixture pool.

Metric: majority label of the selected examples equals the gold label of the
query. It is a proxy for "would the examples steer a model the right way", and
needs no model call. Numbers are fixture results, not a benchmark.
"""
import json
import os
import sys
from collections import Counter

from .pool import load_pool
from .selector import select

ROOT = os.path.join(os.path.dirname(__file__), "..", "fixtures")
K = 3
STRATEGIES = {
    "first-k": lambda query, pool: pool[:K],
    "bm25": lambda query, pool: select(query, pool, K, diversity=1.0),
    "bm25+mmr": lambda query, pool: select(query, pool, K),
}


def majority(examples):
    if not examples:
        return None
    return Counter(e.output for e in examples).most_common(1)[0][0]


def load_queries():
    with open(os.path.join(ROOT, "queries.jsonl"), encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def count_hits(strategy, pool, queries):
    return sum(majority(strategy(q["query"], pool)) == q["label"] for q in queries)


def main():
    pool = load_pool(os.path.join(ROOT, "pool.jsonl"))
    queries = load_queries()
    print(f"pool={len(pool)} queries={len(queries)} k={K} (fixtures)")
    print(f"{'strategy':<10} majority-correct")
    for name, strategy in STRATEGIES.items():
        print(f"{name:<10} {count_hits(strategy, pool, queries)}/{len(queries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
