"""
主程序入口
"""

from returns.result import Success

from .discovery import discover
from .registry import save_assets


def main():
    assets = discover(".")
    output_result = save_assets(assets)
    if isinstance(output_result, Success):
        print(f"Saved {len(assets)} assets to {output_result.unwrap()}")
    else:
        print(f"Failed to save assets: {output_result.failure()}")


if __name__ == "__main__":
    main()
