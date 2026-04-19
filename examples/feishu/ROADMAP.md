# ROADMAP

## 飞书知识库递归下载

### 已完成

- [x] 问题定位：API 用错了，`get_node` 是获取单个节点，`/wiki/v2/spaces/:space_id/nodes` 才是获取子节点列表
- [x] 验证本地 lark-cli 命令（`--help` + `--dry-run`）：
  - `lark-cli wiki spaces get_node` - 获取知识空间节点信息
  - `lark-cli docs +fetch` - 获取文档内容
  - `lark-cli api GET /open-apis/wiki/v2/spaces/:space_id/nodes` - 通用 API 调用

### 进行中

- [ ] 验证 API 实际可用性（先用 --dry-run 测试每个命令）

  ```bash
  # 测试获取知识库列表
  lark-cli api GET /open-apis/wiki/v2/spaces --dry-run

  # 测试获取子节点列表
  lark-cli api GET /open-apis/wiki/v2/spaces/xxx/nodes --dry-run --params '{"parent_node_token":"xxx"}'
  ```

- [ ] 根据验证结果调整方案

### 待处理

- [ ] 实现递归下载脚本
- [ ] 处理快捷方式节点（`node_type: shortcut`，追踪 `origin_node_token`）
- [ ] 如果 lark-cli 不支持，改用飞书 Python SDK 或原生 REST API

## 改进

- 先验证再设计方案
- 用 `--dry-run` 测试每个假设
- 不确定的 API 先做小规模测试