# 资产发现程序设计

## 概述

本程序实现以指定目录为目标的数字资产发现功能，遵循量潮科技资产发现规范。

## 设计目标

扫描指定目录，识别数字资产并生成清单。无契约时直接发现文件系统资产，有契约时进行对比验证。

## 核心功能

### 1. 目录扫描

作为目标入口：

```python
def scan(target_path: str) -> list[Asset]:
    """扫描指定目录，发现数字资产"""
```

### 2. 资产类型识别

根据文件扩展名和目录结构自动识别：

| 类型 | 标识 | 示例 |
|------|------|------|
| 文档 | docs | `.md`, `.txt`, `.pdf` |
| 代码 | code | `.py`, `.js`, `.ts` |
| 配置 | config | `.yaml`, `.json`, `.toml` |
| 数据 | data | `.csv`, `.json`, `.sqlite` |

### 3. 契约加载策略

```
扫描目标目录
    │
    ▼
检查 .quanttide/asset/contract.yaml 是否存在
    │
    ├── 存在 → 加载契约，对比验证
    │
    └── 不存在 → 仅文件系统发现
```

参考 `.quanttide/asset/contract.yaml` 结构：

```yaml
assets:
  brd:
    title: 商业需求文档
    type: docs
    category: brd
    path: docs/brd
```

契约验证模式：
- 标记新增资产（未在契约中定义）
- 标记缺失资产（契约中定义但不存在）
- 标记变更资产（内容或元数据已修改）

## 使用方式

```bash
# 发现当前目录资产
python -m app.discovery .

# 发现指定目录资产
python -m app.discovery /path/to/target
```

## 资产事件

| 事件 | 描述 |
|------|------|
| `asset.discovered` | 发现新资产 |
| `asset.missing` | 契约中定义但目录缺失 |
| `asset.modified` | 资产内容变更 |
