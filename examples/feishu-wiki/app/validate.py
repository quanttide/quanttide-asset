#!/usr/bin/env python3
"""对照契约检查已下载的目录快照"""

import json
import yaml
from config import BASE_DIR, metadata_file


def load_contract():
    with open("contract.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_catalog_metadata():
    with open(f"{BASE_DIR}/metadata.json") as f:
        return json.load(f)


def validate():
    contract = load_contract()
    catalog = load_catalog_metadata()

    catalog_space_ids = {s["space_id"] for s in catalog["spaces"]}

    for required_space in contract["spaces"]:
        space_id = required_space["id"]
        if space_id not in catalog_space_ids:
            print(f"[FAIL] 缺失知识库: {required_space['name']} ({space_id})")
            continue

        print(f"[PASS] 知识库存在: {required_space['name']}")

        required_nodes = required_space.get("required_nodes", [])
        if not required_nodes:
            continue

        with open(metadata_file(space_id)) as f:
            space_data = json.load(f)
        node_titles = [n["title"] for n in space_data.get("nodes", [])]

        for keyword in required_nodes:
            matched = any(keyword in title for title in node_titles)
            status = "[PASS]" if matched else "[FAIL]"
            print(f"  {status} 节点{'存在' if matched else '缺失'}: 含 '{keyword}'")


if __name__ == "__main__":
    validate()
