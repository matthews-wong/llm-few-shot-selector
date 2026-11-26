"""Choose examples: BM25 relevance, MMR diversity, whole-example budget packing."""
from .bm25 import bm25_scores
from .pool import example_tokens, tokenize

DEFAULT_LAMBDA = 0.7  # weight on relevance; the rest penalises similarity to picks


def _jaccard(a, b):
    left, right = set(tokenize(a)), set(tokenize(b))
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def select(query, pool, k, budget=None, diversity=DEFAULT_LAMBDA):
    """Return up to k examples, best first, whose total tokens fit the budget.

    An example that does not fit is skipped rather than truncated, so the
    prompt never contains half an example.
    """
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k}")
    if not 0.0 <= diversity <= 1.0:
        raise ValueError(f"diversity must be within [0, 1], got {diversity}")
    scores = bm25_scores(query, [e.input for e in pool])
    top = max(scores, default=0.0) or 1.0
    relevance = [s / top for s in scores]
    remaining = list(range(len(pool)))
    picked = []
    used = 0
    while remaining and len(picked) < k:
        def mmr(i):
            overlap = max((_jaccard(pool[i].input, pool[j].input) for j in picked), default=0.0)
            return diversity * relevance[i] - (1 - diversity) * overlap

        best = max(remaining, key=lambda i: (mmr(i), -i))
        remaining.remove(best)
        cost = example_tokens(pool[best])
        if budget is not None and used + cost > budget:
            continue
        used += cost
        picked.append(best)
    return [pool[i] for i in picked]
