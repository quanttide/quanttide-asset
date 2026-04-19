# 飞书知识库资产目录

## 格式

### JSON文件清单

适合一次性导出、节点数量相对较少、需要版本更新的场景。

feishu_wiki/
- metadata.json
- spaces/
  - space_<space_id>/
    - metadata.json
    - nodes/ 

### SQLite数据库

适合需要持续复用、节点数量相对较多、需要复杂查询的场景。

## 步骤

1. 知识库清单：调用`lark-cli api GET /open-apis/wiki/v2/spaces`，保存返回JSON到`spaces.json`
2. 知识库节点清单：调用`lark-cli api GET /open-apis/wiki/v2/spaces/{space_id}/nodes --params '{"parent_node_token":"{parent_token}","page_size":50}'`，
3. 节点详细信息：调用`lark-cli api GET /open-apis/wiki/v2/spaces/get_node --params '{"token":"{node_token}"}'`，获取JSON格式的节点元数据。
