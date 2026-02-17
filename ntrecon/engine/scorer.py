"""Simple heuristic-based risk scoring engine."""
from __future__ import annotations

from typing import Any, Dict, List


RULES = {
    ".env": 5,
    ".git": 5,
    "/admin": 3,
    "/swagger": 3,
    "s3.amazonaws.com": 2,
    "jwt": 2,
}


def calculate_score(results_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate risk score and level from normalized recon results."""
    score = 0
    findings: List[str] = []

    urls: List[str] = results_dict.get("urls", [])
    url_blob = "\n".join(urls).lower()

    for indicator, value in RULES.items():
        if indicator.lower() in url_blob:
            score += value
            findings.append(f"Indicador detectado: {indicator} (+{value})")

    nuclei_results = results_dict.get("nuclei", [])
    for item in nuclei_results:
        info = item.get("info", {}) if isinstance(item, dict) else {}
        severity = str(info.get("severity", "")).upper()
        template = info.get("name") or item.get("template-id") or "template desconhecido"
        if severity == "HIGH":
            score += 4
            findings.append(f"Nuclei HIGH: {template} (+4)")
        elif severity == "MEDIUM":
            score += 2
            findings.append(f"Nuclei MEDIUM: {template} (+2)")

    risk_level = "Low"
    if score >= 10:
        risk_level = "High"
    elif score >= 5:
        risk_level = "Medium"

    return {
        "score": score,
        "risk_level": risk_level,
        "findings": findings,
    }
