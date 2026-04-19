# ROADMAP

## 飞书知识库递归下载

### 已完成

- [x] 问题定位：API 用错了，`get_node` 是获取单个节点，`/wiki/v2/spaces/:space_id/nodes` 才是获取子节点列表
- [x] 验证 API 路径：用 curl 直接调用正确的 list API
- [x] 确认权限范围：确认 access_token 包含必要的权限 scope

### 进行中

- [ ] 实现递归下载脚本（Python）
  1. 获取 tenant_access_token
  2. 获取所有知识库的 space_id 和根节点
  3. 递归调用 `list` 接口获取子节点
  4. 调用 `get_node` 获取节点详情
  5. 下载文档内容并转换为 Markdown

### 待处理

- [ ] 处理快捷方式节点（`node_type: shortcut`，追踪 `origin_node_token`）
- [ ] 如果 lark-cli 不支持，改用飞书 Python SDK 或原生 REST API