"""NapCat QQ 适配器插件入口 — 导出 register 函数。"""

import sys
from pathlib import Path

# 确保插件目录在 sys.path 中，以便 adapter.py 能导入 napcat_adapter
_插件目录 = str(Path(__file__).parent)
if _插件目录 not in sys.path:
    sys.path.insert(0, _插件目录)

from .adapter import register

__all__ = ["register"]