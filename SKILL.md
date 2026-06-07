---
name: evolve-skill
description: skill 体系的 meta-level 自我进化引擎 — 扫描所有 skills 的 learns/，按评分排序触发升级
triggers:
  - 扫描 skills 进化
  - skill 自动升级
  - 自我进化
  - evolution skill
  - evolve skill
category: development
author: relunctance
created: 2026-06-10
updated: 2026-06-10
tags:
  - skill
  - evolution
  - self-improvement
  - meta-level
---

# evolve-skill

> skill 体系的 meta-level 自我进化引擎。
>
> 核心价值：跨 skill 统一进化入口，skill 运行后自动反思沉淀，无需人工干预。

## 触发条件

当需要以下操作时使用：
- 扫描所有 skills 的 learns/ 积累问题
- 按评分排序触发升级
- 批量或项目级别的 skill 升级

## 核心流程

```
skill 运行 → reflection_hook → LLM 反思沉淀 → evolve-skill 扫描
→ 评分排序 → 双模式升级 → pytest + commit + 通知
```

详细流程见下方 Step 0-4。

---

## Step 0：扫描 + 打分排序

运行 scanner.py 扫描所有 skill 的 learns/：

```bash
python3 scripts/scanner.py
```

输出 JSON，按 `total_score` 降序排列。

---

## Step 1：生成进化报告

LLM 读取 Top N 问题内容，生成：
- 问题分类汇总（LAYOUT / VISUAL / FUNCTIONAL / UX / PERFORMANCE）
- 优先级排序（按分数高低）
- 每个 skill 的 `change_magnitude`

---

## Step 2：分支判断（双模式）

判断 `change_magnitude = total_score × 1.2`：

| change_magnitude | 阈值 | 模式 |
|-----------------|------|------|
| ≤ 5 | 保守阈值 | 批量升级模式 |
| > 5 | - | 项目升级模式 |

**用户指定 skill → 项目升级模式（精细确认）**

---

## Step 3：执行升级

**A. skill 缺少 learns/ scaffold**
```
skill-created --upgrade <target-skill>
→ 注入 learns/ + scripts/feedback.py + scripts/reflection_hook.py
```

**B. skill 有 learns/ 但问题 ≥ 阈值**
```
darwin-skill(target_skill="xxx", learns_dir="/path/to/learns")
```

---

## Step 4：验证 + commit

- 运行 pytest（如果存在）
- 成功 → 自动 commit + push + 通知

---

## references/ 索引

| 文件 | 内容 |
|------|------|
| references/scanner.md | scanner.py 详细规格 |
| references/severity.md | 严重程度体系（P0-P3 + auto-severity） |
| references/dual-mode.md | 双模式架构（批量 vs 项目） |
| references/reflection-hook.md | 反射机制说明 |
