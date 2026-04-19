---
name: docs-validate
description: 验证文档能否正常编译或渲染。
---

# 文档验证技能

验证各类文档能否正常编译或渲染。

## 子模块列表

| 子模块 | 文档格式 | 验证命令 |
|--------|---------|----------|
| docs/specification | MyST | `myst build --site` |
| docs/bylaw | - | - |
| docs/handbook | - | - |
| docs/report | - | - |
| docs/context | - | - |
| docs/tutorial | - | - |

## 验证流程

### specification 子模块

```bash
cd docs/specification
myst build --site
```

验证成功标准：
- 无警告/错误
- `_build/site/content/` 有 `.json` 文件

### 通用检查

1. **文件存在**：检查引用的文件是否存在
2. **链接有效**：内部链接是否能访问
3. **语法正确**：Markdown/MyST 语法

## 常见问题

### specification 编译错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `'name' unexpected comma` | authors 格式 | 改为 `name: 名称` |
| `'file' expected` | toc 配置 | 确认有 file 或 title |
| `No given name` | authors 缺少 | 使用 `name: xxx` |

### 正确 myst.yml

```yaml
project:
  title: 标题
  authors:
    - name: QuantTide
  toc:
    - file: index.md
    - title: 章节
      children:
        - file: path/to.md
```

## 验证要点

- 确认使用对应的子模块路径
- 检查相应的配置文件
- 验证编译输出