#!/usr/bin/env python3
"""Validate agent-cookbook repo: structure, frontmatter, no leaked secrets."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = ["README.md", "LICENSE", "CONTRIBUTING.md", ".gitignore"]
REQUIRED_DIRS = ["skills", "playbooks", "workflows", "scripts"]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk_live_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"xoxb-[A-Za-z0-9-]{20,}"),
]


def check_structure():
    missing = []
    for f in REQUIRED_FILES:
        if not (ROOT / f).exists():
            missing.append(f)
    for d in REQUIRED_DIRS:
        if not (ROOT / d).is_dir():
            missing.append(d + "/")
    return missing


def check_skills():
    skill_dir = ROOT / "skills"
    skills = list(skill_dir.rglob("SKILL.md"))
    bad = []
    for s in skills:
        text = s.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            bad.append({"file": str(s.relative_to(ROOT)), "issue": "no frontmatter"})
            continue
        if "description" not in text.split("---", 2)[1].lower():
            bad.append({"file": str(s.relative_to(ROOT)), "issue": "no description in frontmatter"})
    return len(skills), bad


def check_playbooks():
    pb = ROOT / "playbooks"
    return [p.name for p in pb.glob("*.md")]


def check_workflows():
    wf = ROOT / "workflows"
    return [p.name for p in wf.glob("*.md")]


def scan_secrets():
    hits = []
    for f in ROOT.rglob("*"):
        if not f.is_file():
            continue
        if any(p == ".git" for p in f.parts):
            continue
        if f.suffix in (".png", ".jpg", ".jpeg", ".mp4", ".gif", ".pdf"):
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(txt):
                hits.append({"file": str(f.relative_to(ROOT)), "pattern": pat.pattern})
    return hits


def main():
    report = {
        "missing_structure": check_structure(),
        "skill_count": None,
        "skill_issues": [],
        "playbooks": [],
        "workflows": [],
        "secret_hits": [],
    }
    n, bad = check_skills()
    report["skill_count"] = n
    report["skill_issues"] = bad
    report["playbooks"] = check_playbooks()
    report["workflows"] = check_workflows()
    report["secret_hits"] = scan_secrets()

    ok = not report["missing_structure"] and not report["secret_hits"]
    report["ok"] = ok
    print(json.dumps(report, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
