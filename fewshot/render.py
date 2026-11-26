"""Render selected examples as a delimited, labelled data block."""
import json

OPEN_TAG = "<examples untrusted=\"true\">"
CLOSE_TAG = "</examples>"


def render(examples):
    """Examples come from a pool we do not fully control, so each is emitted as
    a JSON string: quotes and newlines are escaped and a pool entry cannot
    close the block or pose as an instruction."""
    lines = [OPEN_TAG]
    for example in examples:
        lines.append(json.dumps(
            {"id": example.id, "input": example.input, "output": example.output},
            ensure_ascii=True,
        ))
    lines.append(CLOSE_TAG)
    return "\n".join(lines)
