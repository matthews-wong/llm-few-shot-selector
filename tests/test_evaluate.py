import os
import unittest

from fewshot.evaluate import ROOT, STRATEGIES, count_hits, load_queries
from fewshot.pool import load_pool


class EvaluateTest(unittest.TestCase):
    def test_similarity_beats_arbitrary_picks_on_fixtures(self):
        pool = load_pool(os.path.join(ROOT, "pool.jsonl"))
        queries = load_queries()
        baseline = count_hits(STRATEGIES["first-k"], pool, queries)
        for name in ("bm25", "bm25+mmr"):
            self.assertGreater(count_hits(STRATEGIES[name], pool, queries), baseline, name)


if __name__ == "__main__":
    unittest.main()
