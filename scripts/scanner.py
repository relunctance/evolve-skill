#!/usr/bin/env python3
"""scanner.py - Scan learns/*-problems.md across all skills, output scored JSON."""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# BDD: "### [P2] xxx" → score 2.4 (P2*layout); "- [P2] xxx" → same
# TDD: scan_skill(Path) returns None if no learns/; returns dict with total_score

SEVERITY_WEIGHT = {"P0": 4, "P1": 3, "P2": 2, "P3": 1}
CATEGORY_WEIGHT = {
    "functional": 2.0,
    "performance": 1.5,
    "layout": 1.2,
    "visual": 1.1,
    "ux": 1.0,
    "other": 1.0,
}


def get_severity(line: str) -> str:
    """Extract [Px] tag. BDD: "### [P2] xxx" → "P2\""""
    m = re.search(r'\[P([0-3])\]', line)
    return f"P{m.group(1)}" if m else "P3"


def get_category(fname: str) -> str:
    """Infer category from filename. BDD: "layout-problems.md" → "layout\""""
    name = os.path.basename(fname).replace("-problems.md", "").lower()
    return name if name in CATEGORY_WEIGHT else "other"


def calc_score(severity: str, category: str) -> float:
    """Compute score. BDD: P2 + layout → 2 * 1.2 = 2.4"""
    return SEVERITY_WEIGHT.get(severity, 1) * CATEGORY_WEIGHT.get(category, 1.0)


def is_problem_line(line: str) -> bool:
    """Check if line is a problem line (### [Px] or - [Px] at line start)."""
    stripped = line.lstrip()
    return bool(
        stripped.startswith("### [P")
        or stripped.startswith("- [P")
        or re.match(r'^\s*\[P[0-3]\]', line)
    )


def scan_skill(skill_dir: Path) -> dict | None:
    """Scan a single skill's learns/ directory."""
    learns_dir = skill_dir / "learns"
    if not learns_dir.is_dir():
        return None

    problems = []
    total_score = 0.0

    try:
        entries = os.listdir(learns_dir)
    except Exception:
        return None

    for fname in sorted(entries):
        if not fname.endswith("-problems.md"):
            continue
        prob_file = learns_dir / fname
        if not prob_file.is_file():
            continue

        category = get_category(fname)
        prob_score = 0.0
        count = 0

        try:
            text = prob_file.read_text(encoding="utf-8")
            for line in text.splitlines():
                stripped = line.lstrip()
                if not (
                    stripped.startswith("### [P")
                    or stripped.startswith("- [P")
                    or re.match(r'^\s*\[P[0-3]\]', line)
                ):
                    continue
                severity = get_severity(line)
                score = calc_score(severity, category)
                prob_score += score
                count += 1
        except Exception:
            pass

        if count > 0:
            problems.append({
                "file": fname,
                "count": count,
                "score": round(prob_score, 2),
                "path": str(prob_file),
            })
            total_score += prob_score

    if not problems:
        return None

    return {
        "name": skill_dir.name,
        "learns_dir": str(learns_dir),
        "problems": problems,
        "total_count": sum(p["count"] for p in problems),
        "total_score": round(total_score, 2),
        "change_magnitude": round(total_score * 1.2, 2),
    }


def main():
    output_file = "/tmp/evolve-scan.json"
    scan_dirs = [
        Path(os.path.expanduser("~/.hermes/skills")),
        Path("/home/gql/repos"),
    ]

    skills = []
    for base_dir in scan_dirs:
        if not base_dir.is_dir():
            continue
        try:
            for skill_dir in base_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "learns").is_dir():
                    result = scan_skill(skill_dir)
                    if result:
                        skills.append(result)
        except Exception:
            pass

    skills.sort(key=lambda x: x["total_score"], reverse=True)

    output = {
        "skills": skills,
        "scan_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(output_file)


if __name__ == "__main__":
    main()
