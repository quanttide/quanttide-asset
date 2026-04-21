"""
资产发现程序 (Asset Discovery)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本模块遵循量潮科技资产发现规范，核心逻辑分为两层：
1. 物理层：扫描文件系统，识别潜在资产。
2. 逻辑层：加载契约文件，进行状态对标（发现、缺失、变更）。
"""

from fnmatch import fnmatch
from pathlib import Path, PurePath
from typing import Dict, List

try:
    from .config import EXCLUDES, MAPS, get_assets
    from .schemas import Asset
except ImportError:
    from config import EXCLUDES, MAPS, get_assets
    from schemas import Asset


# --- 核心业务逻辑 ---


def identify_type(path: Path) -> str:
    """【功能 2：资产类型识别】根据映射规则自动识别资产类型"""
    rel_path = str(path)
    for map_name, map_rule in MAPS.items():
        if fnmatch(rel_path, map_rule["match"]):
            return map_rule.get("assign", {}).get("type", "unknown")
    return "unknown"


def is_excluded(path: Path, target: Path) -> bool:
    """检查路径是否被排除"""
    rel_path = path.relative_to(target)
    for pattern in EXCLUDES:
        clean_pattern = pattern
        if clean_pattern.startswith("**/"):
            clean_pattern = clean_pattern[3:]
        if clean_pattern.endswith("/**"):
            dir_name = clean_pattern[:-3]
            if dir_name in rel_path.parts:
                return True
        elif PurePath(rel_path).match(clean_pattern):
            return True
    return False


def scan_physical_assets(target: Path) -> List[Asset]:
    """【功能 1：目录扫描】执行文件系统扫描，初步发现所有数字资产"""
    return [
        Asset(str(p.relative_to(target)), identify_type(p), "discovered")
        for p in target.rglob("*")
        if p.is_file() and not is_excluded(p, target)
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

    # 索引契约路径，用于目录前缀匹配
    contract_paths = {info["path"]: info for info in contract.values()}

    def is_verified(path: str) -> bool:
        for contract_path in contract_paths:
            if path == contract_path or path.startswith(contract_path + "/"):
                return True
        return False

    # 对物理发现的资产进行状态分类
    results = [
        Asset(a.path, a.type, "verified" if is_verified(a.path) else "new_asset")
        for a in fs_assets
    ]

    # 追溯契约中定义但实际缺失的资产
    results += [
        Asset(p, info["type"], "missing")
        for p, info in contract_paths.items()
        if not any(is_verified(a.path) for a in fs_assets)
    ]

    return results


def discover(target_dir: str) -> List[Asset]:
    """
    资产发现主流程：
    1. 确定目标路径 -> 2. 尝试加载契约 -> 3. 执行物理扫描 -> 4. 验证比对
    """
    root = Path(target_dir)
    contract = get_assets()
    fs_assets = scan_physical_assets(root)
    return validate_against_contract(contract, fs_assets)
