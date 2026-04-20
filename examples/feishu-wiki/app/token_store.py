#!/usr/bin/env python3
"""
token_store.py - token 的读写和过期管理

存储格式（.lark_token）：
  {"token": "t-xxx", "expires_at": 1713600000.0}

过期提前 5 分钟刷新，避免请求途中 token 失效。
"""

import json
import os
import time

TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".lark_token")
EXPIRE_BUFFER = 300  # 提前 5 分钟视为过期


def save_token(token: str, expires_in: int = 7200):
    """
    保存 token 到文件。
    expires_in: token 有效期（秒），飞书默认 7200。
    proxy.py 捕获到 token 时调用此函数。
    """
    data = {
        "token": token,
        "expires_at": time.time() + expires_in - EXPIRE_BUFFER,
    }
    # 写临时文件再 rename，避免写入一半时被读到损坏数据
    tmp = TOKEN_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp, TOKEN_FILE)


def load_token() -> str | None:
    """
    读取 token，过期则返回 None。
    """
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if time.time() < data.get("expires_at", 0):
            return data.get("token")
        else:
            print("[TOKEN] 已过期，需要重新获取")
            return None
    except (json.JSONDecodeError, KeyError):
        # 文件损坏，删掉重来
        os.remove(TOKEN_FILE)
        return None


def clear_token():
    """手动清除 token（如需强制重新登录）。"""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("[TOKEN] 已清除")
