"""
配置模块：集中管理资产发现程序的所有配置。
从契约文件加载发现规则。
"""

import yaml
from pathlib import Path
from typing import Final

PROJECT_ROOT: Final = Path(__file__).parent.parent
DATA_DIR: Final = PROJECT_ROOT / "data"
CONTRACT_FILE: Final = ".quanttide/asset/contract.yaml"


def load_discovery_config() -> dict:
    """从契约文件加载发现配置"""
    config_path = PROJECT_ROOT / CONTRACT_FILE
    if not config_path.exists():
        return {}
    with open(config_path) as f:
        return yaml.safe_load(f).get("discovery", {})


discovery = load_discovery_config()
TYPE_MAP: Final = discovery.get("type_map", {})
IGNORE_FILES: Final = set(discovery.get("ignore_files", []))
IGNORE_DIRS: Final = set(discovery.get("ignore_dirs", []))