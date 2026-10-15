"""Command line: `python -m pipeline check|check-all|known`."""

import argparse
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from pipeline import config
from pipeline.adapters.outbound.repo import RepoError
from pipeline.application.check import check_all, check_week, known_posts


def _monday(value: str) -> date:
    try:
        day = date.fromisoformat(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("use YYYY-MM-DD") from e
    if day.weekday() != 0:
        raise argparse.ArgumentTypeError(f"{value} is not a Monday")
    return day


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pipeline")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="site checkout")
    sub = parser.add_subparsers(dest="command", required=True)
    week = sub.add_parser("check", help="check this week's new posts before publishing")
    week.add_argument("--base", default="origin/main", help="git ref the branch started from")
    week.add_argument("--monday", type=_monday, required=True, help="this week's Monday")
    week.add_argument("--offline", action="store_true", help="skip loading source links")
    sub.add_parser("check-all", help="check format and plain words in every post")
    sub.add_parser("known", help="list published posts, one per line")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    store = config.repo(args.root, getattr(args, "base", "HEAD"))
    try:
        if args.command == "known":
            print("\n".join(known_posts(store)))
            return 0
        if args.command == "check-all":
            problems = check_all(store)
        else:
            report = check_week(store, None if args.offline else config.probe(), args.monday)
            print(f"new posts: {len(report.new_posts)}")
            for name in report.new_posts:
                print(f"  {name}")
            problems = report.problems
    except RepoError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    for problem in problems:
        print(f"PROBLEM {problem}")
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 0 if not problems else 1
