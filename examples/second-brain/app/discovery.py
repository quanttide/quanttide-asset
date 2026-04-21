"""
资产发现程序 (Asset Discovery)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本模块遵循量潮科技资产发现规范，核心逻辑分为两层：
1. 物理层：扫描文件系统，识别潜在资产。
2. 逻辑层：加载契约文件，进行状态对标（发现、缺失、变更）。
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List

import yaml

from .config import CONTRACT_FILE, IGNORE_FILES, IGNORE_DIRS, TYPE_MAP


@dataclass(frozen=True)
class Asset:
    """资产模型：对标规范中的资产定义，包含路径、类型及生命周期状态"""

    path: str
    type: str
    status: str  # 对应事件：discovered, verified, missing, new_asset


# --- 核心业务逻辑 ---


def identify_type(path: Path) -> str:
    """【功能 2：资产类型识别】根据扩展名自动识别资产类别"""
    if path.suffix:
        return TYPE_MAP.get(path.suffix, "unknown")
    if path.name in {".gitignore", ".python-version"}:
        return "config"
    return "unknown"


def load_contract(target: Path) -> Dict:
    """【功能 3：契约加载策略】尝试读取契约文件"""
    contract_path = target / CONTRACT_FILE
    if not contract_path.exists():
        return {}
    with open(contract_path) as f:
        return yaml.safe_load(f).get("assets", {})


def scan_physical_assets(target: Path) -> List[Asset]:
    """【功能 1：目录扫描】执行文件系统扫描，初步发现所有数字资产"""
    return [
        Asset(str(p.relative_to(target)), identify_type(p), "discovered")
        for p in target.rglob("*")
        if p.is_file()
        and p.name not in IGNORE_FILES
        and not any(ignored in p.parts for ignored in IGNORE_DIRS)
    ]


def validate_against_contract(contract: Dict, fs_assets: List[Asset]) -> List[Asset]:
    """
    【契约验证模式】核心对比算法：
    1. 标记新增：物理存在但契约未定义 -> new_asset
    2. 标记验证：物理存在且契约已定义 -> verified
    3. 标记缺失：契约定义但物理不存在 -> missing
    """
    if not contract:
        return fs_assets  # 无契约时：仅执行文件系统发现

    # 索引契约路径，用于快速比对
    contract_map = {info["path"]: info for info in contract.values()}
    fs_paths = {a.path for a in fs_assets}

    # 对物理发现的资产进行状态分类
    results = [
        a._replace(status="verified" if a.path in contract_map else "new_asset")
        for a in fs_assets
    ]

    # 追溯契约中定义但实际缺失的资产
    results += [
        Asset(p, info["type"], "missing")
        for p, info in contract_map.items()
        if p not in fs_paths
    ]

    return results


# --- 程序入口 ---


def save_assets(assets: List[Asset], output_path: Path | None = None) -> Path:
    """将资产发现结果写入 data/ 目录"""
    if output_path is None:
        output_path = Path(__file__).parent.parent / "data" / "assets.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump([asdict(a) for a in assets], f, indent=2)

    return output_path


def discover(target_dir: str) -> List[Asset]:
    """
    资产发现主流程：
    1. 确定目标路径 -> 2. 尝试加载契约 -> 3. 执行物理扫描 -> 4. 验证比对
    """
    root = Path(target_dir)
    contract = load_contract(root)
    fs_assets = scan_physical_assets(root)
    return validate_against_contract(contract, fs_assets)


if __name__ == "__main__":
    assets = discover(".")
    output_path = save_assets(assets)
    print(f"Saved {len(assets)} assets to {output_path}")
