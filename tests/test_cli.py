import contextlib
import io
import os
import tempfile
import unittest

from fewshot.__main__ import main

POOL = os.path.join(os.path.dirname(__file__), "..", "fixtures", "pool.jsonl")


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_select_prints_block(self):
        code, out, _ = run(["select", "--pool", POOL, "--query", "charged twice", "--k", "2"])
        self.assertEqual(code, 0)
        self.assertIn('"output": "billing"', out)

    def test_missing_pool_is_reported(self):
        code, _, err = run(["select", "--pool", "nope.jsonl", "--query", "x"])
        self.assertEqual(code, 2)
        self.assertIn("nope.jsonl", err)

    def test_bad_pool_line_is_located(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
            handle.write('{"id": "a", "input": "x"}\n')
        self.addCleanup(os.unlink, handle.name)
        code, _, err = run(["select", "--pool", handle.name, "--query", "x"])
        self.assertEqual(code, 2)
        self.assertIn(":1:", err)
        self.assertIn("'output'", err)


if __name__ == "__main__":
    unittest.main()
