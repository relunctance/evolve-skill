---
search: false
---

<div align="center">

# 🌱 evolve-skill

**[English](README.md) · [中文](README_zh.md)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![version](https://img.shields.io/badge/version-1.0.0-green.svg)](#)
[![platforms](https://img.shields.io/badge/platforms-Hermes%20Agent-4B8FBA.svg)](#)
[![category](https://img.shields.io/badge/category-development-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org/)

*skill 体系的 meta-level 自我进化引擎*

</div>

> 扫描 `learns/` 目录，对问题评分，触发双模式升级。

## 核心能力

```
skill 运行 → reflection_hook → LLM 反思沉淀 → evolve-skill 扫描
→ 评分排序 → 双模式升级 → pytest + commit + 通知
```

## 核心特性

- **自动反思**：skill 运行后自动将经验沉淀到 `learns/`
- **评分体系**：P0-P3 严重程度 × 分类权重 = 问题分数
- **双模式升级**：批量模式（小改动）vs 项目模式（重大变更）
- **零依赖**：纯 Python 标准库，无外部包

## 快速开始

### 扫描所有 skills

```bash
python3 scripts/scanner.py
```

输出：`/tmp/evolve-scan.json`

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

### 运行 evolve-skill

```bash
hermes skills run evolve-skill
```

## 评分体系

### 严重程度标签

| 标签 | 权重 | 说明 |
|------|------|------|
| P0 | 4 | 关键 — 功能完全失效 |
| P1 | 3 | 主要 — 功能受影响 |
| P2 | 2 | 中等 — 体验较差 |
| P3 | 1 | 轻微 — 改进建议 |

### 分类权重

| 分类 | 权重 |
|------|------|
| functional | 2.0 |
| performance | 1.5 |
| layout | 1.2 |
| visual | 1.1 |
| ux | 1.0 |

### 问题格式

learns `{category}-problems.md` 采用**双层结构**：

```markdown
### [P2] 节点宽度不一致导致布局错位

<!-- 问题 #1 -->
## 2026-06-10 问题 #1

**DQS**: 52.0 (D1=60 D2=40 D3=55 D4=50 D5=55 D6=52)
**来源**: input.md

> 节点宽度不一致导致连接线错位

---
```

- `### [P2] ...` → scanner 提取计分
- `<!-- 问题 #N -->` 块 → 人类可读完整记录

## 双模式升级

| 模式 | 触发条件 | 用户交互 |
|------|---------|---------|
| 批量模式 | `change_magnitude ≤ 5` | 单次概要确认 |
| 项目模式 | `change_magnitude > 5` | 逐个精细确认 |

## 文件结构

```
evolve-skill/
├── SKILL.md                      # 主入口（SOP + prompt 模板）
├── README.md                     # English
├── README_zh.md                 # 本文件（顶部引用 README.md）
├── scripts/
│   └── scanner.py               # 扫描脚本（~150 行，纯 Python 标准库）
└── learns/                      # （未来：自我进化追踪）
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/relunctance/evolve-skill.git
cd evolve-skill

# 直接运行 scanner
python3 scripts/scanner.py
```

**依赖**：Python 3.8+（仅使用标准库，无需安装外部包）

## 安装后验证

- [ ] Python 3.8+ 已安装（`python3 --version`）
- [ ] 克隆成功（`ls -la README.md`）
- [ ] scanner 可运行（`python3 scripts/scanner.py`）
- [ ] JSON 输出生成（`cat /tmp/evolve-scan.json`）

## 相关 Skills

| Skill | 关系 | 为什么相关 |
|-------|------|----------|
| [skill-created](https://github.com/relunctance/skill-created) | 创建带 `learns/` scaffold 的新 skill | 为 `evolve-skill` 提供可扫描的 scaffold 结构 |
| [darwin-skill](https://github.com/relunctance/darwin-skill) | 执行实际代码进化 | 执行 `evolve-skill` 触发的升级工作 |
| arch-diagram-skill | 参考实现（私有仓库） | 展示端到端问题沉淀工作流 |

## 欢迎贡献

欢迎提交 Issue 和 PR！

### 发现问题

在对应 skill 的 `learns/` 目录创建 `{category}-problems.md`：

```markdown
### [P2] 你的问题描述

<!-- 问题 #1 -->
## 2026-06-10 问题 #1

**DQS**: 55.0 (D1=60 D2=50 D3=55 D4=55 D5=55 D6=55)
**来源**: 你的输入文件.md

> 详细问题描述

---
```

### 贡献代码

1. Fork 本仓库
2. 创建 feature 分支（`git checkout -b feature/your-feature`）
3. 提交更改
4. 运行测试（`pytest tests/`）
5. 提交 PR 并关联 Issue

## 许可证

MIT License
