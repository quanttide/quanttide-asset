# quanttide-asset

量潮数字资产管理

## 概述

量潮数字资产管理（quanttide-asset）是量潮知识管理体系中的**数字资产管理**领域，以契约承载数字资产的登记、组织与浏览——资产长什么样，页面就长什么样。

## 领域边界

- **资产契约**：`.quanttide/asset/contract.yaml` 定义资产组成、路径与类型，实际结构必须与契约一致
- **资产组织**：data/ 陈述性记忆（context/insight/intention/journal/profile/report/roadmap）+ docs/ 程序性记忆（bylaw/essay/gallery/handbook/specification/tutorial）
- **资产浏览**：结构即界面——契约驱动的目录镜像（参照 qtfounder studio asset 页模式）
- **资产使用**：skill 执行、契约验证与 diff

## 子模块

### apps/ — 应用

- `qtcloud-asset` — 数字资产云：CLI + Provider + Studio

### data/ — 陈述性记忆

- `context` — 语境
- `insight` — 洞察
- `intention` — 意图
- `journal` — 日志
- `profile` — 档案
- `report` — 报告
- `roadmap` — 路线图

### docs/ — 程序性记忆

- `bylaw` — 章程
- `essay` — 随笔
- `gallery` — 案例
- `handbook` — 手册
- `specification` — 标准
- `tutorial` — 教程

### examples/ — 实验室

- `default` — 实验室入口（实验性/原型项目）

### packages/ — 工具包

- `quanttide-asset-toolkit` — 资产管理工具包

## 许可

[CC BY 4.0](LICENSE)
