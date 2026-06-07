---
search: false
---

# evolve-skill

**[English](README.md) · [中文](README_zh.md)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![version](https://img.shields.io/badge/version-1.0.0-green.svg)](#)
[![platforms](https://img.shields.io/badge/platforms-Hermes%20Agent-4B8FBA.svg)](#)
[![category](https://img.shields.io/badge/category-development-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org/)

> Self-evolution engine for the skill ecosystem — scans `learns/` directories, scores problems, triggers upgrades via dual-mode system.

## What It Does

```
skill runs → reflection_hook → LLM reflection → evolve-skill scan
→ score & sort → dual-mode upgrade → pytest + commit + notify
```

## Features

- **Automatic reflection**: skill runs automatically沉淀 experiences to `learns/`
- **Scoring system**: P0-P3 severity × category weight = problem score
- **Dual-mode upgrade**: batch mode (small changes) vs project mode (major changes)
- **Zero dependencies**: pure Python stdlib, no external packages

## Quick Start

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

## Scoring System

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

## Dual-Mode Upgrade

| Mode | Trigger | User Interaction |
|------|---------|-----------------|
| Batch mode | `change_magnitude ≤ 5` | Single summary confirmation |
| Project mode | `change_magnitude > 5` | Per-skill detailed confirmation |

## File Structure

```
evolve-skill/
├── SKILL.md                      # Main entry (SOP + prompt templates)
├── README.md                     # This file (English)
├── README_zh.md                 # 中文（top references README.md）
├── scripts/
│   └── scanner.py               # Scan script (~150 lines, Python stdlib)
└── learns/                      # (future: self-improvement tracking)
```

## Installation

```bash
# Clone the repository
git clone https://github.com/relunctance/evolve-skill.git
cd evolve-skill

# Run scanner directly
python3 scripts/scanner.py
```

**Dependencies**: Python 3.8+ (standard library only — no external packages required)

## Installation Verification

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Clone successful (`ls -la README.md`)
- [ ] Scanner runs (`python3 scripts/scanner.py`)
- [ ] JSON output generated (`cat /tmp/evolve-scan.json`)

## Related Skills

| Skill | Relationship | Why Related |
|-------|-------------|-------------|
| [skill-created](https://github.com/relunctance/skill-created) | Creates new skills with `learns/` scaffold | Provides the scaffold that `evolve-skill` scans for improvements |
| [darwin-skill](https://github.com/relunctance/darwin-skill) | Executes actual code evolution | Performs the upgrade work that `evolve-skill` triggers |
| arch-diagram-skill | Reference implementation (private) | Shows the problem-settling workflow end-to-end |

## Contributing

Contributions welcome! Here's how to get involved:

### Report Problems

Create a `{category}-problems.md` file in the target skill's `learns/` directory:

```markdown
### [P2] Your problem description here

<!-- Problem #1 -->
## 2026-06-10 Problem #1

**DQS**: 55.0 (D1=60 D2=50 D3=55 D4=55 D5=55 D6=55)
**Source**: your-input.md

> Detailed problem description

---
```

### Contribute Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Run tests (`pytest tests/`)
5. Submit a Pull Request with a link to the relevant Issue

## License

MIT License
