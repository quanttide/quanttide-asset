# 飞书知识库资产目录

1. 知识库清单：调用`lark-cli api GET /open-apis/wiki/v2/spaces`，保存返回JSON到`spaces.json`
2. 知识库节点清单：调用`lark-cli api GET /open-apis/wiki/v2/spaces/{space_id}/nodes --params '{"parent_node_token":"{parent_token}","page_size":50}'`，
3. 节点详细信息：调用`lark-cli api GET /open-apis/wiki/v2/spaces/get_node --params '{"token":"{node_token}"}'`，获取JSON格式的节点元数据。
