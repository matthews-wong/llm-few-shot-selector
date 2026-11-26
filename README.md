# llm-few-shot-selector

Pick few-shot examples for a prompt from a labelled pool. Examples are ranked
by BM25 similarity to the query, re-ranked with MMR so the picks are not
near-duplicates, and packed whole into a token budget. Stdlib Python, runs
offline.

## Usage

```
python3 -m fewshot select --pool fixtures/pool.jsonl \
    --query "I was charged twice this month" --k 3 --budget 120
```

Pool format is JSONL with `id`, `input` and `output` per line. Output is an
`<examples untrusted="true">` block with one JSON object per line.

## Design notes

- **Whole examples only.** One that does not fit the budget is skipped, never
  cut in half. Tokens are estimated at 4 characters each, so treat the budget
  as approximate.
- **`--diversity`** is the MMR weight on relevance (1.0 = pure BM25, default 0.7).
- **Pool text is untrusted.** Examples are JSON-escaped so an entry containing
  `</examples>` or "ignore previous instructions" stays a quoted string.
  Escaping does not make a model ignore it; keep the block labelled as data
  in your prompt.

## Validate

```
make validate
```

Runs the unit tests and `python3 -m fewshot.evaluate`, which scores each
strategy on the fixture pool (20 examples, 12 queries, k=3): does the
majority label of the picks match the query's label? Latest fixture run:

| strategy | majority correct |
| --- | --- |
| first-k | 3/12 |
| bm25 | 10/12 |
| bm25+mmr | 11/12 |

These are fixture results on a tiny hand-written set, not a benchmark.
