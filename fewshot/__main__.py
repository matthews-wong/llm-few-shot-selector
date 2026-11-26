import argparse
import sys

from .pool import load_pool
from .render import render
from .selector import DEFAULT_LAMBDA, select


def main(argv=None):
    parser = argparse.ArgumentParser(prog="fewshot")
    sub = parser.add_subparsers(dest="command", required=True)
    pick = sub.add_parser("select", help="print the examples chosen for a query")
    pick.add_argument("--pool", required=True)
    pick.add_argument("--query", required=True)
    pick.add_argument("--k", type=int, default=3)
    pick.add_argument("--budget", type=int, help="max estimated tokens for all examples")
    pick.add_argument("--diversity", type=float, default=DEFAULT_LAMBDA)
    args = parser.parse_args(argv)
    try:
        pool = load_pool(args.pool)
        chosen = select(args.query, pool, args.k, args.budget, args.diversity)
    except (OSError, ValueError) as exc:
        print(f"fewshot: {exc}", file=sys.stderr)
        return 2
    print(render(chosen))
    return 0


if __name__ == "__main__":
    sys.exit(main())
