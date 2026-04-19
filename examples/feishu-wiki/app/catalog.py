#!/usr/bin/env python3
# catalog.py - 下载知识库到本地

import subprocess
import json
import os
import time
from config import BASE_DIR, SPACES_DIR, PAGE_SIZE, REQUEST_DELAY

os.makedirs(SPACES_DIR, exist_ok=True)

def run_lark_cli(args):
    cmd = ["lark-cli"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"执行失败: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"JSON解析失败")
        return None

def run_api(method, path, params=None):
    cmd = ["api", method, path]
    if params:
        cmd.extend(["--params", json.dumps(params)])
    return run_lark_cli(cmd)

def get_node_detail(node_token):
    return run_lark_cli(["wiki", "spaces", "get_node", "--params", json.dumps({"token": node_token})])

def save_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  💾 已保存: {filepath}")

def fetch_nodes(space_id, parent_token, indent=0):
    page_token = None
    prefix = "  " * indent
    all_nodes = []

    while True:
        params = {"parent_node_token": parent_token, "page_size": PAGE_SIZE}
        if page_token:
            params["page_token"] = page_token

        resp = run_api("GET", f"/open-apis/wiki/v2/spaces/{space_id}/nodes", params)
        if not resp or resp.get("code") != 0:
            print(f"{prefix}[错误] 获取节点列表失败")
            break

        data = resp.get("data", {})
        items = data.get("items", [])

        for node in items:
            node_token = node.get("node_token")
            title = node.get("title", "未命名")

            print(f"{prefix}├─ {title}")

            all_nodes.append(node)

            # 获取节点详情并保存到 nodes/ 目录
            detail = get_node_detail(node_token)
            if detail and detail.get("code") == 0:
                node_data = {
                    "node": node,
                    "detail": detail.get("data", {})
                }
                save_json(node_data, f"{SPACES_DIR}/space_{space_id}/nodes/node_{node_token}.json")

            if node.get("has_child"):
                child_nodes = fetch_nodes(space_id, node_token, indent + 1)
                all_nodes.extend(child_nodes)

            time.sleep(REQUEST_DELAY)

        if not data.get("has_more"):
            break
        page_token = data.get("page_token")

    return all_nodes

def main():
    print("=== 获取知识库列表 ===")
    resp = run_api("GET", "/open-apis/wiki/v2/spaces")

    if not resp or resp.get("code") != 0:
        print(f"获取知识库列表失败")
        return

    spaces = resp.get("data", {}).get("items", [])
    if not spaces:
        print("未找到任何知识库")
        return

    all_spaces = []

    for space in spaces:
        space_id = space.get("space_id")
        space_name = space.get("name")

        print(f"\n{'='*50}")
        print(f"知识库: {space_name} ({space_id})")
        print(f"{'='*50}")

        space_dir = f"{SPACES_DIR}/space_{space_id}"
        os.makedirs(f"{space_dir}/nodes", exist_ok=True)

        # 保存知识库 metadata
        space_data = {
            "space": space,
            "nodes_count": 0
        }
        save_json(space_data, f"{space_dir}/metadata.json")

        # 获取节点树
        nodes = fetch_nodes(space_id, "")
        print(f"\n共获取 {len(nodes)} 个节点")

        all_spaces.append({
            "space_id": space_id,
            "name": space_name,
            "nodes_count": len(nodes)
        })

    # 保存整体 metadata
    metadata = {
        "spaces": all_spaces,
        "total_spaces": len(all_spaces),
        "total_nodes": sum(s["nodes_count"] for s in all_spaces)
    }
    save_json(metadata, f"{BASE_DIR}/metadata.json")

    print(f"\n=== 完成，保存在 {BASE_DIR} ===")

if __name__ == "__main__":
    main()
