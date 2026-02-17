# ntrecon

ntrecon é uma ferramenta CLI em Python 3.11+ para **recon em bug bounty** com orquestração de ferramentas externas, normalização de dados e um motor simples de priorização de risco.

> Foco: reconhecimento e triagem inteligente (sem exploração ativa).

## Instalação

```bash
cd ntrecon
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Dependências externas (obrigatórias)

A ferramenta invoca utilitários via `subprocess`:

- `subfinder`
- `httpx`
- `gau`
- `nuclei` (opcional com `--no-nuclei`)

Instale-os e garanta que estejam no `PATH`.

## Uso

```bash
python cli.py -d example.com
```

Opções disponíveis:

- `-d, --domain` (obrigatório)
- `-o, --output` diretório de saída
- `--no-nuclei` desabilita scanner nuclei
- `--verbose` logs detalhados
- `--threads` número de threads (default: `10`)

## Exemplo real

```bash
python cli.py -d testphp.vulnweb.com --threads 20
```

Saídas geradas automaticamente:

```text
output/
  testphp.vulnweb.com.json
  testphp.vulnweb.com.md
```

## Screenshot (placeholder)

> Adicione aqui um screenshot real da execução do CLI (ex.: `docs/screenshot-terminal.md`).

## Estrutura do projeto

```text
ntrecon/
├── cli.py
├── config.py
├── requirements.txt
├── README.md
├── core/
│   └── runner.py
├── modules/
│   ├── subdomains.py
│   ├── http_probe.py
│   ├── urls.py
│   └── scanner.py
├── engine/
│   └── scorer.py
├── report/
│   ├── json_export.py
│   └── markdown.py
└── utils/
    └── logger.py
```

## Roadmap

- [ ] Adicionar suporte a fontes OSINT extras
- [ ] Cache local de resultados por domínio
- [ ] Regras customizáveis de scoring (YAML)
- [ ] Exportar para HTML/PDF
- [ ] Modo assíncrono para melhor performance

## Disclaimer ético

ntrecon deve ser utilizado **apenas em ativos autorizados** (programas de bug bounty, laboratórios, ambientes próprios). O uso indevido pode violar leis e políticas de segurança.
