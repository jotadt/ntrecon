"""Main orchestration flow for ntrecon."""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from rich.progress import Progress, SpinnerColumn, TextColumn

from config import DEFAULT_OUTPUT_DIR
from engine.scorer import calculate_score
from modules.http_probe import probe_hosts
from modules.scanner import scan_with_nuclei
from modules.subdomains import enumerate_subdomains
from modules.urls import collect_urls
from report.json_export import export_json
from report.markdown import build_markdown_report

logger = logging.getLogger(__name__)


def run_recon(domain: str, output_dir: str | None, threads: int = 10, no_nuclei: bool = False) -> Dict[str, Any]:
    """Execute complete recon workflow and return normalized report data."""
    out_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Enumerando subdomínios...", total=None)
        subdomains = enumerate_subdomains(domain)

        progress.update(task, description="Probing hosts ativos (httpx)...")
        active_hosts = probe_hosts(subdomains, threads=threads)

        progress.update(task, description="Coletando URLs (gau)...")
        urls = collect_urls(domain)

        nuclei_results = []
        if not no_nuclei:
            progress.update(task, description="Executando nuclei...")
            nuclei_results = scan_with_nuclei(active_hosts, threads=threads)

        progress.update(task, description="Calculando score de risco...")
        risk = calculate_score({"urls": urls, "nuclei": nuclei_results})

        progress.update(task, description="Finalizando relatório...")
        progress.stop()

    report_data: Dict[str, Any] = {
        "domain": domain,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "results": {
            "subdomains": subdomains,
            "active_hosts": active_hosts,
            "urls": urls,
            "nuclei": nuclei_results,
        },
        "metrics": {
            "subdomains": len(subdomains),
            "active_hosts": len(active_hosts),
            "urls": len(urls),
            "nuclei_findings": len(nuclei_results),
        },
        "risk": risk,
    }

    json_path = out_dir / f"{domain}.json"
    md_path = out_dir / f"{domain}.md"

    export_json(report_data, json_path)
    md_path.write_text(build_markdown_report(report_data), encoding="utf-8")

    logger.info("Relatórios gerados em: %s e %s", json_path, md_path)
    return report_data
