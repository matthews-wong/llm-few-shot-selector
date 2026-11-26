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

## Validate

```
make validate
```
