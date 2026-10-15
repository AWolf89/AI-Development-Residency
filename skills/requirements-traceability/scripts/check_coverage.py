#!/usr/bin/env python3
"""Verify a trace file before a coverage report is handed over.

Enforces the properties a reader depends on and computes the summary counts so the headline
cannot drift from the table beneath it:

  * every requirement has a valid status
  * every status other than `met` carries an explanation
  * `met` rows carry evidence (a claim of verification needs something to check)
  * `blocked` names a blocker, `deferred` names the agreement, `superseded` references an ID
  * explanations are specific, not filler ("mostly done", "in progress")
  * IDs are unique, and none were invented relative to the source spec when one is given
  * nothing is left in a working state (`not-started`, `in-progress`) at report time

Usage:
    python3 check_coverage.py trace.json
    python3 check_coverage.py trace.json --source SPEC.md    # also check for dropped IDs
    python3 check_coverage.py trace.json --json

Exit codes: 0 clean · 1 problems found · 2 unreadable input
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FINAL_STATUSES = {"met", "partial", "not-met", "blocked", "deferred", "superseded"}
WORKING_STATUSES = {"not-started", "in-progress"}
NEEDS_EXPLANATION = FINAL_STATUSES - {"met"}

ID_RE = re.compile(r"\b(FR|NFR|CON|REQ|R|US)-\d+\b")

FILLER = re.compile(
    r"^\s*(n/?a|tbd|todo|wip|done|not done|mostly done|in progress|partially|"
    r"see above|as discussed|pending|-{1,3}|\.{1,3})\s*$", re.I)

VAGUE_EXPLANATION = re.compile(
    r"\b(mostly|basically|should be fine|probably|more or less|roughly done|"
    r"almost (?:done|complete))\b", re.I)


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "requirements" not in data:
        raise ValueError("trace file must be an object with a 'requirements' array")
    if not isinstance(data["requirements"], list):
        raise ValueError("'requirements' must be an array")
    return data


def explanation_of(req: dict) -> str:
    return " ".join(str(req.get(k, "")) for k in ("notes", "explanation", "gap")).strip()


def check(data: dict, source: Path | None) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    reqs = data["requirements"]

    if not data.get("confirmed_by_requester", False):
        warnings.append(
            "confirmed_by_requester is false — the requirement list was never agreed. "
            "A coverage report against an unconfirmed list can only prove self-consistency.")

    seen: dict[str, int] = {}
    counts = {s: 0 for s in sorted(FINAL_STATUSES)}

    for idx, req in enumerate(reqs):
        rid = str(req.get("id", "")).strip() or f"<row {idx + 1}>"
        text = str(req.get("text", "")).strip()
        status = str(req.get("status", "")).strip().lower()
        evidence = str(req.get("evidence", "")).strip()
        expl = explanation_of(req)

        if rid in seen:
            errors.append(f"{rid}: duplicate ID (also at row {seen[rid] + 1}). "
                          "Every requirement must appear exactly once.")
        seen[rid] = idx

        if not text:
            errors.append(f"{rid}: requirement text is empty.")

        if status in WORKING_STATUSES:
            errors.append(f"{rid}: status is '{status}' — work-in-progress statuses are not "
                          "reportable. Resolve to met/partial/not-met/blocked/deferred.")
            continue
        if status not in FINAL_STATUSES:
            errors.append(f"{rid}: invalid status '{status or '(empty)'}'. "
                          f"Allowed: {', '.join(sorted(FINAL_STATUSES))}.")
            continue

        counts[status] += 1

        if status == "met":
            if not evidence or FILLER.match(evidence):
                errors.append(f"{rid}: marked 'met' without checkable evidence. "
                              "'met' claims verification — cite a file, test, or section, "
                              "or downgrade to 'partial'.")
        else:
            if not expl or FILLER.match(expl):
                errors.append(f"{rid}: status '{status}' needs an explanation saying what is "
                              "missing and why. An unexplained gap is nearly as unhelpful "
                              "as a hidden one.")
            elif VAGUE_EXPLANATION.search(expl):
                warnings.append(f"{rid}: explanation is vague ('{expl[:60]}'). "
                                "Name the specific gap the reader should act on.")

        if status == "blocked" and not re.search(r"\b(block|wait|depend|need|require|owner|"
                                                 r"access|decision)\w*\b", expl, re.I):
            warnings.append(f"{rid}: 'blocked' should name the blocker and who can clear it.")
        if status == "deferred" and not re.search(r"\b(agree|approved|confirmed|requester|"
                                                  r"decided|sign.?off|next (sprint|release|phase))\b",
                                                  expl, re.I):
            warnings.append(f"{rid}: 'deferred' claims the requester agreed. Reference that "
                            "agreement, or use 'not-met'.")
        if status == "superseded" and not ID_RE.search(expl + " " + str(req.get("superseded_by", ""))):
            errors.append(f"{rid}: 'superseded' must reference the replacing requirement by ID.")

    if source is not None:
        if not source.is_file():
            warnings.append(f"source file not found: {source}; skipped dropped-ID check.")
        else:
            src_text = source.read_text(encoding="utf-8")
            src_ids = {m.group(0) for m in ID_RE.finditer(src_text)}
            traced = set(seen)
            derived = {str(r.get("id", "")).strip() for r in reqs
                       if str(r.get("source", "")).strip().lower() == "derived"}
            dropped = sorted(src_ids - traced)
            # Already-declared derived requirements are expected to be absent from the
            # source — that is the point of marking them.
            invented = sorted(i for i in traced - src_ids - derived if ID_RE.fullmatch(i))
            for d in dropped:
                errors.append(f"{d} appears in {source.name} but is missing from the trace. "
                              "Silently dropped requirements are the exact failure this "
                              "report exists to prevent.")
            for i in invented:
                warnings.append(f"{i} is in the trace but not in {source.name}. "
                                "If derived, mark source='derived' so it reads as your "
                                "inference rather than the requester's ask.")

    total = sum(counts.values())
    summary = {"total": total, **counts,
               "fully_covered": counts["met"],
               "needs_attention": total - counts["met"] - counts["superseded"]}
    return errors, warnings, summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("trace", help="Path to trace.json")
    ap.add_argument("--source", help="Original spec, to detect dropped or invented IDs")
    ap.add_argument("--json", action="store_true", help="Emit results as JSON")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = ap.parse_args(argv)

    path = Path(args.trace)
    if not path.is_file():
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 2
    try:
        data = load(path)
        errors, warnings, summary = check(data, Path(args.source) if args.source else None)
    except Exception as exc:
        print(f"ERROR: could not check {path}: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"summary": summary, "errors": errors, "warnings": warnings}, indent=2))
    else:
        print(f"{summary['total']} requirements tracked · "
              f"{summary['met']} met · {summary['partial']} partial · "
              f"{summary['not-met']} not met · {summary['blocked']} blocked · "
              f"{summary['deferred']} deferred · {summary['superseded']} superseded")
        print(f"{summary['needs_attention']} requirement(s) need attention in the report.\n")
        for e in errors:
            print(f"ERROR    {e}")
        for w in warnings:
            print(f"WARNING  {w}")
        if not errors and not warnings:
            print("PASS  trace is internally consistent and reportable.")
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")

    if errors:
        return 1
    return 1 if (warnings and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
