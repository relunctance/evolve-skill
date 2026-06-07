---
search: false
---

<div align="center">

# 🌱 evolve-skill

**[English](README.md) · [中文](README_zh.md)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![version](https://img.shields.io/badge/version-1.0.0-green.svg)](#)
[![platforms](https://img.shields.io/badge/platforms-Hermes%20Agent%20%7C%20Claude%20Code%20%7C%20OpenClaw-4B8FBA.svg)](#)
[![category](https://img.shields.io/badge/category-development-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org/)

*Self-evolution engine for the skill ecosystem — scans `learns/` directories, scores problems, triggers upgrades via dual-mode system*

</div>

## 🎯 Triggers

Use evolve-skill when you need to:
- Scan all skills' `learns/` accumulated problems
- Score and sort problems to trigger targeted upgrades
- Batch or project-level skill upgrades

## ✨ Features

- **Automatic reflection**: skill runs automatically precipitate experiences to `learns/`
- **Scoring system**: P0-P3 severity × category weight = problem score
- **Dual-mode upgrade**: batch mode (small changes) vs project mode (major changes)
- **Zero dependencies**: pure Python stdlib, no external packages required

## 🚀 Quick Start

### Scan all skills

```bash
python3 scripts/scanner.py
```

Output: `/tmp/evolve-scan.json`

```json
{
  "skills": [
    {
      "name": "arch-diagram-skill",
      "total_score": 11.4,
      "change_magnitude": 13.68,
      "problems": [
        {"file": "layout-problems.md", "count": 2, "score": 4.8}
      ]
    }
  ],
  "scan_time": "2026-06-10T12:00:00Z"
}
```

### Run evolve-skill

```bash
hermes skills run evolve-skill
```

## 📊 Scoring System

### Severity Tags

| Tag | Weight | Description |
|-----|--------|-------------|
| P0 | 4 | Critical — complete failure |
| P1 | 3 | Major — functionality affected |
| P2 | 2 | Moderate — poor experience |
| P3 | 1 | Minor — improvement suggestion |

### Category Weights

| Category | Weight |
|----------|--------|
| functional | 2.0 |
| performance | 1.5 |
| layout | 1.2 |
| visual | 1.1 |
| ux | 1.0 |

### Problem Format

learns `{category}-problems.md` uses a **dual-layer format**:

```markdown
### [P2] Node width inconsistency causes layout misalignment

<!-- Problem #1 -->
## 2026-06-10 Problem #1

**DQS**: 52.0 (D1=60 D2=40 D3=55 D4=50 D5=55 D6=52)
**Source**: input.md

> Node width inconsistency causes connection line misalignment

---
```

- `### [P2] ...` → scanner extracts for scoring
- `<!-- Problem #N -->` block → human-readable full record

## 🔄 Dual-Mode Upgrade

| Mode | Trigger | User Interaction |
|------|---------|-----------------|
| Batch mode | `change_magnitude ≤ 5` | Single summary confirmation |
| Project mode | `change_magnitude > 5` | Per-skill detailed confirmation |

## 📁 File Structure

```
evolve-skill/
├── SKILL.md                      # Main entry (SOP + prompt templates)
├── README.md                     # English documentation
├── README_zh.md                  # Chinese documentation (top references README.md)
├── scripts/
│   └── scanner.py               # Scan script (~150 lines, Python stdlib)
└── learns/                      # Self-improvement tracking archive
```

## 📦 Installation

```bash
# Hermes / OpenClaw
hermes skills install https://github.com/relunctance/evolve-skill

# Or clone directly
git clone https://github.com/relunctance/evolve-skill.git
cd evolve-skill
python3 scripts/scanner.py
```

**Dependencies**: Python 3.8+ (standard library only — no external packages required)

## ✅ Installation Verification

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Clone successful (`ls -la README.md`)
- [ ] Scanner runs (`python3 scripts/scanner.py`)
- [ ] JSON output generated (`cat /tmp/evolve-scan.json`)

## 🔗 Related Skills

| Skill | Relationship | Why Related |
|-------|-------------|-------------|
| [skill-created](https://github.com/relunctance/skill-created) | Creates new skills with `learns/` scaffold | Provides the scaffold structure that `evolve-skill` scans to discover improvement opportunities |
| [darwin-skill](https://github.com/alchaincyf/darwin-skill) | Executes actual code evolution | Performs the upgrade work that `evolve-skill` triggers based on scored problems |
| [readme-skill](https://github.com/relunctance/readme-skill) | README beautification | A skill that `evolve-skill` can scan and trigger improvements for its own documentation |
| arch-diagram-skill | Reference implementation (private) | Demonstrates the end-to-end problem-settling workflow using `learns/` |

## 🤝 Contributing

Contributions, issues and pull requests are welcome!

**Found a bug or want to improve a skill?**
1. Submit an [Issue](https://github.com/relunctance/evolve-skill/issues)
2. Describe reproduction steps
3. Attach error logs

**Want to contribute code?**
1. Fork this repository
2. Create a Feature branch (`git checkout -b feature/AmazingFeature`)
3. Write BDD comments + TDD tests
4. Commit changes (`git commit -m 'Add AmazingFeature'`)
5. Push to branch (`git push origin feature/AmazingFeature`)
6. Create a Pull Request

**Adding a problem to scan?**
In the target skill's `learns/` directory, create or edit `{category}-problems.md`:

```markdown
### [P2] Your problem description here

<!-- Problem #1 -->
## 2026-06-10 Problem #1

**DQS**: 55.0 (D1=60 D2=50 D3=55 D4=55 D5=55 D6=55)
**Source**: your-input.md

> Detailed problem description

---
```

## 📜 License

MIT — see [LICENSE](LICENSE)
