"""HTTP probing using httpx."""
from __future__ import annotations

import logging
import shutil
import subprocess
from typing import Iterable, List

logger = logging.getLogger(__name__)


def probe_hosts(hosts: Iterable[str], threads: int = 10) -> List[str]:
    """Run httpx against a host list and return responsive URLs."""
    host_list = [h.strip() for h in hosts if h.strip()]
    if not host_list:
        return []

    if not shutil.which("httpx"):
        raise FileNotFoundError("'httpx' não encontrado no PATH. Instale a ferramenta para continuar.")

    cmd = ["httpx", "-silent", "-threads", str(threads)]
    logger.debug("Executando: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        input="\n".join(host_list),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"httpx falhou: {result.stderr.strip() or 'erro desconhecido'}")

    active = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return sorted(set(active))
