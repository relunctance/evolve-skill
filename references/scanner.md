# scanner.py 详细规格

## 接口

```bash
python3 scripts/scanner.py [scan_path] [...scan_path]
```

- 无参数：扫描 `~/.hermes/skills` + `/home/gql/repos`
- 1+ 参数：扫描每个指定路径

## 输出

`/tmp/evolve-scan.json` 格式：

```json
{
  "skills": [
    {
      "name": "arch-diagram-skill",
      "learns_dir": "/home/gql/repos/arch-diagram-skill/learns",
      "problems": [
        {"file": "layout-problems.md", "count": 4, "score": 10.8, "path": "..."}
      ],
      "total_count": 7,
      "total_score": 17.4,
      "change_magnitude": 20.88
    }
  ],
  "scan_time": "2026-06-07T14:32:02Z"
}
```

## 评分公式

- `total_score = Σ(problem.score)` 其中 `problem.score = severity_weight × category_weight`
- `change_magnitude = total_score × 1.2`
  - `≤ 5` → 批量升级模式
  - `> 5` → 项目升级模式

## BDD 注释（scanner.py 顶部）

```
BDD: "### [P2] xxx" → score 2.4 (P2*layout); "- [P2] xxx" → same
TDD: scan_skill(Path) returns None if no learns/; returns dict with total_score
```
