#!/usr/bin/env python3
"""Validate a security review report and, with --release, enforce the release gate.

Checks: header fields, every finding has all fields with valid values, Observations
section present. With --release: fails if any Critical/High finding is Open, if any
Accepted finding lacks an entry in docs/security/accepted-risks.md, or if an accepted
risk's review date has passed.

Usage: python3 check_report.py <report.md> [--release] [--risks <accepted-risks.md>]
Exit codes: 0 = valid (and release allowed), 1 = problems or release blocked,
            2 = bad input.
"""
import datetime
import os
import re
import sys

FIELDS = ["Severity", "Status", "Location", "Risk", "How an attacker could use it", "Analogy", "Fix"]
SEVERITIES = {"Critical", "High", "Medium", "Low"}
STATUSES = {"Open", "Fixed", "Accepted"}


def parse_findings(text):
    findings = []
    for m in re.finditer(r"^###\s+(F\d+):\s*(.+?)\s*$(.*?)(?=^###\s|^##\s|\Z)", text, re.M | re.S):
        fields = dict(re.findall(r"^-\s*([^:]+):\s*(.*)$", m.group(3), re.M))
        findings.append((m.group(1), m.group(2), {k.strip(): v.strip() for k, v in fields.items()}))
    return findings


def check(text, release, risks_text, today):
    problems = []
    for h in ("Date:", "Mode:", "Scope:"):
        if not re.search(rf"^{h}\s*\S", text, re.M):
            problems.append(f"Missing header '{h}'")
    if "## Observations" not in text:
        problems.append("Missing '## Observations' section")
    for fid, title, f in parse_findings(text):
        for name in FIELDS:
            if not f.get(name):
                problems.append(f"{fid}: missing '{name}'")
        if f.get("Severity") and f["Severity"] not in SEVERITIES:
            problems.append(f"{fid}: invalid severity '{f['Severity']}'")
        if f.get("Status") and f["Status"] not in STATUSES:
            problems.append(f"{fid}: invalid status '{f['Status']}'")
        if not release:
            continue
        if f.get("Status") == "Open" and f.get("Severity") in ("Critical", "High"):
            problems.append(f"RELEASE BLOCKED: {fid} ({f['Severity']}) is Open")
        if f.get("Status") == "Accepted":
            if title not in risks_text:
                problems.append(f"RELEASE BLOCKED: {fid} Accepted but not recorded in accepted-risks.md")
    if release:
        for m in re.finditer(r"^###\s+(R\d+):.*?^-\s*Review by:\s*(\d{4}-\d{2}-\d{2})", risks_text, re.M | re.S):
            if datetime.date.fromisoformat(m.group(2)) < today:
                problems.append(f"RELEASE BLOCKED: accepted risk {m.group(1)} review date {m.group(2)} has passed")
    return problems


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args else 2)
    report = args[0]
    release = "--release" in args
    risks = os.path.join(os.path.dirname(report), "accepted-risks.md")
    if "--risks" in args:
        i = args.index("--risks")
        if i + 1 >= len(args):
            print("ERROR: --risks needs a path", file=sys.stderr); sys.exit(2)
        risks = args[i + 1]
    try:
        text = open(report, encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR: cannot read {report}: {e}", file=sys.stderr); sys.exit(2)
    risks_text = open(risks, encoding="utf-8").read() if os.path.exists(risks) else ""
    problems = check(text, release, risks_text, datetime.date.today())
    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        sys.exit(1)
    print("PASS: report valid" + (" - release allowed" if release else ""))


if __name__ == "__main__":
    main()
