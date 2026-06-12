#!/usr/bin/env python3
"""Validate agent-cookbook repo: structure, frontmatter, no leaked secrets, examples runnable."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = ["README.md", "LICENSE", "CONTRIBUTING.md", ".gitignore"]
REQUIRED_DIRS = ["skills", "playbooks", "workflows", "scripts", "examples"]

EXAMPLES = [
    "faceless-video-engine",
    "tradeflow-research-pipeline",
    "cold-outreach",
    "newsletter-pipeline",
    "self-improving-agent",
]

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
        parts = f.parts
        if any(p == ".git" for p in parts):
            continue
        # Skip the validator itself — it carries the pattern regexes by design.
        if f == Path(__file__):
            continue
        # Skip example output artifacts.
        if "examples" in parts and "out" in parts:
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


def check_examples():
    """Each example must have README.md + run.py; run.py must exit 0 in --dry-run and emit an artifact."""
    results = []
    ex_root = ROOT / "examples"
    for name in EXAMPLES:
        d = ex_root / name
        entry = {"example": name, "ok": False, "issues": []}
        if not d.is_dir():
            entry["issues"].append("directory missing")
            results.append(entry)
            continue
        if not (d / "README.md").exists():
            entry["issues"].append("README.md missing")
        if not (d / "run.py").exists():
            entry["issues"].append("run.py missing")
            results.append(entry)
            continue
        # Syntax-check.
        syn = subprocess.run(
            [sys.executable, "-c", f"import py_compile; py_compile.compile(r'{d/'run.py'}', doraise=True)"],
            capture_output=True, text=True,
        )
        if syn.returncode != 0:
            entry["issues"].append(f"syntax error: {syn.stderr.strip()}")
            results.append(entry)
            continue
        # Execute dry-run.
        proc = subprocess.run(
            [sys.executable, "run.py", "--dry-run"],
            cwd=d, capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            entry["issues"].append(f"exit {proc.returncode}: {proc.stderr.strip()[-300:]}")
            results.append(entry)
            continue
        # Confirm an artifact landed under out/.
        artifacts = list((d / "out").rglob("*")) if (d / "out").exists() else []
        artifact_files = [a for a in artifacts if a.is_file()]
        if not artifact_files:
            entry["issues"].append("no artifact produced in out/")
            results.append(entry)
            continue
        entry["ok"] = True
        entry["artifacts"] = [str(a.relative_to(d)) for a in artifact_files]
        results.append(entry)
    return results


def main():
    report = {
        "missing_structure": check_structure(),
        "skill_count": None,
        "skill_issues": [],
        "playbooks": [],
        "workflows": [],
        "secret_hits": [],
        "examples": [],
    }
    n, bad = check_skills()
    report["skill_count"] = n
    report["skill_issues"] = bad
    report["playbooks"] = check_playbooks()
    report["workflows"] = check_workflows()
    report["secret_hits"] = scan_secrets()
    report["examples"] = check_examples()

    examples_ok = all(e["ok"] for e in report["examples"]) and len(report["examples"]) == len(EXAMPLES)
    ok = (
        not report["missing_structure"]
        and not report["secret_hits"]
        and examples_ok
    )
    report["ok"] = ok
    print(json.dumps(report, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
