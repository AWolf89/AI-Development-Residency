#!/usr/bin/env python3
"""Extract candidate requirements from a spec, ticket, or prose request into trace.json.

Two modes, chosen automatically:
  structured  — the source already has IDs (FR-1, NFR-2, R-3). IDs are preserved exactly,
                because renumbering breaks traceability against the original document.
  prose       — no IDs found. Lines are split into candidates using obligation language and
                list structure, then numbered R-1..R-n.

The output is a DRAFT for a human to correct. This script cannot tell a requirement from an
aside, and it deliberately over-splits rather than under-splits, since a spurious row is
cheap and a missed one is the failure this whole skill exists to prevent.

Usage:
    python3 extract_requirements.py SPEC.md --out trace.json
    python3 extract_requirements.py SPEC.md --prefix FR --out trace.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"\b(FR|NFR|CON|REQ|R|AC|US)-(\d+)(?:\.(\d+))?\b")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$")
BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")

OBLIGATION = re.compile(
    r"\b(shall|must|should|will|needs? to|has to|have to|is required to|"
    r"we need|it needs|required|ensure that|make sure)\b", re.I)

# Sections whose content is context, not deliverables.
NON_REQUIREMENT_HEADINGS = re.compile(
    r"^\s*(background|context|problem|rationale|motivation|overview|introduction|"
    r"out of scope|non-goals?|open questions?|glossary|appendix|references?|"
    r"assumptions?|notes?)\b", re.I)

SPLIT_HINT = re.compile(r"\b(and also|and then|, and |; and |, plus |as well as)\b", re.I)


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def _clean(text: str) -> str:
    text = re.sub(r"\*\*|__|`", "", text).strip()
    text = re.sub(r"^[-—–:\s]+", "", text)
    return text.strip()


def extract_structured(lines: list[str]) -> list[dict]:
    """Preserve IDs already present in the source."""
    out: list[dict] = []
    seen: set[str] = set()
    current: dict | None = None

    for i, raw in enumerate(lines, start=1):
        m = ID_RE.search(raw)
        if m and (m.group(1), m.group(3)) and m.group(3) is None:
            ident = f"{m.group(1)}-{m.group(2)}"
            if ident in seen:
                # Duplicate declaration; attach as continuation rather than a new row.
                continue
            seen.add(ident)
            text = _clean(ID_RE.sub("", raw, count=1))
            current = {
                "id": ident,
                "text": text,
                "source": "stated",
                "source_line": i,
                "acceptance_criteria": [],
                "status": "not-started",
                "evidence": "",
                "notes": "",
            }
            out.append(current)
        elif m and m.group(3) is not None and current is not None:
            # AC-1.1 style criterion belongs to its parent requirement.
            current["acceptance_criteria"].append(_clean(ID_RE.sub("", raw, count=1)))
        elif current is not None and raw.strip() and not HEADING_RE.match(raw):
            if not current["text"]:
                current["text"] = _clean(raw)
    return [r for r in out if r["text"]]


def extract_prose(lines: list[str], prefix: str) -> list[dict]:
    """Split unstructured text into candidate requirements."""
    candidates: list[tuple[int, str]] = []
    skipping = False

    for i, raw in enumerate(lines, start=1):
        h = HEADING_RE.match(raw)
        if h:
            skipping = bool(NON_REQUIREMENT_HEADINGS.match(h.group(1)))
            continue
        if skipping:
            continue
        line = raw.strip()
        if not line or line.startswith(">") or line.startswith("|"):
            continue

        b = BULLET_RE.match(raw)
        if b:
            candidates.append((i, _clean(b.group(1))))
            continue
        # Plain sentences only qualify when they carry obligation language.
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            if OBLIGATION.search(sentence) and len(sentence.split()) >= 4:
                candidates.append((i, _clean(sentence)))

    out: list[dict] = []
    n = 0
    for line_no, text in candidates:
        if not text:
            continue
        parts = [p for p in SPLIT_HINT.split(text) if p and not SPLIT_HINT.fullmatch(p)]
        parts = [p.strip(" ,;") for p in parts if len(p.strip(" ,;").split()) >= 3] or [text]
        for part in parts:
            n += 1
            out.append({
                "id": f"{prefix}-{n}",
                "text": part,
                "source": "stated",
                "source_line": line_no,
                "acceptance_criteria": [],
                "status": "not-started",
                "evidence": "",
                "notes": "",
            })
    return out


def flag_compounds(reqs: list[dict]) -> list[str]:
    warnings = []
    for r in reqs:
        words = r["text"].split()
        # Short "X and Y" pairs (CSV and XLSX) hide partial delivery just as effectively as
        # long compound sentences, so flag on the conjunction rather than on length.
        if SPLIT_HINT.search(r["text"]) or (re.search(r"\band\b", r["text"], re.I) and len(words) >= 6):
            warnings.append(
                f"{r['id']} may be compound — if part of it could be delivered while another "
                f"part is skipped, split it: \"{r['text'][:90]}\"")
    return warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="Source spec, ticket, or notes (markdown or plain text)")
    ap.add_argument("--out", default="trace.json", help="Where to write the trace file")
    ap.add_argument("--prefix", default="R", help="ID prefix when the source has none")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 2
    try:
        lines = read_lines(path)
    except Exception as exc:
        print(f"ERROR: could not read {path}: {exc}", file=sys.stderr)
        return 2

    has_ids = any(ID_RE.search(l) for l in lines)
    reqs = extract_structured(lines) if has_ids else extract_prose(lines, args.prefix)
    mode = "structured" if has_ids else "prose"

    if not reqs:
        print(f"ERROR: no candidate requirements found in {path}. "
              "Check the file, or decompose by hand.", file=sys.stderr)
        return 2

    trace = {
        "source_file": str(path),
        "extraction_mode": mode,
        "confirmed_by_requester": False,
        "requirements": reqs,
    }
    Path(args.out).write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")

    if not args.quiet:
        print(f"Extracted {len(reqs)} candidate requirement(s) from {path} ({mode} mode).")
        print(f"Written to {args.out}\n")
        for w in flag_compounds(reqs):
            print(f"REVIEW  {w}")
        print("\nThis is a DRAFT. Confirm the list with the requester, add any derived "
              "requirements, and set confirmed_by_requester to true before starting work.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
