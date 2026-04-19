# 飞书知识库资产目录

## 格式

### JSON文件清单

适合一次性导出、节点数量相对较少、需要版本更新的场景。

```
feishu_wiki/
├── metadata.json          # 整体元数据（知识库列表、统计）
└── spaces/
    ├── space_{space_id}/
    │   ├── metadata.json  # 知识库信息（name, space_id, description）
    │   └── nodes/
    │       ├── node_{node_token}.json   # 节点详情（node + detail）
    │       └── ...
    └── ...
```

### SQLite数据库

适合需要持续复用、节点数量相对较多、需要复杂查询的场景。

## 步骤

1. 知识库清单：调用`lark-cli api GET /open-apis/wiki/v2/spaces`，保存返回JSON到`feishu_wiki/metadata.json`
2. 知识库节点清单：调用`lark-cli api GET /open-apis/wiki/v2/spaces/{space_id}/nodes --params '{"parent_node_token":"{parent_token}","page_size":50}'`，递归获取所有子节点
3. 节点详细信息：调用`lark-cli wiki spaces get_node --params '{"token":"{node_token}"}'`，获取JSON格式的节点元数据，保存到`spaces/space_{id}/nodes/{node_token}.json`
