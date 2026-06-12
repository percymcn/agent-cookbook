#!/usr/bin/env python3
"""Dry-run of the self-improving-agent workflow.

Scans this repo's own skills/ tree and runs the same scoring rubric the
prod skill-health-scanner uses. Writes:
  out/health.json     — per-skill scored snapshot
  out/backlog.md      — ranked improvement queue (lowest-scoring first)

No external IO, no model call. The "loop" here is structural — it scores
metadata so the agent loading these skills routes them better.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SKILLS = REPO / "skills"

GENERIC = ("useful", "various", "many", "stuff", "things", "etc")


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    body = text[3:end].strip().splitlines()
    fm: dict = {}
    for line in body:
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip().lower()] = v.strip().strip('"').strip("'")
    return fm


def score_skill(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return {"path": str(path.relative_to(REPO)), "score": -100, "issues": [f"read failed: {exc}"]}

    issues: list[str] = []
    s = 100
    fm = parse_frontmatter(text)
    if fm is None:
        issues.append("no frontmatter")
        s -= 35
        desc = ""
    else:
        desc = fm.get("description", "")
        if not desc:
            issues.append("no description")
            s -= 40
        else:
            if len(desc) < 40:
                issues.append(f"description short ({len(desc)} chars)")
                s -= 40
            if len(desc) > 600:
                issues.append(f"description long ({len(desc)} chars)")
                s -= 10
            if "use when" not in desc.lower():
                issues.append('missing "Use when ..." trigger')
                s -= 15
            for g in GENERIC:
                if re.search(rf"\b{g}\b", desc.lower()):
                    issues.append(f'generic word: "{g}"')
                    s -= 5

    age_days = (time.time() - path.stat().st_mtime) / 86400
    if age_days > 120:
        issues.append(f"stale ({int(age_days)}d)")
        s -= 5

    return {
        "path": str(path.relative_to(REPO)),
        "score": s,
        "description_len": len(desc),
        "issues": issues,
    }


def render_backlog(scored: list[dict]) -> str:
    ranked = sorted(scored, key=lambda r: r["score"])
    lines = ["# Skill health backlog", "",
             f"_Scanned {len(scored)} skills. Lowest-scoring first._", ""]
    for r in ranked[:20]:
        lines.append(f"## {r['path']}  (score {r['score']})")
        if r["issues"]:
            for i in r["issues"]:
                lines.append(f"- {i}")
        else:
            lines.append("- (no issues)")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--skills-dir", default=str(SKILLS))
    ap.add_argument("--out", default=str(HERE / "out"))
    args = ap.parse_args()

    skill_dir = Path(args.skills_dir)
    if not skill_dir.is_dir():
        print(f"[dry-run] skills dir not found: {skill_dir}")
        return 1
    files = list(skill_dir.rglob("SKILL.md"))
    scored = [score_skill(p) for p in files]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "health.json").write_text(json.dumps(scored, indent=2), encoding="utf-8")
    (out / "backlog.md").write_text(render_backlog(scored), encoding="utf-8")

    avg = (sum(r["score"] for r in scored) / len(scored)) if scored else 0
    worst = sorted(scored, key=lambda r: r["score"])[:3]
    print(f"[dry-run] skills scanned: {len(scored)}")
    print(f"[dry-run] avg score: {avg:.1f}")
    print(f"[dry-run] worst 3: {[(r['path'], r['score']) for r in worst]}")
    print(f"[dry-run] artifacts: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
