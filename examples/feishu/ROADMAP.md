# ROADMAP

## 飞书知识库递归下载

### 已完成

- [x] 问题定位：API 用错了，`get_node` 是获取单个节点，`/wiki/v2/spaces/:space_id/nodes` 才是获取子节点列表
- [x] 验证 lark-cli 是否支持 list API：需要测试 `lark-cli api GET /wiki/v2/spaces/:space_id/nodes`
- [x] 确认权限范围：确认 access_token 包含必要的权限 scope

### 进行中

- [ ] 使用 lark-cli 实现递归下载
  1. 安装本地 lark-cli：`pip install lark-cli`
  2. 配置 access_token
  3. 调用 `lark-cli api GET /wiki/v2/spaces` 获取知识库列表
  4. 递归调用 `lark-cli api GET /wiki/v2/spaces/:space_id/nodes` 获取子节点
  5. 调用 `lark-cli api GET /wiki/v2/spaces/get_node` 获取节点详情
  6. 调用 `lark-cli docs fetch` 下载文档内容

### 待处理

- [ ] 处理快捷方式节点（`node_type: shortcut`，追踪 `origin_node_token`）
- [ ] 如果 lark-cli 不支持，改用飞书 Python SDK 或原生 REST API