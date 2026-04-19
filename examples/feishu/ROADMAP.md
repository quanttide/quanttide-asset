# ROADMAP

## 飞书知识库递归下载

### 已完成

- [x] 问题定位：API 用错了，`get_node` 是获取单个节点，`/wiki/v2/spaces/:space_id/nodes` 才是获取子节点列表
- [x] 确认本地 lark-cli 命令：
  - `lark-cli wiki spaces get_node` - 获取知识空间节点信息
  - `lark-cli docs +fetch` - 获取文档内容
  - `lark-cli api GET /open-apis/wiki/v2/spaces` - 获取知识库列表

### 进行中

- [ ] 使用本地 lark-cli 实现递归下载
  1. 安装：`npm i -g @lark-suite/cli`
  2. 授权：`lark-cli auth login`
  3. 获取知识库列表：`lark-cli api GET /open-apis/wiki/v2/spaces`
  4. 获取子节点列表：`lark-cli api GET /open-apis/wiki/v2/spaces/:space_id/nodes --params '{"parent_node_token": "xxx"}'`
  5. 获取节点详情：`lark-cli wiki spaces get_node`
  6. 下载文档内容：`lark-cli docs +fetch`

### 待处理

- [ ] 处理快捷方式节点（`node_type: shortcut`，追踪 `origin_node_token`）
- [ ] 如果 lark-cli 不支持，改用飞书 Python SDK 或原生 REST API