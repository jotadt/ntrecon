"""Nuclei integration module."""
from __future__ import annotations

import json
import logging
import shutil
import subprocess
from typing import Any, Dict, Iterable, List

logger = logging.getLogger(__name__)


def scan_with_nuclei(targets: Iterable[str], threads: int = 10) -> List[Dict[str, Any]]:
    """Run nuclei in JSON output mode and parse findings."""
    target_list = [t.strip() for t in targets if t.strip()]
    if not target_list:
        return []

    if not shutil.which("nuclei"):
        raise FileNotFoundError("'nuclei' não encontrado no PATH. Instale a ferramenta para continuar.")

    cmd = ["nuclei", "-jsonl", "-silent", "-nc", "-c", str(threads)]
    logger.debug("Executando: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        input="\n".join(target_list),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"nuclei falhou: {result.stderr.strip() or 'erro desconhecido'}")

    findings: List[Dict[str, Any]] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            findings.append(json.loads(line))
        except json.JSONDecodeError:
            logger.debug("Linha não JSON do nuclei ignorada: %s", line)
    return findings
