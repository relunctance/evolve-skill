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

## 异常处理表

| 异常 | 检测方式 | 处理方式 |
|------|----------|----------|
| **scanner 路径不存在** | `python3 scripts/scanner.py /no/such/path` 返回 `skills: []` | 提示"路径无效"，不报错 |
| **learns/ 缺失** | scanner 跳过该 skill | 不计入待升级列表 |
| **JSON 解析失败** | scanner 内 try/except 兜底 | 记录到 stderr，不中断扫描 |
| **scanner 超时** | > 30s 仍在运行 | Ctrl+C + 检查 IO 性能（learns/ 太大）|
| **无 [Px] 标签** | 扫描结果 total_score=0 | 用 `grep -rE '\[P[0-3]\]' <learns_dir>` 验证 |
| **change_magnitude 卡在 0** | 公式 `total_score × 1.2` | 检查所有问题是否缺分类标签 |

### 自检脚本

```bash
# 验证 scanner 输出
python3 scripts/scanner.py /home/gql/repos
[ -f /tmp/evolve-scan.json ] && echo "✅ scanner OK" || echo "❌ scanner failed"
python3 -c "import json; d=json.load(open('/tmp/evolve-scan.json')); print(f'Scanned {len(d[\"skills\"])} skills')"
```

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

## 危险信号表

🔴 **以下症状出现时，立即停止并诊断**：

| 危险信号 | 症状 | 根因 | 正确做法 |
|----------|------|------|----------|
| scanner 空输出 | `skills: []` | 路径无 learns/ 目录 | 确认路径正确 + 含 `learns/` 子目录 |
| scanner 失败退出 | Python traceback | JSON 解析错/路径权限 | 单独跑 scanner.py 调试 |
| change_magnitude=0 | total_score=0 | 所有问题无 [Px] 标签 | 用 `grep -E '### \\[P[0-3]\\]'` 检查 learns/ |
| 修复后分数不变 | Px 仍被计分 | 未去掉 [Px] 标记 | 删整行或用 `~~### [P2] xxx~~` 删除线 |
| 升级失败 pytest | 测试红 | 改动破坏了已有功能 | 立即回滚，不继续提交 |
| 误判大批量 | scanner 把无 learns/ 也算 | 路径未过滤 | 手动加 `os.listdir(learns_dir)` 守卫 |

## 禁止行为

- ❌ 不要跳过 `change_magnitude` 阈值判断（>5 必须项目模式）
- ❌ 不要直接 `rm` learns/ 文件（scanner 会重扫到，丢失历史）
- ❌ 不要把已修复问题直接改 [P0]（会触发"误判大批量"）
- ❌ 不要在未跑 pytest 前 commit

## references/ 索引

| 文件 | 内容 |
|------|------|
| references/scanner.md | scanner.py 详细规格 |
| references/severity.md | 严重程度体系（P0-P3 + auto-severity） |
| references/dual-mode.md | 双模式架构（批量 vs 项目） |
| references/reflection-hook.md | 反射机制说明 |
