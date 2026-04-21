"""
数据模型定义
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Asset:
    """资产模型：对标规范中的资产定义，包含路径、类型及生命周期状态"""

    path: str
    type: str
    status: str  # 对应事件：discovered, verified, missing, new_asset
