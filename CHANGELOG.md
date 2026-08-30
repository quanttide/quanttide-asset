# CHANGELOG

## [Unreleased]

### Added
- 新增公开平台资产契约章程 (bylaw/contract/public-platform.md)：云存储桶等基础设施资产的分类、生命周期与治理规范

### Changed
- 重写 README：补全领域定义（概述、领域边界、子模块结构、许可 CC BY 4.0）
- 更新 specification 子模块至 v0.1.0：新增 type 字段，重命名 assets 为 schemas，移除 content 字段 (**breaking**)
- 更新 bylaw 子模块至 v0.3.0：新增公开平台资产契约章程，第二大脑章程重构为双轴组织与 20 类资产命名规范

## [v0.1.3] - 2026-05-15

### Changed
- 更新 handbook 子模块至 v0.1.1：调整陈述型记忆九宫格，新增 Archive 工作归档
- 更新 gallery 子模块：移除重复的分类和类型文件

## [v0.1.2] - 2026-04-27

### Added
- 添加资产契约 (asset/contract.yaml)

## [v0.1.1] - 2026-04-21

### Added
- 添加数字资产工具箱 (toolkit) 子模块

### Removed
- 移除第二大脑示例 (second-brain)

## [v0.1.0] - 2025-04-21

### Added
- 添加第二大脑资产管理系统
- 添加工作章程 (bylaw) 子模块 v0.2.0：组织治理纲领
- 添加工作案例 (gallery) 子模块 v0.1.0：资产类别和类型定义
- 添加上下文 (context) 子模块：默认上下文文档
- 添加飞书知识库资产发现流程

### Changed
- 重新梳理章程和案例边界，章程聚焦治理纲领

## [0.0.3] - 2026-04-19

### Added
- 飞书知识库下载示例 (examples/feishu-wiki)
- 文档验证技能 (docs-validate)

### Changed
- 更新规范子模块到 v0.0.2
- 更新上下文子模块
- 优化文档验证 SKILL

## [0.0.2] - 2026-04-17

### Added
- 发布 specification 子模块 v0.0.1
- 添加 MyST 构建输出忽略规则

## [0.0.1] - 2026-04-17

### Added
- 初始版本：引入四个文档子模块
  - bylaw: 工作章程
  - handbook: 工作手册
  - context: 上下文文档
  - tutorial: 教程文档