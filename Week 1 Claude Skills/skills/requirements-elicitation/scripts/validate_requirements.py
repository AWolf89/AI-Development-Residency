#!/usr/bin/env python3
"""Validate a requirements document produced by the requirements-elicitation skill.

Checks the mechanical properties that are easy to get wrong and tedious to verify by eye:
ID numbering and uniqueness, acceptance-criteria coverage, vague wording, compound
requirements, and required sections that were left empty.

Usage:
    python3 validate_requirements.py path/to/requirements.md [--json] [--strict]

Exit codes:
    0  no errors (warnings may still be present)
    1  errors found
    2  the file could not be read or parsed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VAGUE_TERMS = [
    "fast", "slow", "quick", "quickly", "scalable", "robust", "secure", "user-friendly",
    "user friendly", "intuitive", "seamless", "flexible", "efficient", "reliable",
    "appropriate", "reasonable", "acceptable", "adequate", "minimal", "optimal",
    "best practice", "industry standard", "as needed", "where possible",
    "state-of-the-art", "modern", "etc.", "and so on", "easy to use", "simple",
]

REQUIRED_SECTIONS = [
    "Problem",
    "Users and stakeholders",
    "Goals and success measures",
    "Scope",
    "Functional requirements",
    "Non-functional requirements",
    "Constraints",
    "Assumptions",
    "Open questions",
]

MODAL_VERBS = ("shall", "should", "may", "must", "will")

REQ_ID_RE = re.compile(r"\*\*(FR|NFR|CON|A|G|Q)-(\d+)\*\*|^(FR|NFR|CON|A|G|Q)-(\d+)\b")
AC_ID_RE = re.compile(r"\bAC-(\d+)\.(\d+)\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


@dataclass
class Finding:
    level: str  # "error" | "warning"
    check: str
    line: int
    message: str


@dataclass
class Document:
    lines: list[str]
    sections: dict[str, list[str]] = field(default_factory=dict)


def parse(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    doc = Document(lines=lines)
    current = "_preamble"
    doc.sections[current] = []
    for line in lines:
        m = HEADING_RE.match(line)
        # Only top-level headings open a new section; h3+ (e.g. "### In scope")
        # belongs to its parent so subsections don't read as empty parents.
        if m and len(m.group(1)) <= 2:
            current = re.sub(r"^\d+\.\s*", "", m.group(2)).strip()
            doc.sections.setdefault(current, [])
        else:
            doc.sections[current].append(line)
    return doc


def _requirement_lines(doc: Document) -> list[tuple[int, str, str, int]]:
    """Return (line_no, prefix, raw_line, number) for every requirement declaration."""
    out = []
    for i, line in enumerate(doc.lines, start=1):
        m = REQ_ID_RE.search(line)
        if m:
            prefix = m.group(1) or m.group(3)
            number = int(m.group(2) or m.group(4))
            out.append((i, prefix, line, number))
    return out


def check_required_sections(doc: Document) -> list[Finding]:
    findings = []
    present = {k.lower(): v for k, v in doc.sections.items()}
    for name in REQUIRED_SECTIONS:
        key = name.lower()
        match = next((v for k, v in present.items() if key in k), None)
        if match is None:
            findings.append(Finding("error", "required-section", 0,
                                    f"Required section missing: '{name}'."))
        elif not any(l.strip() and not l.strip().startswith("<") for l in match):
            findings.append(Finding("error", "required-section", 0,
                                    f"Required section '{name}' is present but empty."))
    # Out of scope gets its own check because an empty one is a scoping failure.
    body = "\n".join(doc.lines).lower()
    if "out of scope" not in body:
        findings.append(Finding("error", "out-of-scope", 0,
                                "No 'Out of scope' content found. Scope boundaries must be stated."))
    return findings


def check_ids(doc: Document) -> list[Finding]:
    findings = []
    seen: dict[str, list[int]] = {}
    by_prefix: dict[str, list[int]] = {}
    for line_no, prefix, _line, number in _requirement_lines(doc):
        ident = f"{prefix}-{number}"
        seen.setdefault(ident, []).append(line_no)
        by_prefix.setdefault(prefix, []).append(number)

    for ident, locations in seen.items():
        if len(locations) > 1:
            findings.append(Finding("error", "duplicate-id", locations[1],
                                    f"Requirement ID {ident} declared more than once "
                                    f"(lines {', '.join(map(str, locations))})."))

    for prefix, numbers in by_prefix.items():
        ordered = sorted(set(numbers))
        if ordered and ordered[0] != 1:
            findings.append(Finding("warning", "id-sequence", 0,
                                    f"{prefix} IDs start at {prefix}-{ordered[0]}, expected {prefix}-1."))
        gaps = [n for n in range(1, ordered[-1] + 1) if n not in ordered] if ordered else []
        if gaps:
            findings.append(Finding("warning", "id-sequence", 0,
                                    f"{prefix} IDs have gaps at: "
                                    + ", ".join(f"{prefix}-{g}" for g in gaps)
                                    + ". Withdrawn requirements should be marked, not removed."))
    return findings


def check_acceptance_criteria(doc: Document) -> list[Finding]:
    findings = []
    fr_numbers = [(ln, num) for ln, prefix, _l, num in _requirement_lines(doc) if prefix == "FR"]
    text = "\n".join(doc.lines)
    ac_pairs = {(int(a), int(b)) for a, b in AC_ID_RE.findall(text)}
    covered = {a for a, _ in ac_pairs}

    for line_no, num in fr_numbers:
        if num not in covered:
            findings.append(Finding("error", "missing-acceptance-criteria", line_no,
                                    f"FR-{num} has no acceptance criterion (expected AC-{num}.x). "
                                    "A requirement nobody can test cannot be accepted."))

    # Given/When/Then completeness for each AC line.
    for i, line in enumerate(doc.lines, start=1):
        if AC_ID_RE.search(line):
            low = line.lower()
            missing = [w for w in ("given", "when", "then") if w not in low]
            if missing:
                # Allow multi-line ACs: look ahead a few lines before complaining.
                window = " ".join(doc.lines[i - 1:i + 4]).lower()
                missing = [w for w in ("given", "when", "then") if w not in window]
            if missing:
                findings.append(Finding("warning", "acceptance-criteria-form", i,
                                        "Acceptance criterion is missing "
                                        + "/".join(missing)
                                        + ". Use Given / When / Then so the test is unambiguous."))
    return findings


def check_vague_terms(doc: Document) -> list[Finding]:
    findings = []
    skip_section_markers = ("notes on using this template",)
    for i, line in enumerate(doc.lines, start=1):
        low = line.lower()
        if any(marker in low for marker in skip_section_markers):
            continue
        if not REQ_ID_RE.search(line) and not AC_ID_RE.search(line):
            continue
        for term in VAGUE_TERMS:
            if re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", low):
                findings.append(Finding("warning", "vague-term", i,
                                        f"Vague term '{term}' appears in a requirement. "
                                        "Replace it with a number, a named standard, or an "
                                        "observable behavior."))
    return findings


def check_compound_requirements(doc: Document) -> list[Finding]:
    findings = []
    for line_no, prefix, line, number in _requirement_lines(doc):
        if prefix not in ("FR", "NFR"):
            continue
        body = line.split("—", 1)[-1] if "—" in line else line
        low = body.lower()
        modal_count = sum(low.count(f" {v} ") for v in MODAL_VERBS)
        has_and = re.search(r"\band\b", low) is not None
        if modal_count > 1 or (has_and and modal_count >= 1 and len(body.split()) > 18):
            findings.append(Finding("warning", "compound-requirement", line_no,
                                    f"{prefix}-{number} looks like more than one requirement. "
                                    "Split it so each can be independently accepted."))
    return findings


def check_modal_verbs(doc: Document) -> list[Finding]:
    findings = []
    for line_no, prefix, line, number in _requirement_lines(doc):
        if prefix not in ("FR", "NFR"):
            continue
        low = line.lower()
        if not any(re.search(rf"\b{v}\b", low) for v in MODAL_VERBS):
            findings.append(Finding("warning", "missing-modal", line_no,
                                    f"{prefix}-{number} has no shall/should/may. "
                                    "State obligation explicitly so priority is not inferred."))
    return findings


def check_placeholders(doc: Document) -> list[Finding]:
    findings = []
    for i, line in enumerate(doc.lines, start=1):
        if re.search(r"<[a-z][^>]{2,}>", line) or "TBD" in line or "TODO" in line:
            findings.append(Finding("warning", "unfilled-placeholder", i,
                                    "Unfilled placeholder left in the document."))
    return findings


CHECKS = (
    check_required_sections,
    check_ids,
    check_acceptance_criteria,
    check_vague_terms,
    check_compound_requirements,
    check_modal_verbs,
    check_placeholders,
)


def validate(path: Path) -> list[Finding]:
    doc = parse(path)
    findings: list[Finding] = []
    for check in CHECKS:
        findings.extend(check(doc))
    return sorted(findings, key=lambda f: (f.level != "error", f.line))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="Path to the requirements markdown document")
    ap.add_argument("--json", action="store_true", help="Emit findings as JSON")
    ap.add_argument("--strict", action="store_true",
                    help="Treat warnings as errors (non-zero exit)")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 2
    try:
        findings = validate(path)
    except Exception as exc:  # fail loudly, with context
        print(f"ERROR: could not validate {path}: {exc}", file=sys.stderr)
        return 2

    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(json.dumps({
            "file": str(path),
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [f.__dict__ for f in findings],
        }, indent=2))
    else:
        if not findings:
            print(f"PASS  {path}: no issues found.")
        for f in findings:
            where = f"line {f.line}" if f.line else "document"
            print(f"{f.level.upper():7} [{f.check}] {where}: {f.message}")
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
