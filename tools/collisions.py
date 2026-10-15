#!/usr/bin/env python3
"""Surface candidate trigger collisions between skills.

Every positive trigger prompt from each skill's eval suite is scored for lexical overlap
against every skill description. When a prompt scores highly against a skill that does not
own it, that is a CANDIDATE collision — the descriptions compete for the same vocabulary.

This is a candidate finder, not a verdict. Lexical overlap is a crude proxy for what a model
actually does with a description, so the output is a shortlist to review by judgment, and a
quiet result does not prove the descriptions are clean.

Usage: python3 collisions.py <skill-dir> [<skill-dir> ...]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STOP = set("""a an the and or but if then than that this these those of in on at to for with
from by as is are was were be been being it its do does did not no nor so such can could
should would will shall may might must i me my you your we our they them he she his her
one two all any some each both few more most other own same just also very too own what
which who whom when where why how out up down over under again further once here there
only own than too s t don now d ll m o re ve y ain aren couldn didn doesn hadn hasn haven
isn ma mightn mustn needn shan shouldn wasn weren won wouldn want need get got make made
like use using used help please can't im ive theres thats""".split())


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']{3,}", text.lower()) if w not in STOP}


def load(d: Path) -> dict:
    text = (d / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.*?)$", text, re.M)
    desc = m.group(1) if m else ""
    ev = d / "evals" / "evals.json"
    data = json.loads(ev.read_text(encoding="utf-8")) if ev.is_file() else {}
    return {
        "name": d.name,
        "desc_tokens": tokens(desc),
        "positives": [t["query"] for t in data.get("trigger_evals", []) if t.get("should_trigger")],
        "negatives": [t["query"] for t in data.get("trigger_evals", []) if not t.get("should_trigger")],
    }


def score(prompt: str, skill: dict) -> float:
    pt = tokens(prompt)
    if not pt:
        return 0.0
    return len(pt & skill["desc_tokens"]) / len(pt)


def main() -> int:
    dirs = [Path(a) for a in sys.argv[1:]]
    if not dirs:
        print(__doc__)
        return 2
    skills = [load(d) for d in dirs]

    print("CANDIDATE COLLISIONS — a prompt owned by one skill scoring close to another\n")
    flagged = 0
    for owner in skills:
        for prompt in owner["positives"]:
            scores = sorted(((score(prompt, s), s["name"]) for s in skills), reverse=True)
            own = next(sc for sc, n in scores if n == owner["name"])
            rivals = [(sc, n) for sc, n in scores if n != owner["name"] and sc >= own * 0.8 and sc > 0.05]
            if rivals:
                flagged += 1
                print(f"[{owner['name']}] \"{prompt[:76]}\"")
                print(f"    own {own:.2f}  vs  " +
                      "  ".join(f"{n} {sc:.2f}" for sc, n in rivals[:3]))
    print(f"\n{flagged} prompt(s) flagged for manual review.\n")

    print("NEGATIVE PROMPTS scoring high against their own skill (risk of false trigger)\n")
    nflag = 0
    for owner in skills:
        for prompt in owner["negatives"]:
            sc = score(prompt, owner)
            if sc >= 0.20:
                nflag += 1
                print(f"[{owner['name']}] {sc:.2f}  \"{prompt[:72]}\"")
    print(f"\n{nflag} negative prompt(s) flagged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
