"""ntrecon CLI entrypoint."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

import typer
from rich import box
from rich.panel import Panel
from rich.table import Table

from config import DEFAULT_THREADS, REQUIRED_TOOLS
from core.runner import run_recon
from utils.logger import get_console, setup_logging

app = typer.Typer(help="ntrecon - Orquestrador inteligente de recon para bug bounty.")
console = get_console()


def _validate_dependencies(no_nuclei: bool) -> None:
    missing = []
    for tool in REQUIRED_TOOLS:
        if no_nuclei and tool == "nuclei":
            continue
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        msg = "\n".join(f"- {m}" for m in missing)
        raise typer.BadParameter(
            f"Ferramentas externas ausentes no PATH:\n{msg}\n"
            "Instale as dependências e tente novamente."
        )


@app.command()
def main(
    domain: str = typer.Option(..., "-d", "--domain", help="Domínio alvo (ex.: example.com)."),
    output: Optional[Path] = typer.Option(None, "-o", "--output", help="Diretório de saída dos relatórios."),
    no_nuclei: bool = typer.Option(False, "--no-nuclei", help="Desabilita execução do nuclei."),
    verbose: bool = typer.Option(False, "--verbose", help="Habilita logs detalhados."),
    threads: int = typer.Option(DEFAULT_THREADS, "--threads", min=1, help="Quantidade de threads para ferramentas suportadas."),
) -> None:
    """Run full ntrecon workflow."""
    setup_logging(verbose)
    _validate_dependencies(no_nuclei=no_nuclei)

    console.print(Panel.fit("[bold cyan]ntrecon[/bold cyan]\n[white]Smart Bug Bounty Recon Orchestrator[/white]", border_style="cyan"))

    results = run_recon(domain=domain, output_dir=str(output) if output else None, threads=threads, no_nuclei=no_nuclei)
    metrics = results["metrics"]
    risk = results["risk"]

    risk_color = {"Low": "green", "Medium": "yellow", "High": "red"}.get(risk["risk_level"], "white")

    table = Table(title="ntrecon Summary", box=box.SIMPLE_HEAVY)
    table.add_column("Métrica", style="bold")
    table.add_column("Valor")
    table.add_row("Total subdomínios", str(metrics["subdomains"]))
    table.add_row("Hosts ativos", str(metrics["active_hosts"]))
    table.add_row("URLs coletadas", str(metrics["urls"]))
    table.add_row("Findings", str(len(risk["findings"])))
    table.add_row("Score", str(risk["score"]))
    table.add_row("Risk level", f"[{risk_color}]{risk['risk_level']}[/{risk_color}]")
    console.print(table)


if __name__ == "__main__":
    app()
