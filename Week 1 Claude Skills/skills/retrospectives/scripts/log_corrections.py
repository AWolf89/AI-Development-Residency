#!/usr/bin/env python3
"""Log corrections across tasks and surface rule candidates at the recurrence threshold.

Recurrence is counted mechanically because recollection is biased: the most recent correction
feels like a pattern and the one from three tasks ago is forgotten. The script decides only
whether something RECURS. Whether it should become a rule is a judgment call made against
references/rule-writing.md, and whether that rule is adopted is the owner's decision.

Nothing here edits a skill. Proposals are recorded, approvals and declines are recorded, and
a declined cause is not re-surfaced as a candidate.

Usage:
    log_corrections.py --add --category wrong-assumption \\
        --what "used the staging DB" --cause "did not ask which environment" \\
        --skill scope-discipline --task "import fix" [--severity moderate]

    log_corrections.py --report [--threshold 2] [--since-days 90]
    log_corrections.py --propose <cause-key> --rule "<the rule as written>"
    log_corrections.py --approve <cause-key> | --decline <cause-key>
    log_corrections.py --list-categories

Default log: ./.corrections-log.json (override with --log)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

CATEGORIES = [
    "wrong-assumption", "missed-requirement", "ignored-instruction", "scope-overreach",
    "wrong-approach", "unasked-question", "quality-miss", "format-miss",
    "existing-rule-not-applied",
]
SEVERITIES = ["minor", "moderate", "major"]
DEFAULT_LOG = Path(".corrections-log.json")
STOPWORDS = {"the", "a", "an", "to", "of", "for", "and", "in", "on", "did", "not", "was",
             "is", "it", "that", "this", "with", "have", "had", "been", "be", "i"}


def cause_key(category: str, cause: str, explicit: str = "") -> tuple[str, bool]:
    """Key used to group occurrences of the same underlying cause.

    Judging whether two corrections share a cause is a semantic call, and word overlap is a
    poor proxy for it — "didn't ask which environment was current" and "didn't ask which
    environment to target" are the same cause with almost no words in common. So the caller
    should pass --cause-key with a short slug they have decided groups these together. The
    derived fallback exists so logging still works without one, and the report says plainly
    when it was used, since under-grouping hides real patterns.

    Returns (key, was_derived).
    """
    if explicit:
        slug = "-".join(re.findall(r"[a-z0-9]+", explicit.lower()))
        if slug:
            return f"{category}:{slug}", False
    words = [w for w in re.findall(r"[a-z0-9]+", cause.lower()) if w not in STOPWORDS]
    return (f"{category}:{'-'.join(sorted(set(words))[:4])}" if words else category), True


def load(path: Path) -> dict:
    if not path.exists():
        return {"entries": [], "proposals": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"log is not valid JSON ({exc}). Fix or delete it.") from exc
    data.setdefault("entries", [])
    data.setdefault("proposals", {})
    return data


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def add(data: dict, args) -> dict:
    if args.category not in CATEGORIES:
        raise ValueError(f"unknown category '{args.category}'.\nUse one of:\n  "
                         + "\n  ".join(CATEGORIES))
    if args.severity not in SEVERITIES:
        raise ValueError(f"severity must be one of: {', '.join(SEVERITIES)}")
    if not args.cause or len(args.cause.split()) < 2:
        raise ValueError("--cause must describe the underlying cause, not a symptom. "
                         "'tests failed' is a symptom; 'assumed tests ran in CI' is a cause.")
    key, derived = cause_key(args.category, args.cause, args.cause_key)
    entry = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "category": args.category,
        "what": args.what[:300],
        "cause": args.cause[:300],
        "cause_key": key,
        "key_derived": derived,
        "skill": args.skill or "",
        "task": args.task[:120],
        "severity": args.severity,
    }
    data["entries"].append(entry)
    return entry


def report(data: dict, threshold: int, since_days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)
    recent = []
    for e in data["entries"]:
        try:
            d = datetime.strptime(e["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except (ValueError, KeyError):
            continue
        if d >= cutoff:
            recent.append(e)

    groups: dict[str, list[dict]] = defaultdict(list)
    for e in recent:
        groups[e.get("cause_key", e["category"])].append(e)

    proposals = data.get("proposals", {})
    candidates, watching = [], []

    for key, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        state = proposals.get(key, {})
        status = state.get("status", "none")
        distinct_tasks = len({i.get("task", "") for i in items})
        record = {
            "cause_key": key,
            "occurrences": len(items),
            "distinct_tasks": distinct_tasks,
            "independent": distinct_tasks >= threshold,
            "severities": sorted({i.get("severity", "minor") for i in items}),
            "target_skill": next((i["skill"] for i in items if i.get("skill")), ""),
            "examples": [i["cause"] for i in items][:3],
            "status": status,
            "derived_keys": any(i.get("key_derived") for i in items),
        }
        (candidates if len(items) >= threshold else watching).append(record)

    return {
        "window_days": since_days,
        "threshold": threshold,
        "entries_in_window": len(recent),
        "candidates": candidates,
        "watching": watching,
    }


def print_report(r: dict) -> None:
    print(f"{r['entries_in_window']} correction(s) logged in the last {r['window_days']} days. "
          f"Threshold: {r['threshold']} occurrences.\n")

    actionable = [c for c in r["candidates"] if c["status"] in ("none", "deferred")]
    for c in r["candidates"]:
        if c["status"] == "declined":
            print(f"DECLINED   {c['cause_key']} ({c['occurrences']}x) — do not re-propose. "
                  "Further recurrences are new evidence, raised once, not the same proposal.")
            continue
        if c["status"] == "proposed":
            print(f"AWAITING   {c['cause_key']} ({c['occurrences']}x) — proposed, "
                  "waiting on the owner. Don't restate it.")
            continue
        if c["status"] == "approved":
            print(f"APPROVED   {c['cause_key']} ({c['occurrences']}x) — make the skill edit "
                  "as a separate reviewable change with a changelog entry and version bump.")
            continue

        if not c["independent"]:
            print(f"COINCIDENCE? {c['cause_key']} ({c['occurrences']}x across only "
                  f"{c['distinct_tasks']} task) — same cause, same context. That is closer to "
                  "one event seen twice than a pattern. Keep logging.")
            continue

        skill = c["target_skill"] or "<no target skill recorded>"
        print(f"CANDIDATE  {c['cause_key']} — {c['occurrences']}x across "
              f"{c['distinct_tasks']} tasks, severity {'/'.join(c['severities'])}, "
              f"target: {skill}")
        for ex in c["examples"]:
            print(f"             e.g. \"{ex}\"")
        print("             → Run the generalization test in references/rule-writing.md "
              "BEFORE proposing. A count is not a rule.")

    for w in r["watching"]:
        note = "  (key auto-derived — check it isn't the same cause as another line)" \
            if w.get("derived_keys") else ""
        print(f"watching   {w['cause_key']} ({w['occurrences']}x) — below threshold.{note}")

    if not r["candidates"] and not r["watching"]:
        print("Nothing logged in this window.")
    elif not actionable:
        print("\nNo new candidates needing a decision.")


def set_status(data: dict, key: str, status: str, rule: str | None) -> None:
    entry = data["proposals"].setdefault(key, {})
    entry["status"] = status
    entry[f"{status}_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if rule:
        entry["rule"] = rule


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=str(DEFAULT_LOG))
    ap.add_argument("--add", action="store_true")
    ap.add_argument("--category")
    ap.add_argument("--what", default="")
    ap.add_argument("--cause", default="")
    ap.add_argument("--cause-key", default="",
                    help="Short slug grouping this with earlier corrections of the SAME cause "
                         "(e.g. unasked-environment). Supply it — word matching cannot judge "
                         "sameness reliably.")
    ap.add_argument("--skill", default="")
    ap.add_argument("--task", default="")
    ap.add_argument("--severity", default="minor", help=f"{', '.join(SEVERITIES)}")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--threshold", type=int, default=2)
    ap.add_argument("--since-days", type=int, default=90)
    ap.add_argument("--propose", metavar="CAUSE_KEY")
    ap.add_argument("--rule", default="", help="The proposed rule, recorded with --propose")
    ap.add_argument("--approve", metavar="CAUSE_KEY")
    ap.add_argument("--decline", metavar="CAUSE_KEY")
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
        if not args.category or not args.what:
            print("ERROR: --add requires --category and --what.", file=sys.stderr)
            return 2
        try:
            entry = add(data, args)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        save(path, data)
        print(json.dumps(entry, indent=2) if args.json else
              f"Logged {entry['category']} (key: {entry['cause_key']}) "
              f"for '{entry['task'] or 'untitled'}'.")
        return 0

    for flag, status in (("propose", "proposed"), ("approve", "approved"), ("decline", "declined")):
        key = getattr(args, flag)
        if key:
            if status == "proposed" and not args.rule:
                print("ERROR: --propose requires --rule, so the proposal is recorded in the "
                      "words it was put to the owner.", file=sys.stderr)
                return 2
            set_status(data, key, status, args.rule or None)
            save(path, data)
            print(f"Marked '{key}' as {status}."
                  + (" Do not re-propose it." if status == "declined" else ""))
            return 0

    if args.report:
        r = report(data, args.threshold, args.since_days)
        print(json.dumps(r, indent=2)) if args.json else print_report(r)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # Normal when piping into head/less — not an error worth a traceback.
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
