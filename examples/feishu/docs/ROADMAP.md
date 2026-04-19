# 飞书知识库递归下载 - 详细方案

## 问题定位

API 用错了，`get_node` 是获取单个节点，`/wiki/v2/spaces/:space_id/nodes` 才是获取子节点列表

## 验证本地 lark-cli 命令

用 `--help` 和 `--dry-run` 验证：

```bash
# 查看 wiki 子命令
lark-cli wiki --help
lark-cli wiki spaces --help

# 查看 docs 子命令
lark-cli docs --help

# 验证 API 调用方式
lark-cli api GET /open-apis/wiki/v2/spaces --help
```

### 已确认命令

- `lark-cli wiki spaces get_node` - 获取知识空间节点信息
- `lark-cli docs +fetch` - 获取文档内容
- `lark-cli api GET /open-apis/wiki/v2/spaces/:space_id/nodes` - 通用 API 调用获取子节点列表

## 验证 API 实际可用性

先用 --dry-run 测试每个命令：

```bash
# 测试获取知识库列表
lark-cli api GET /open-apis/wiki/v2/spaces --dry-run

# 测试获取子节点列表
lark-cli api GET /open-apis/wiki/v2/spaces/xxx/nodes --dry-run --params '{"parent_node_token":"xxx"}'
```

## 实现步骤

1. 安装：`npm i -g @lark-suite/cli`
2. 授权：`lark-cli auth login`
3. 获取知识库列表：`lark-cli api GET /open-apis/wiki/v2/spaces`
4. 获取子节点列表：`lark-cli api GET /open-apis/wiki/v2/spaces/:space_id/nodes --params '{"parent_node_token": "xxx"}'`
5. 获取节点详情：`lark-cli wiki spaces get_node`
6. 下载文档内容：`lark-cli docs +fetch`
7. 处理快捷方式节点（`node_type: shortcut`，追踪 `origin_node_token`）

## 待处理

- 如果 lark-cli 不支持，改用飞书 Python SDK 或原生 REST API

## 改进

- 先验证再设计方案
- 用 `--dry-run` 测试每个假设
- 不确定的 API 先做小规模测试