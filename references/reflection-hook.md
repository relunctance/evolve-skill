# 反射机制说明

## 流程

```
skill 运行 → reflection_hook → LLM 反思沉淀 → evolve-skill 扫描
```

## reflection_hook 位置

在目标 skill 的 `scripts/reflection_hook.py` 中（由 `skill-created --upgrade` 注入）。

## LLM 反思沉淀格式

写入目标 skill 的 `learns/{category}-problems.md`：

```markdown
### [P2] 问题简短描述

<!-- Problem #1 -->
## 2026-06-07 Problem #1

**DQS**: 52.0 (D1=60 D2=40 D3=55 D4=50 D5=55 D6=52)
**Source**: input.md

> 详细问题描述

---
```

## 双层结构说明

- `### [P2] xxx` → scanner 提取计分
- `<!-- Problem #N -->` 块 → 人类可读完整记录
