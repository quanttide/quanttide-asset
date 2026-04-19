#!/usr/bin/env python3
# feishu-wiki-downloader.py

import subprocess
import json
import os
import time

OUTPUT_DIR = "./data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_cli_api(method, path, params=None):
    """调用 lark-cli api 命令并返回解析后的 JSON"""
    cmd = ["lark-cli", "api", method, path]
    if params:
        cmd.extend(["--params", json.dumps(params)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"API 调用失败: {result.stderr}")
        return None
    return json.loads(result.stdout)

def download_document(obj_token, obj_type, title):
    """下载文档内容"""
    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()
    filepath = f"{OUTPUT_DIR}/{safe_title}.md"

    if obj_type == "docx":
        resp = run_cli_api("GET", f"/open-apis/docx/v1/documents/{obj_token}/raw_content")
        if resp and resp.get("code") == 0:
            content = resp.get("data", {}).get("content", "")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  📄 已下载: {safe_title}.md")
            return True
    # 其他类型可按需扩展
    return False

def fetch_nodes(space_id, parent_token, indent=0):
    """递归获取子节点"""
    page_token = None
    prefix = "  " * indent

    while True:
        params = {"parent_node_token": parent_token, "page_size": 50}
        if page_token:
            params["page_token"] = page_token

        resp = run_cli_api("GET", f"/open-apis/wiki/v2/spaces/{space_id}/nodes", params)
        if not resp or resp.get("code") != 0:
            print(f"{prefix}[错误] 获取节点列表失败: {resp}")
            break

        data = resp.get("data", {})
        items = data.get("items", [])

        for node in items:
            node_token = node.get("node_token")
            title = node.get("title", "未命名")
            has_child = node.get("has_child", False)
            obj_type = node.get("obj_type", "")

            print(f"{prefix}├─ {title} ({obj_type})")

            # 获取节点详情
            detail = run_cli_api("GET", "/open-apis/wiki/v2/spaces/get_node", {"token": node_token})
            if detail and detail.get("code") == 0:
                obj_token = detail.get("data", {}).get("node", {}).get("obj_token")
                if obj_token:
                    download_document(obj_token, obj_type, title)

            # 递归子节点
            if has_child:
                fetch_nodes(space_id, node_token, indent + 1)

            # 避免触发频率限制
            time.sleep(0.2)

        if not data.get("has_more"):
            break
        page_token = data.get("page_token")

def main():
    print("=== 获取知识库列表 ===")
    resp = run_cli_api("GET", "/open-apis/wiki/v2/spaces")

    if not resp or resp.get("code") != 0:
        print(f"获取知识库列表失败: {resp}")
        return

    spaces = resp.get("data", {}).get("items", [])
    if not spaces:
        print("未找到任何知识库，请确认应用已添加到知识库成员中")
        return

    for space in spaces:
        space_id = space.get("space_id")
        space_name = space.get("name")
        root_token = space.get("root_node_token")

        print(f"\n{'='*50}")
        print(f"知识库: {space_name} ({space_id})")
        print(f"{'='*50}")

        if root_token:
            fetch_nodes(space_id, root_token)
        else:
            print("该知识库无根节点，跳过")

    print(f"\n=== 下载完成，文件保存在 {OUTPUT_DIR} ===")

if __name__ == "__main__":
    main()
