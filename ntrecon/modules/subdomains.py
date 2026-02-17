"""Subdomain discovery integrations."""
from __future__ import annotations

import logging
import shutil
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def enumerate_subdomains(domain: str) -> List[str]:
    """Run subfinder and return discovered subdomains."""
    if not shutil.which("subfinder"):
        raise FileNotFoundError("'subfinder' não encontrado no PATH. Instale a ferramenta para continuar.")

    cmd = ["subfinder", "-silent", "-d", domain]
    logger.debug("Executando: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"subfinder falhou: {result.stderr.strip() or 'erro desconhecido'}")

    subdomains = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return sorted(set(subdomains))
