"""
配置模块：集中管理资产发现程序的所有配置。
"""

from pathlib import Path
from typing import Final

PROJECT_ROOT: Final = Path(__file__).parent.parent
DATA_DIR: Final = PROJECT_ROOT / "data"
CONTRACT_FILE: Final = ".quanttide/asset/contract.yaml"

TYPE_MAP: Final = {
    ".md": "docs",
    ".txt": "docs",
    ".pdf": "docs",
    ".py": "code",
    ".js": "code",
    ".ts": "code",
    ".yaml": "config",
    ".yml": "config",
    ".json": "config",
    ".toml": "config",
    ".csv": "data",
    ".sqlite": "data",
    ".lock": "config",
}

IGNORE_FILES: Final = {".gitignore", ".python-version", "uv.lock"}
IGNORE_DIRS: Final = {".venv", "data", ".git", "__pycache__", ".ruff_cache", ".pytest_cache"}