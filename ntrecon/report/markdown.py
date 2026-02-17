"""Markdown report formatter."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict


def build_markdown_report(report_data: Dict[str, Any]) -> str:
    """Build a professional markdown report from collected results."""
    domain = report_data["domain"]
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metrics = report_data["metrics"]
    risk = report_data["risk"]

    findings_section = "\n".join(f"- {f}" for f in risk.get("findings", [])) or "- Nenhum finding crítico identificado pelas heurísticas."

    return f"""# ntrecon Security Recon Report

**Data:** {created_at}

## Escopo

- Domínio alvo: `{domain}`
- Tipo: Reconhecimento passivo/ativo leve

## Resumo Executivo

Este relatório consolida resultados automatizados de enumeração, coleta de superfície e varredura de templates para apoiar priorização de risco em programas de bug bounty.

## Métricas

- Total de subdomínios: **{metrics['subdomains']}**
- Hosts ativos: **{metrics['active_hosts']}**
- URLs coletadas: **{metrics['urls']}**
- Findings de scanner: **{metrics['nuclei_findings']}**

## Findings

{findings_section}

## Risk Score

- Score final: **{risk['score']}**
- Nível de risco: **{risk['risk_level']}**

## Recomendações

1. Validar manualmente os endpoints sensíveis identificados.
2. Priorizar correções para exposições de configuração e painéis administrativos.
3. Integrar execução recorrente do ntrecon no ciclo de security testing.
4. Revisar e expandir templates do Nuclei conforme tecnologia do alvo.
"""
