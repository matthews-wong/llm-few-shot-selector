import unittest

from fewshot.bm25 import bm25_scores


class Bm25Test(unittest.TestCase):
    def test_matching_document_scores_highest(self):
        scores = bm25_scores("refund order", ["reset my password", "refund my order", "cancel plan"])
        self.assertEqual(scores.index(max(scores)), 1)

    def test_no_overlap_scores_zero(self):
        self.assertEqual(bm25_scores("zebra", ["alpha beta", "gamma"]), [0.0, 0.0])

    def test_empty_inputs(self):
        self.assertEqual(bm25_scores("x", []), [])
        self.assertEqual(bm25_scores("x", ["", ""]), [0.0, 0.0])

    def test_rarer_term_outweighs_common_term(self):
        docs = ["invoice invoice", "invoice vat", "invoice tax", "vat"]
        scores = bm25_scores("invoice vat", docs)
        self.assertGreater(scores[1], scores[0])


if __name__ == "__main__":
    unittest.main()
