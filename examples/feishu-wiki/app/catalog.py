#!/usr/bin/env python3
# catalog.py - 下载知识库到本地

import json
import os
import time
import subprocess
import shutil
import requests
from config import (
    BASE_DIR,
    SPACES_DIR,
    PAGE_SIZE,
    REQUEST_DELAY,
    space_dir,
    node_file,
    metadata_file,
    ensure_space_dirs,
)

os.makedirs(SPACES_DIR, exist_ok=True)
os.makedirs(BASE_DIR, exist_ok=True)

FEISHU_BASE = "https://open.feishu.cn"

# ─────────────────────────────────────────────
# Token 获取：三种方式按优先级依次尝试
# ─────────────────────────────────────────────

def _token_from_env():
    return os.getenv("FEISHU_ACCESS_TOKEN") or os.getenv("LARK_ACCESS_TOKEN")


def _token_from_file():
    """从 token_store 读取，自动检查过期。"""
    try:
        from token_store import load_token
        return load_token()
    except ImportError:
        return None


def _token_from_lark_cli():
    exe = shutil.which("lark-cli") or shutil.which("lark-cli.exe")
    if not exe:
        cli_js = "C:/Users/雨下雨停/AppData/Roaming/npm/node_modules/@larksuite/cli/bin/lark-cli.exe"
        if os.path.exists(cli_js):
            exe = cli_js
    if not exe:
        return None
    try:
        proc = subprocess.run(
            [exe, "token"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            encoding="utf-8", errors="replace", timeout=10,
        )
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line.startswith(("t-", "u-")) or (line and " " not in line and len(line) > 20):
                # 顺手存起来，下次直接走文件
                try:
                    from token_store import save_token
                    save_token(line)
                except ImportError:
                    pass
                return line
    except Exception as e:
        print(f"[WARN] lark-cli token 失败: {e}")
    return None


_cached_token = None


def get_access_token():
    global _cached_token
    if _cached_token:
        # 每次用之前验证文件里是否仍有效（防止长时间运行中过期）
        fresh = _token_from_file()
        if fresh:
            _cached_token = fresh
            return _cached_token

    token = _token_from_env() or _token_from_file() or _token_from_lark_cli()
    if not token:
        raise RuntimeError(
            "无法获取飞书 access token，请选择以下方式之一：\n"
            "  1. 先启动代理：python proxy.py\n"
            "     再运行（PowerShell）：$env:LARK_ENDPOINT='http://localhost:7777'; python catalog.py\n"
            "  2. 手动设置：$env:FEISHU_ACCESS_TOKEN='<your_token>'; python catalog.py"
        )
    _cached_token = token
    return token


# ─────────────────────────────────────────────
# HTTP 请求
# ─────────────────────────────────────────────

def feishu_get(path, params=None, _retry=True):
    """
    用 requests 直接请求飞书 API。
    token 过期时自动清除缓存重试一次。
    """
    global _cached_token
    token = get_access_token()
    url = FEISHU_BASE + path
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # token 过期（飞书返回 code=99991671 或 99991672）
        if data.get("code") in (99991671, 99991672) and _retry:
            print("[TOKEN] 服务端报告 token 过期，清除缓存后重试...")
            _cached_token = None
            try:
                from token_store import clear_token
                clear_token()
            except ImportError:
                pass
            return feishu_get(path, params, _retry=False)

        return data
    except requests.HTTPError as e:
        print(f"[HTTP错误] {e} | {url} params={params}")
        return None
    except requests.RequestException as e:
        print(f"[请求失败] {e} | {url}")
        return None


# ─────────────────────────────────────────────
# 业务函数
# ─────────────────────────────────────────────

def get_spaces():
    spaces = []
    page_token = None
    while True:
        params = {"page_size": PAGE_SIZE}
        if page_token:
            params["page_token"] = page_token
        resp = feishu_get("/open-apis/wiki/v2/spaces", params)
        if not resp or resp.get("code") != 0:
            msg = resp.get("msg", "无响应") if resp else "无响应"
            print(f"[错误] 获取知识库列表失败: {msg}")
            break
        data = resp.get("data", {})
        spaces.extend(data.get("items", []))
        if not data.get("has_more"):
            break
        page_token = data.get("page_token")
    return spaces


def get_node_detail(node_token):
    if not node_token:
        return None
    return feishu_get("/open-apis/wiki/v2/spaces/get_node", {"token": node_token})


def save_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [SAVE] {filepath}")


def clean_deleted_nodes(space_id, valid_tokens):
    nodes_dir = f"{space_dir(space_id)}/nodes"
    if not os.path.exists(nodes_dir):
        return
    valid_set = set(valid_tokens)
    deleted_count = 0
    for filename in os.listdir(nodes_dir):
        if filename.startswith("node_") and filename.endswith(".json"):
            token = filename[5:-5]
            if token not in valid_set:
                filepath = os.path.join(nodes_dir, filename)
                os.remove(filepath)
                deleted_count += 1
                print(f"  [DEL] {filepath}")
    if deleted_count > 0:
        print(f"  共清理 {deleted_count} 个已删除节点")


def fetch_nodes(space_id, parent_token, indent=0):
    page_token = None
    prefix = "  " * indent
    all_nodes = []
    node_index = []

    while True:
        params = {"page_size": PAGE_SIZE}
        if parent_token:
            params["parent_node_token"] = parent_token
        if page_token:
            params["page_token"] = page_token

        resp = feishu_get(f"/open-apis/wiki/v2/spaces/{space_id}/nodes", params)
        if not resp or resp.get("code") != 0:
            msg = resp.get("msg", "无响应") if resp else "无响应"
            print(f"{prefix}[错误] 获取节点列表失败: {msg}")
            break

        data = resp.get("data", {})
        items = data.get("items", [])

        for node in items:
            node_token = node.get("node_token")
            title = node.get("title", "未命名")
            print(f"{prefix}├─ {title}")

            all_nodes.append(node)
            node_index.append({
                "node_token": node_token,
                "title": title,
                "obj_type": node.get("obj_type"),
                "parent_token": node.get("parent_node_token"),
                "has_child": node.get("has_child"),
                "updated_at": node.get("updated_at"),
            })

            detail = get_node_detail(node_token)
            if detail and detail.get("code") == 0:
                node_data = {"node": node, "detail": detail.get("data", {})}
                save_json(node_data, node_file(space_id, node_token))
            elif detail:
                print(f"{prefix}  [WARN] 节点详情失败 ({node_token}): {detail.get('msg', '')}")

            if node.get("has_child"):
                child_nodes, child_index = fetch_nodes(space_id, node_token, indent + 1)
                all_nodes.extend(child_nodes)
                node_index.extend(child_index)

            time.sleep(REQUEST_DELAY)

        if not data.get("has_more"):
            break
        page_token = data.get("page_token")

    return all_nodes, node_index


# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    print("=== 获取知识库列表 ===")
    spaces = get_spaces()
    if not spaces:
        print("未找到任何知识库")
        return

    target_space_ids = None
    try:
        from validate import load_contract
        contract_spaces = load_contract().get("spaces", [])
        if contract_spaces:
            target_space_ids = {s["id"] for s in contract_spaces}
            print(f"契约过滤：仅同步 {len(target_space_ids)} 个知识库")
    except (FileNotFoundError, ImportError):
        pass

    all_spaces = []

    for space in spaces:
        space_id = space.get("space_id")
        space_name = space.get("name")

        # 调试用的硬编码过滤，正式使用时删掉这段
        if space_id != "7526874705676091393":
            print(f"[SKIP] {space_name} ({space_id})")
            continue

        if target_space_ids and space_id not in target_space_ids:
            print(f"[SKIP] 未在契约中声明: {space_name} ({space_id})")
            continue

        print(f"\n{'=' * 50}")
        print(f"知识库: {space_name} ({space_id})")
        print(f"{'=' * 50}")

        ensure_space_dirs(space_id)

        nodes, node_index = fetch_nodes(space_id, "")
        print(f"\n共获取 {len(nodes)} 个节点")

        valid_tokens = [n["node_token"] for n in node_index]
        clean_deleted_nodes(space_id, valid_tokens)

        space_data = {
            "space": space,
            "nodes_count": len(nodes),
            "nodes": node_index,
            "synced_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        save_json(space_data, metadata_file(space_id))
        all_spaces.append({"space_id": space_id, "name": space_name, "nodes_count": len(nodes)})

    metadata = {
        "spaces": all_spaces,
        "total_spaces": len(all_spaces),
        "total_nodes": sum(s["nodes_count"] for s in all_spaces),
    }
    save_json(metadata, f"{BASE_DIR}/metadata.json")
    print(f"\n=== 完成，保存在 {BASE_DIR} ===")


if __name__ == "__main__":
    main()
