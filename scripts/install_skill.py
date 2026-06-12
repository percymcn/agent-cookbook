#!/usr/bin/env python3
"""Install skills from agent-cookbook into a target skill directory.

Usage:
    python3 scripts/install_skill.py --list
    python3 scripts/install_skill.py --skill domain --dry-run
    python3 scripts/install_skill.py --skill domain
    python3 scripts/install_skill.py --category trading
    python3 scripts/install_skill.py --skill domain --target /path/to/skills --force
"""
import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DEFAULT_TARGET = Path.home() / ".hermes" / "skills"


def resolve_safe(base: Path, name: str) -> Path:
    """Resolve a path under base, preventing traversal outside it."""
    resolved = (base / name).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        print(f"ERROR: path traversal detected: {name!r}")
        sys.exit(1)
    return resolved


def find_skills() -> dict[str, list[dict]]:
    """Return {category: [{name, path, has_skill_md}]} from repo skills/."""
    cats: dict[str, list[dict]] = {}
    if not SKILLS_DIR.is_dir():
        return cats
    for cat_dir in sorted(SKILLS_DIR.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        entries = []
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            entries.append({
                "name": skill_dir.name,
                "path": skill_dir,
                "has_skill_md": (skill_dir / "SKILL.md").exists(),
            })
        if entries:
            cats[cat_dir.name] = entries
    return cats


def find_skill_by_name(name: str, catalog: dict) -> Path | None:
    """Find a skill by name across all categories."""
    for cat, skills in catalog.items():
        for s in skills:
            if s["name"] == name:
                return s["path"]
    return None


def list_skills(catalog: dict):
    total = 0
    for cat in sorted(catalog):
        skills = catalog[cat]
        print(f"\n  {cat}/ ({len(skills)} skills)")
        for s in skills:
            marker = "+" if s["has_skill_md"] else "-"
            print(f"    [{marker}] {s['name']}")
            total += 1
    print(f"\nTotal: {total} skills in {len(catalog)} categories")
    print("  [+] has SKILL.md    [-] missing SKILL.md")


def install_skill(src: Path, target_base: Path, name: str, *, dry_run: bool, force: bool):
    dst = resolve_safe(target_base, name)

    if dst.exists():
        if dry_run:
            print(f"  EXISTS  {dst}")
            print(f"  WOULD backup to {dst}.bak-*")
            print(f"  WOULD copy {src} -> {dst}")
            return True

        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = dst.parent / f"{dst.name}.bak-{ts}"
        print(f"  BACKUP  {dst} -> {backup}")
        shutil.copytree(dst, backup)
        shutil.rmtree(dst)
    elif dry_run:
        print(f"  WOULD copy {src} -> {dst}")
        return True

    shutil.copytree(src, dst)
    print(f"  INSTALLED  {src.name} -> {dst}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Install skills from agent-cookbook")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--skill", help="Install a single skill by name")
    group.add_argument("--category", help="Install all skills in a category")
    group.add_argument("--list", action="store_true", help="List available skills")
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET,
                        help=f"Target skill directory (default: {DEFAULT_TARGET})")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without copying")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite without backup (default: backup + copy)")

    args = parser.parse_args()
    catalog = find_skills()

    if not catalog:
        print(f"ERROR: no skills found in {SKILLS_DIR}")
        sys.exit(1)

    if args.list:
        print("Available skills:")
        list_skills(catalog)
        sys.exit(0)

    if not args.skill and not args.category:
        parser.print_help()
        sys.exit(1)

    target = args.target.resolve()
    # Prevent traversal in target
    if ".." in str(args.target):
        print("ERROR: target path must not contain '..'")
        sys.exit(1)

    target.mkdir(parents=True, exist_ok=True)

    if args.skill:
        src = find_skill_by_name(args.skill, catalog)
        if not src:
            print(f"ERROR: skill {args.skill!r} not found. Use --list to see available skills.")
            sys.exit(1)
        mode = "DRY RUN" if args.dry_run else "INSTALL"
        print(f"\n[{mode}] Skill: {args.skill} -> {target}")
        ok = install_skill(src, target, args.skill, dry_run=args.dry_run, force=args.force)
        if ok and not args.dry_run:
            print(f"\nDone. Skill installed to {target / args.skill}")
        elif ok:
            print("\nDry run complete. No files changed.")

    elif args.category:
        if args.category not in catalog:
            print(f"ERROR: category {args.category!r} not found. Use --list to see categories.")
            sys.exit(1)
        skills = catalog[args.category]
        mode = "DRY RUN" if args.dry_run else "INSTALL"
        print(f"\n[{mode}] Category: {args.category} ({len(skills)} skills) -> {target}")
        installed = 0
        for s in skills:
            ok = install_skill(s["path"], target, s["name"], dry_run=args.dry_run, force=args.force)
            if ok:
                installed += 1
        if not args.dry_run:
            print(f"\nDone. {installed}/{len(skills)} skills installed to {target}")
        else:
            print(f"\nDry run complete. {installed} skills would be installed.")


if __name__ == "__main__":
    main()
