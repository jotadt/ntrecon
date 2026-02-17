"""JSON reporting helpers."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def export_json(data: Dict[str, Any], path: Path) -> None:
    """Write report dictionary as pretty JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
