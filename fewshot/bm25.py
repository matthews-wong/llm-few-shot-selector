"""BM25 over example inputs; no index to persist, pools are small."""
import math
from collections import Counter

from .pool import tokenize

K1 = 1.5
B = 0.75


def bm25_scores(query, documents):
    """Return one BM25 score per document, in document order."""
    docs = [Counter(tokenize(text)) for text in documents]
    lengths = [sum(doc.values()) for doc in docs]
    if not docs or not any(lengths):
        return [0.0] * len(docs)
    avg = sum(lengths) / len(docs)
    scores = []
    for doc, length in zip(docs, lengths):
        score = 0.0
        for term in set(tokenize(query)):
            freq = doc.get(term, 0)
            if not freq:
                continue
            df = sum(1 for other in docs if term in other)
            idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
            score += idf * freq * (K1 + 1) / (freq + K1 * (1 - B + B * length / avg))
        scores.append(score)
    return scores
