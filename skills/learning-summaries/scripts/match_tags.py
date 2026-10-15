#!/usr/bin/env python3
"""Map proposed topic tags onto existing Notion multi-select tags, to prevent tag drift.

Tag drift is cumulative and quiet: "API", "APIs", and "REST APIs" become three filters that
each find a third of the relevant summaries. Deciding whether two tags are "the same" by eye
is inconsistent from one summary to the next, so the mechanical part — case, plurals,
punctuation, spacing, and a short list of known equivalents — is done here, the same way
every time.

What this does NOT decide: whether two genuinely different words mean the same thing
("Version control" vs "Git"). Those are reported as new, and the caller judges.

Usage:
    match_tags.py --existing "API,Notion,Git" --proposed "APIs,notion databases,GitHub"
    match_tags.py --existing-file tags.txt --proposed "..." --json

Exit codes: 0 ok · 2 bad input
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Known equivalents: normalized form -> canonical normalized form.
# Kept deliberately short. Add pairs only when the same drift has actually happened.
ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "gh": "github",
    "ai": "artificial intelligence",
    "llm": "large language model",
    "llms": "large language model",
    "db": "database",
    "k8s": "kubernetes",
    "ci cd": "cicd",
    "ci/cd": "cicd",
}


def normalize(tag: str) -> str:
    t = tag.strip().lower()
    t = re.sub(r"[_\-/.]+", " ", t)
    t = re.sub(r"[^a-z0-9 +#]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = ALIASES.get(t, t)
    # Singularize each word conservatively: "apis" -> "api", "databases" -> "database".
    words = []
    for w in t.split():
        if len(w) > 3 and w.endswith("ies"):
            w = w[:-3] + "y"
        elif len(w) > 4 and w.endswith("sses"):
            w = w[:-2]  # classes -> class, processes -> process
        elif len(w) > 3 and w.endswith("ses") and not w.endswith("sses"):
            w = w[:-1]
        elif len(w) > 2 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
            w = w[:-1]
        words.append(w)
    t = " ".join(words)
    return ALIASES.get(t, t)


def variants(n: str) -> list[str]:
    """Forms to try against the index, most exact first.

    normalize() singularizes conservatively, so it leaves words like "apis" alone (the same
    rule protects "analysis"). Trying a trailing-s-stripped form as a fallback catches
    acronym plurals without making normalize() mangle real words.
    """
    out = [n]
    stripped = " ".join(w[:-1] if len(w) > 2 and w.endswith("s") else w for w in n.split())
    if stripped != n:
        out.append(stripped)
    return out


def match(existing: list[str], proposed: list[str]) -> list[dict]:
    index: dict[str, str] = {}
    for tag in existing:
        for v in variants(normalize(tag)):
            index.setdefault(v, tag)

    results = []
    seen_final: set[str] = set()
    for p in proposed:
        n = normalize(p)
        if not n:
            continue
        hit = next((index[v] for v in variants(n) if v in index), None)
        if hit is not None:
            final, action = hit, "reuse"
        else:
            # A proposed multi-word tag containing an existing single tag as a whole word
            # (e.g. "notion databases" vs "Notion") is a candidate, not an automatic match.
            contained = [orig for norm, orig in index.items()
                         if " " not in norm and re.search(rf"\b{re.escape(norm)}\b", n)]
            if contained:
                final, action = contained[0], "reuse-broader"
            else:
                final, action = p.strip().title() if p.strip().islower() else p.strip(), "new"
        key = normalize(final)
        if key in seen_final:
            action = "duplicate-dropped"
        seen_final.add(key)
        results.append({"proposed": p.strip(), "use": final, "action": action})
    return results


def split_list(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--existing", default="", help="Comma-separated existing tags")
    src.add_argument("--existing-file", help="File with one existing tag per line")
    ap.add_argument("--proposed", required=True, help="Comma-separated proposed topics")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.existing_file:
        p = Path(args.existing_file)
        if not p.is_file():
            print(f"ERROR: no such file: {p}", file=sys.stderr)
            return 2
        existing = [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    else:
        existing = split_list(args.existing)

    proposed = split_list(args.proposed)
    if not proposed:
        print("ERROR: --proposed is empty.", file=sys.stderr)
        return 2

    results = match(existing, proposed)
    final = [r["use"] for r in results if r["action"] != "duplicate-dropped"]

    if args.json:
        print(json.dumps({"results": results, "final_tags": final}, indent=2))
        return 0

    labels = {
        "reuse": "REUSE  ",
        "reuse-broader": "BROADER",
        "new": "NEW    ",
        "duplicate-dropped": "DROPPED",
    }
    for r in results:
        print(f"{labels[r['action']]}  {r['proposed']!r:32} -> {r['use']}")
    print(f"\nFinal tags: {', '.join(final)}")
    if any(r["action"] == "reuse-broader" for r in results):
        print("BROADER = mapped to an existing tag contained in the proposed one. Usually "
              "right; override only if the narrower topic deserves its own filter.")
    if len(final) > 5:
        print(f"Note: {len(final)} tags. 2–5 keeps the table filterable — consider broader ones.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
