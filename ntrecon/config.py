"""Central configuration for ntrecon."""
from __future__ import annotations

from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("output")
DEFAULT_THREADS = 10
DATE_FMT = "%Y-%m-%d %H:%M:%S"

REQUIRED_TOOLS = {
    "subfinder": "ProjectDiscovery subdomain enumerator",
    "httpx": "ProjectDiscovery HTTP probe",
    "gau": "GetAllURLs collector",
    "nuclei": "ProjectDiscovery template scanner",
}
