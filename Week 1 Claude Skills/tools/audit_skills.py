#!/usr/bin/env python3
"""Audit skill folders against the Enterprise Skill Build Checklist.

Only checks what can be checked mechanically. Triggering accuracy and output quality are
judgment calls that need evals and review — this script deliberately does not pretend to
measure them, and a clean audit here is necessary, not sufficient.

Usage: python3 audit_skills.py <skill-dir> [<skill-dir> ...]
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

MUST = "MUST"
SHOULD = "SHOULD"


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def metadata_block(text: str) -> dict:
    """Parse the indented key: value pairs under a `metadata:` line in frontmatter."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out: dict = {}
    in_meta = False
    for line in m.group(1).splitlines():
        if re.match(r"^metadata:\s*$", line):
            in_meta = True
            continue
        if in_meta:
            if line.startswith((" ", "\t")) and ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
            elif line.strip() == "":
                continue
            else:
                in_meta = False
    return out


def audit(d: Path) -> list[tuple[str, str, str]]:
    """Return (level, check, message) for each failure."""
    f: list[tuple[str, str, str]] = []
    skill_md = d / "SKILL.md"

    if not skill_md.is_file():
        return [(MUST, "structure", "no SKILL.md")]

    text = skill_md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    meta = metadata_block(text)
    body = text.split("---", 2)[-1]
    desc = fm.get("description", "")

    # §0 scope & ownership
    if not fm.get("name"):
        f.append((MUST, "frontmatter", "no name"))
    if fm.get("name") and fm["name"] != d.name:
        f.append((SHOULD, "frontmatter", f"name '{fm['name']}' != folder '{d.name}'"))
    owner = fm.get("owner") or meta.get("owner") or meta.get("author") or ""
    if not owner:
        f.append((MUST, "ownership", "no owner/author in frontmatter or metadata"))
    elif owner.upper().startswith("TBD"):
        f.append((MUST, "ownership", "owner is TBD — merge blocker"))

    # §1 triggering
    if not desc:
        f.append((MUST, "description", "no description"))
    else:
        if len(desc) < 120:
            f.append((SHOULD, "description", f"short ({len(desc)} chars) — may lack triggers"))
        # The checklist asks that the description state WHEN to use the skill, not that it
        # use one particular phrasing. "Use after completing…" satisfies it as well as
        # "Use when…".
        if not re.search(r"\buse (when|after|whenever|during|for|on)\b", desc, re.I):
            f.append((MUST, "description", "no 'Use when' trigger conditions"))
        if not re.search(r"do not use|don't use", desc, re.I):
            f.append((MUST, "description", "no exclusions ('Do NOT use for…')"))
        if re.search(r"\b(helps? with|assists? with)\b", desc, re.I):
            f.append((MUST, "description", "vague phrasing ('helps with')"))
        # The checklist requires both third person AND real user phrasings, and real
        # phrasings are often first person ("add this to my notes"). Quoted text is the
        # user's voice, not the description's, so it is excluded from this check.
        unquoted = re.sub(r"\"[^\"]*\"|“[^”]*”", "", desc)
        if re.search(r"\b(I|me|my|you|your)\b", unquoted):
            f.append((MUST, "description", "not written in third person"))

    # §2 progressive disclosure
    lines = body.strip().splitlines()
    if len(lines) > 320:
        f.append((SHOULD, "disclosure", f"body is {len(lines)} lines — consider moving detail "
                                        "into references/"))
    refs = sorted((d / "references").glob("*.md")) if (d / "references").is_dir() else []
    for r in refs:
        if f"references/{r.name}" not in body:
            f.append((MUST, "disclosure", f"references/{r.name} never linked from SKILL.md"))

    # §3 determinism
    scripts = sorted((d / "scripts").glob("*.py")) if (d / "scripts").is_dir() else []
    for s in scripts:
        if f"scripts/{s.name}" not in body:
            f.append((MUST, "determinism", f"scripts/{s.name} never invoked from SKILL.md"))
        src = s.read_text(encoding="utf-8")
        if '"""' not in src[:400]:
            f.append((SHOULD, "determinism", f"{s.name}: no module docstring"))
        if "sys.exit" not in src:
            f.append((SHOULD, "determinism", f"{s.name}: no explicit exit codes"))
        r = subprocess.run([sys.executable, str(s), "--help"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            f.append((MUST, "determinism", f"{s.name}: --help failed (not independently runnable)"))

    # §4 governance
    ver = fm.get("version") or meta.get("version")
    if not ver:
        f.append((MUST, "governance", "no version in frontmatter or metadata"))
    elif not re.match(r"^\d+\.\d+\.\d+$", ver):
        f.append((MUST, "governance", f"version '{ver}' is not semantic"))
    if not (d / "CHANGELOG.md").is_file():
        f.append((MUST, "governance", "no CHANGELOG.md"))
    for s in scripts:
        src = s.read_text(encoding="utf-8")
        if re.search(r"(api[_-]?key|secret|password|token)\s*=\s*[\"'][^\"']{8,}", src, re.I):
            f.append((MUST, "governance", f"{s.name}: possible hardcoded secret"))

    # §5 evals
    ev = d / "evals" / "evals.json"
    if not ev.is_file():
        f.append((MUST, "evals", "no evals/evals.json"))
    else:
        try:
            data = json.loads(ev.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            f.append((MUST, "evals", f"evals.json invalid: {exc}"))
            return f
        oq = data.get("output_quality_evals", [])
        tr = data.get("trigger_evals", [])
        if not oq:
            f.append((MUST, "evals", "no output-quality evals"))
        if not tr:
            f.append((MUST, "evals", "no trigger evals"))
        neg = [t for t in tr if not t.get("should_trigger")]
        pos = [t for t in tr if t.get("should_trigger")]
        if not neg:
            f.append((MUST, "evals", "no negative trigger cases"))
        if len(neg) < 3:
            f.append((SHOULD, "evals", f"only {len(neg)} negative cases"))
        if len(pos) < 3:
            f.append((SHOULD, "evals", f"only {len(pos)} positive cases"))
        if data.get("version") and data["version"] != (fm.get("version") or meta.get("version")):
            f.append((SHOULD, "evals", "eval version does not match skill version"))
    return f


def main() -> int:
    dirs = [Path(a) for a in sys.argv[1:]]
    if not dirs:
        print(__doc__)
        return 2

    total_must = 0
    for d in dirs:
        fails = audit(d)
        musts = [x for x in fails if x[0] == MUST]
        shoulds = [x for x in fails if x[0] == SHOULD]
        total_must += len(musts)
        status = "BLOCKED" if musts else ("OK" if not shoulds else "OK (with notes)")
        print(f"\n=== {d.name} — {status} · {len(musts)} must, {len(shoulds)} should ===")
        for level, check, msg in musts + shoulds:
            print(f"  {level:6} [{check}] {msg}")
        if not fails:
            print("  all mechanical checks pass")

    print(f"\n{'=' * 60}\nTotal MUST failures across {len(dirs)} skills: {total_must}")
    return 1 if total_must else 0


if __name__ == "__main__":
    sys.exit(main())
