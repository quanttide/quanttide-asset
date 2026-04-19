---
name: docs-validate
description: 验证 Markdown/Myst 文档能否正常编译。
---

# 文档验证技能

验证 Myst 文档（MyST 格式）能否正常编译。

## 使用场景

- 创建或修改 docs/specification/ 下的文档后
- 修改 myst.yml 配置后

## 验证流程

### 1. 安装检查

```bash
which myst || pip show mystmd
```

### 2. 编译文档

```bash
cd docs/specification
myst build --site
```

### 3. 检查结果

- 无警告/错误输出
- `content/` 目录有 `.json` 文件

## 常见问题

### myst.yml 配置错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `'name' unexpected comma` | authors 格式错误 | 改为 `name: 名称` |
| `'file' expected an entry` | toc 配置错误 | 确认每个条目有 `file` 或 `title` |
| `No given name` | authors 缺少 given | 使用 `name: xxx` 格式 |

### 正确配置示例

```yaml
project:
  title: 项目标题
  authors:
    - name: QuantTide
  toc:
    - file: index.md
    - title: 章节名
      children:
        - file: path/to/file.md
```

### 编译命令

| 命令 | 用途 |
|------|------|
| `--site` | 编译静态站（生产用）|
| `--html` | 编译 HTML（有服务器）|
| `--pdf` | 编译 PDF |

## 验证要点

- myst.yml 无警告/错误
- `toc` 中每个 `file` 对应的源文件存在
- `_build/site/content/` 有 `.json` 文件