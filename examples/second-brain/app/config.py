"""
配置模块：集中管理资产发现程序的所有配置。
从契约文件加载发现规则。
"""

from pathlib import Path
from typing import Final

import yaml
from returns.result import Success, safe


PROJECT_ROOT: Final = Path(__file__).parent.parent
CONTRACT_FILE: Final = ".quanttide/asset/contract.yaml"


@safe
def load_contract() -> dict:
    """从契约文件加载完整配置"""
    config_path = PROJECT_ROOT / CONTRACT_FILE
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_discovery() -> dict:
    """获取发现配置"""
    result = load_contract()
    if isinstance(result, Success):
        return result.unwrap().get("discovery", {})
    return {}


def get_assets() -> dict:
    """获取资产清单"""
    result = load_contract()
    if isinstance(result, Success):
        return result.unwrap().get("assets", {})
    return {}


DISCOVERY = get_discovery()
SCOPE: Final = DISCOVERY.get("scope", ["."])
FILTERS: Final = DISCOVERY.get("filters", {})
EXCLUDES: Final = FILTERS.get("excludes", [])
MAPS: Final = DISCOVERY.get("maps", {})