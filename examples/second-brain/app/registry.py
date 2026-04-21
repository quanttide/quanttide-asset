"""
资产注册模块 (Asset Registry)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

负责将资产发现结果持久化到本地存储。
"""

import json
from dataclasses import asdict
from pathlib import Path
from typing import List

from returns.result import Result, Success, safe

try:
    from .schemas import Asset
except ImportError:
    from schemas import Asset


@safe
def save_assets(assets: List[Asset], output_path: Path | None = None) -> Path:
    """将资产发现结果写入 data/ 目录"""
    if output_path is None:
        output_path = Path(__file__).parent.parent / "data" / "assets.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump([asdict(a) for a in assets], f, indent=2)

    return output_path
