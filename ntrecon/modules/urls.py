"""URL collection integrations."""
from __future__ import annotations

import logging
import shutil
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def collect_urls(domain: str) -> List[str]:
    """Run gau and return URLs for target domain."""
    if not shutil.which("gau"):
        raise FileNotFoundError("'gau' não encontrado no PATH. Instale a ferramenta para continuar.")

    cmd = ["gau", "--subs", domain]
    logger.debug("Executando: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"gau falhou: {result.stderr.strip() or 'erro desconhecido'}")

    urls = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return sorted(set(urls))
