import unittest

from fewshot.pool import Example, example_tokens
from fewshot.selector import select

POOL = [
    Example("a", "refund my order please", "billing"),
    Example("b", "refund my order now please", "billing"),
    Example("c", "app crashes on login", "bug"),
    Example("d", "how do I export data", "howto"),
]


class SelectTest(unittest.TestCase):
    def test_most_relevant_first(self):
        self.assertEqual(select("refund order", POOL, k=1)[0].id, "a")

    def test_diversity_avoids_near_duplicate(self):
        ids = [e.id for e in select("refund order", POOL, k=2, diversity=0.3)]
        self.assertNotIn("b", ids)

    def test_pure_relevance_keeps_near_duplicate(self):
        ids = [e.id for e in select("refund order", POOL, k=2, diversity=1.0)]
        self.assertEqual(ids, ["a", "b"])

    def test_budget_skips_whole_examples(self):
        budget = example_tokens(POOL[0])
        picked = select("refund order", POOL, k=3, budget=budget)
        self.assertLessEqual(sum(example_tokens(e) for e in picked), budget)
        self.assertEqual(picked[0].id, "a")

    def test_zero_budget_returns_nothing(self):
        self.assertEqual(select("refund", POOL, k=3, budget=0), [])

    def test_empty_pool_and_k_zero(self):
        self.assertEqual(select("x", [], k=3), [])
        self.assertEqual(select("refund", POOL, k=0), [])

    def test_invalid_arguments_name_the_value(self):
        with self.assertRaisesRegex(ValueError, "-1"):
            select("x", POOL, k=-1)
        with self.assertRaisesRegex(ValueError, "1.5"):
            select("x", POOL, k=1, diversity=1.5)


if __name__ == "__main__":
    unittest.main()
