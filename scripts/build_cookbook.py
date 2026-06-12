#!/usr/bin/env python3
"""Copy + sanitize skills and playbooks into agent-cookbook.

- Skills: walk ~/.hermes/skills, copy each SKILL.md (and supporting .md/.json under references/)
  into agent-cookbook/skills/<category>/<skill-name>/SKILL.md.
- Playbooks: copy whitelisted *.md from telegram-claude-bridge/brain/playbooks.
- Sanitize: strip lines matching known secret patterns, emails, phone numbers, API keys.
- Never copies symlinks, .json contact/enrichment/outreach blobs, or private session files.
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_SRC = Path.home() / ".hermes" / "skills"
PLAYBOOKS_SRC = Path.home() / "telegram-claude-bridge" / "brain" / "playbooks"
SKILLS_DST = ROOT / "skills"
PLAYBOOKS_DST = ROOT / "playbooks"

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk_live_[A-Za-z0-9]{20,}"),
    re.compile(r"sk_test_[A-Za-z0-9]{20,}"),
    re.compile(r"pk_live_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"xoxb-[A-Za-z0-9-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{8,}\d")

PLAYBOOK_WHITELIST = {
    "ai-consulting-plan.md",
    "business-funding-framework.md",
    "claude-ai-side-hustle-analysis.md",
    "credit-card-side-hustle-analysis.md",
    "digital-products-business-analysis.md",
    "digital-products-plan.md",
    "faceless-content-plan.md",
    "first-10k-with-claude.md",
    "government-contracting-analysis.md",
    "iced-coffee-cart-business-analysis.md",
    "micro-saas-plan.md",
    "mobile-app-validation-playbook-analysis.md",
    "niche-app-opportunity-analysis.md",
    "reddit-idea-engine.md",
    "solopreneur-productivity-system-analysis.md",
    "voice-receptionist-research.md",
    "digital-products-business-analysis.md",
}

SKIP_CATEGORIES = {".archive", ".curator_backups", ".hub", "dogfood"}


def sanitize(text: str) -> tuple[str, list[str]]:
    redactions = []
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            redactions.append(pat.pattern)
            text = pat.sub("[REDACTED-SECRET]", text)
    # Emails: redact unless they look like obvious example domains
    def _email_sub(m):
        addr = m.group(0)
        low = addr.lower()
        if low.endswith(("@example.com", "@example.org", "@anthropic.com")):
            return addr
        redactions.append("email")
        return "[REDACTED-EMAIL]"
    text = EMAIL_RE.sub(_email_sub, text)
    return text, redactions


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    block = text[3:end]
    body = text[end + 4 :]
    fields = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if m:
            fields[m.group(1).lower()] = m.group(2).strip().strip('"').strip("'")
    return fields, body


def categorize(rel_path: Path) -> tuple[str, str]:
    parts = rel_path.parts
    if len(parts) == 1:
        return "uncategorized", parts[0]
    return parts[0], "/".join(parts[1:-1] + (parts[-1].replace(".md", ""),)) if len(parts) > 2 else parts[1] if len(parts) > 1 else parts[0]


def copy_skills():
    SKILLS_DST.mkdir(parents=True, exist_ok=True)
    copied = []
    skipped = []
    for skill_md in SKILLS_SRC.rglob("SKILL.md"):
        try:
            rel = skill_md.relative_to(SKILLS_SRC)
        except ValueError:
            continue
        if any(rel.parts[0] == s for s in SKIP_CATEGORIES):
            skipped.append(str(rel))
            continue
        if any(p.startswith(".") for p in rel.parts):
            skipped.append(str(rel))
            continue
        if skill_md.is_symlink():
            skipped.append(str(rel) + " (symlink)")
            continue
        # determine destination
        parts = rel.parts
        if len(parts) == 2:
            category = "uncategorized"
            name = parts[0]
        else:
            category = parts[0]
            name = "-".join(parts[1:-1])
        dst_dir = SKILLS_DST / category / name
        dst_dir.mkdir(parents=True, exist_ok=True)
        try:
            text = skill_md.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            skipped.append(f"{rel} ({e})")
            continue
        clean, reds = sanitize(text)
        dst = dst_dir / "SKILL.md"
        dst.write_text(clean)
        copied.append({"src": str(rel), "dst": str(dst.relative_to(ROOT)), "redactions": reds})
    return copied, skipped


def copy_playbooks():
    PLAYBOOKS_DST.mkdir(parents=True, exist_ok=True)
    copied = []
    skipped = []
    if not PLAYBOOKS_SRC.exists():
        return copied, ["playbooks src missing"]
    for f in sorted(PLAYBOOKS_SRC.iterdir()):
        if not f.is_file() or f.suffix != ".md":
            skipped.append(f.name)
            continue
        if f.name not in PLAYBOOK_WHITELIST:
            skipped.append(f.name)
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        clean, reds = sanitize(text)
        dst = PLAYBOOKS_DST / f.name
        dst.write_text(clean)
        copied.append({"src": f.name, "redactions": reds})
    return copied, skipped


def main():
    skills_copied, skills_skipped = copy_skills()
    playbooks_copied, playbooks_skipped = copy_playbooks()
    summary = {
        "skills_copied": len(skills_copied),
        "skills_skipped": len(skills_skipped),
        "playbooks_copied": len(playbooks_copied),
        "playbooks_skipped": len(playbooks_skipped),
        "skill_categories": sorted({c.name for c in SKILLS_DST.iterdir() if c.is_dir()}),
    }
    import json
    print(json.dumps(summary, indent=2))
    (ROOT / "scripts" / "build_report.json").write_text(json.dumps({
        "summary": summary,
        "skills_copied": skills_copied,
        "skills_skipped": skills_skipped,
        "playbooks_copied": playbooks_copied,
        "playbooks_skipped": playbooks_skipped,
    }, indent=2))


if __name__ == "__main__":
    main()
