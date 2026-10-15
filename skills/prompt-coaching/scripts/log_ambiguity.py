#!/usr/bin/env python3
"""Log coaching points across tasks and report which ambiguity patterns actually recur.

Recency bias makes the most recent guess feel like the pattern. Counting is mechanical, so
it belongs in a script rather than in an impression — a category that has come up five times
over a month is worth raising once; the one that came up loudly yesterday usually is not.

The log is a local JSON file. Nothing is sent anywhere, and no task content is stored beyond
the short label you pass.

Usage:
    log_ambiguity.py --add --category unstated-audience \\
        --phrase "write up what we did" --task "release notes" [--raised]
    log_ambiguity.py --report [--since-days 60] [--threshold 3]
    log_ambiguity.py --report --json
    log_ambiguity.py --mark-raised unstated-audience

Default log location: ./.ambiguity-log.json (override with --log).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

CATEGORIES = [
    "undefined-term", "unstated-scope", "missing-success-criteria", "implied-constraint",
    "ambiguous-referent", "unstated-audience", "unstated-format", "conflicting-statements",
    "example-as-specification", "missing-context",
]

DEFAULT_LOG = Path(".ambiguity-log.json")


def load(path: Path) -> dict:
    if not path.exists():
        return {"entries": [], "patterns_raised": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"log file is not valid JSON ({exc}). "
                         "Fix or delete it; nothing else depends on it.") from exc
    data.setdefault("entries", [])
    data.setdefault("patterns_raised", {})
    return data


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def add_entry(data: dict, category: str, phrase: str, task: str, raised: bool) -> dict:
    if category not in CATEGORIES:
        raise ValueError(f"unknown category '{category}'.\nUse one of:\n  "
                         + "\n  ".join(CATEGORIES))
    entry = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "category": category,
        "phrase": phrase[:200],
        "task": task[:120],
        "raised_with_user": bool(raised),
    }
    data["entries"].append(entry)
    return entry


def report(data: dict, since_days: int, threshold: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
    recent = []
    for e in data["entries"]:
        try:
            d = datetime.strptime(e["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except (ValueError, KeyError):
            continue
        if d >= cutoff:
            recent.append(e)

    counts = Counter(e["category"] for e in recent)
    tasks = len({e.get("task", "") for e in recent})
    raised = data.get("patterns_raised", {})

    patterns = []
    for category, count in counts.most_common():
        if count < threshold:
            continue
        last_raised = raised.get(category)
        patterns.append({
            "category": category,
            "count": count,
            "examples": [e["phrase"] for e in recent if e["category"] == category][:3],
            "last_raised": last_raised,
            "worth_raising": last_raised is None,
        })

    return {
        "window_days": since_days,
        "entries_in_window": len(recent),
        "distinct_tasks": tasks,
        "counts": dict(counts),
        "patterns": patterns,
    }


def print_report(r: dict) -> None:
    print(f"{r['entries_in_window']} coaching point(s) across {r['distinct_tasks']} "
          f"task(s) in the last {r['window_days']} days.\n")
    if not r["counts"]:
        print("Nothing logged in this window.")
        return
    width = max(len(c) for c in r["counts"])
    for cat, n in sorted(r["counts"].items(), key=lambda kv: -kv[1]):
        print(f"  {cat.ljust(width)}  {n}")
    print()
    if not r["patterns"]:
        print("No category has recurred often enough to raise as a pattern yet. "
              "Keep the per-task notes; don't generalize from one or two.")
        return
    for p in r["patterns"]:
        if p["worth_raising"]:
            print(f"PATTERN  '{p['category']}' has come up {p['count']} times and has not "
                  "been raised as a pattern yet. Worth mentioning once, then logging it "
                  "with --mark-raised.")
        else:
            print(f"(already raised {p['last_raised']})  '{p['category']}' — {p['count']} "
                  "occurrences. Don't repeat it; repetition reads as nagging.")
        for ex in p["examples"]:
            print(f"           e.g. \"{ex}\"")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=str(DEFAULT_LOG))
    ap.add_argument("--add", action="store_true", help="Record a coaching point")
    ap.add_argument("--category", help=f"One of: {', '.join(CATEGORIES)}")
    ap.add_argument("--phrase", help="The ambiguous phrase from the request")
    ap.add_argument("--task", default="", help="Short label for the task")
    ap.add_argument("--raised", action="store_true",
                    help="This point was mentioned to the user in the task feedback")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--since-days", type=int, default=60)
    ap.add_argument("--threshold", type=int, default=3,
                    help="Occurrences before a category counts as a pattern")
    ap.add_argument("--mark-raised", metavar="CATEGORY",
                    help="Record that this pattern has been raised with the user")
    ap.add_argument("--list-categories", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.list_categories:
        print("\n".join(CATEGORIES))
        return 0

    path = Path(args.log)
    try:
        data = load(path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.add:
        if not args.category or not args.phrase:
            print("ERROR: --add requires --category and --phrase.", file=sys.stderr)
            return 2
        try:
            entry = add_entry(data, args.category, args.phrase, args.task, args.raised)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        save(path, data)
        if not args.json:
            print(f"Logged {entry['category']} for '{entry['task'] or 'untitled task'}'.")
        else:
            print(json.dumps(entry, indent=2))
        return 0

    if args.mark_raised:
        if args.mark_raised not in CATEGORIES:
            print(f"ERROR: unknown category '{args.mark_raised}'.", file=sys.stderr)
            return 2
        data["patterns_raised"][args.mark_raised] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        save(path, data)
        print(f"Marked '{args.mark_raised}' as raised.")
        return 0

    if args.report:
        r = report(data, args.since_days, args.threshold)
        print(json.dumps(r, indent=2)) if args.json else print_report(r)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
