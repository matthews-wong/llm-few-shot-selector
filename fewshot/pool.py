"""Example pool: the labelled input/output pairs we pick from."""
import json
import re
from dataclasses import dataclass

CHARS_PER_TOKEN = 4  # rough English average; good enough to budget, not to bill
_WORD = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class Example:
    id: str
    input: str
    output: str


def tokenize(text):
    return _WORD.findall(text.lower())


def estimate_tokens(text):
    return -(-len(text) // CHARS_PER_TOKEN)


def example_tokens(example):
    return estimate_tokens(example.input) + estimate_tokens(example.output)


def load_pool(path):
    """Read a JSONL pool; fail with the file, line and field that is wrong."""
    examples = []
    seen = set()
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{number}: invalid JSON: {exc.msg}") from exc
            for field in ("id", "input", "output"):
                if not isinstance(row.get(field), str) or not row[field]:
                    raise ValueError(f"{path}:{number}: missing or empty string field {field!r}")
            if row["id"] in seen:
                raise ValueError(f"{path}:{number}: duplicate id {row['id']!r}")
            seen.add(row["id"])
            examples.append(Example(row["id"], row["input"], row["output"]))
    return examples
