# geracao do resumo no terminal e exportacao dos resultados (csv/json/markdown)

import json
from pathlib import Path
from typing import List

import pandas as pd
from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from saiku.analise import Resultado

FORMATOS = ("csv", "json", "md")

NOMES_INDICADORES = {
    "issues_analisadas": "Issues analisadas",
    "issues_abertas": "Issues abertas",
    "issues_abertas_ha_mais_de_90_dias": "Abertas há mais de 90 dias",
    "issues_de_bug": "Issues relacionadas a bugs",
    "proporcao_de_bugs": "Proporção de bugs",
    "taxa_de_resolucao_issues": "Taxa de resolução",
    "media_comentarios_issue": "Média de comentários",
    "mediana_dias_issue_aberta": "Mediana de idade das abertas",
    "prs_analisados": "Pull requests analisados",
    "prs_mesclados": "Pull requests mesclados",
    "mediana_dias_para_fechar_pr": "Mediana para finalizar PR",
    "prs_demorados_mais_de_14_dias": "PRs que levaram mais de 14 dias",
    "prs_abertos_ha_mais_de_14_dias": "PRs abertos há mais de 14 dias",
}

NOMES_COLUNAS = {
    "numero": "#",
    "dias_aberta": "DIAS ABERTA",
    "dias_para_fechar": "DIAS PARA FECHAR",
    "titulo": "TÍTULO",
    "arquivo": "ARQUIVO",
    "correcoes": "CORREÇÕES",
    "alteracoes": "ALTERAÇÕES",
}


def imprimir_resumo(repo: str, resultado: Resultado) -> None:
    console = Console(highlight=False)
    cabecalho = Text()
    cabecalho.append("  RELATÓRIO DE MANUTENÇÃO\n", style="bold bright_white")
    cabecalho.append("  ")
    cabecalho.append(repo, style="bold bright_cyan")
    cabecalho.append("  •  visão geral da saúde do repositório", style="dim white")
    console.print(
        Panel(
            cabecalho,
            box=box.ROUNDED,
            border_style="bright_cyan",
            padding=(1, 1),
        )
    )

    indicadores = Table(
        title="[bold bright_white]INDICADORES[/bold bright_white]",
        box=box.SIMPLE_HEAVY,
        border_style="bright_black",
        header_style="bold bright_cyan",
        row_styles=("", "on #111827"),
        expand=True,
        padding=(0, 1),
    )
    indicadores.add_column("ÁREA", style="bold cyan", no_wrap=True)
    indicadores.add_column("MÉTRICA", ratio=1)
    indicadores.add_column("VALOR", justify="right", style="bold bright_white")
    for nome, valor in resultado.indicadores.items():
        indicadores.add_row(
            _area_indicador(nome),
            NOMES_INDICADORES.get(nome, nome.replace("_", " ").capitalize()),
            _formatar_valor(nome, valor),
        )
    console.print(indicadores)

    sinais = []
    sem_alertas = all("Nenhum sinal forte" in sinal for sinal in resultado.sinais)
    for sinal in resultado.sinais:
        linha = Text()
        linha.append("  ✓  " if sem_alertas else "  !  ", style="bold green" if sem_alertas else "bold yellow")
        linha.append(sinal, style="white")
        sinais.append(linha)
    console.print(
        Panel(
            Group(*sinais),
            title="[bold] SINAIS DE MANUTENÇÃO [/bold]",
            title_align="left",
            box=box.ROUNDED,
            border_style="green" if sem_alertas else "yellow",
            padding=(1, 1),
        )
    )

    _imprimir_top(
        console,
        resultado.issues_antigas,
        "⌛  ISSUES ABERTAS HÁ MAIS TEMPO",
        ["numero", "dias_aberta", "titulo"],
    )
    _imprimir_top(
        console,
        resultado.prs_demorados,
        "◷  PRS MAIS DEMORADOS",
        ["numero", "dias_para_fechar", "titulo"],
    )
    _imprimir_top(
        console,
        resultado.arquivos_quentes,
        "◆  HOTSPOTS DE CORREÇÕES",
        ["arquivo", "correcoes", "alteracoes"],
    )
    console.print("[dim]  Análise concluída • os dados completos estão nos arquivos exportados.[/dim]\n")


def _area_indicador(nome: str) -> str:
    if nome.startswith("prs_") or nome.endswith("_pr"):
        return "Pull requests"
    if nome.startswith("arquivos_"):
        return "Arquivos"
    return "Issues"


def _formatar_valor(nome: str, valor: object) -> str:
    if nome in {"proporcao_de_bugs", "taxa_de_resolucao_issues"}:
        return f"{float(valor) * 100:.0f}%"
    if nome in {"mediana_dias_issue_aberta", "mediana_dias_para_fechar_pr"}:
        return f"{valor:g} dias"
    if nome == "media_comentarios_issue":
        return f"{float(valor):g} comentários"
    return str(valor)


def _imprimir_top(
    console: Console,
    df: pd.DataFrame,
    titulo: str,
    colunas: List[str],
    n: int = 5,
) -> None:
    if df.empty:
        return
    tabela = Table(
        title=f"[bold bright_white]{titulo}[/bold bright_white]  [dim](top {min(n, len(df))})[/dim]",
        box=box.SIMPLE,
        header_style="bold bright_cyan",
        border_style="bright_black",
        show_edge=False,
        expand=True,
        padding=(0, 1),
    )
    for coluna in colunas:
        tabela.add_column(
            NOMES_COLUNAS.get(coluna, coluna.upper()),
            justify="right" if coluna not in {"titulo", "arquivo"} else "left",
            ratio=1 if coluna in {"titulo", "arquivo"} else None,
            no_wrap=coluna not in {"titulo", "arquivo"},
        )
    for linha in df[colunas].head(n).itertuples(index=False, name=None):
        tabela.add_row(*(str(valor) for valor in linha))
    console.print(tabela)


def exportar(
    saida: Path,
    formato: str,
    issues: List[dict],
    prs: List[dict],
    arquivos: List[dict],
    resultado: Resultado,
) -> List[Path]:
    # exporta os dados coletados e o resumo da analise no formato escolhido
    saida.mkdir(parents=True, exist_ok=True)
    tabelas = {"issues": issues, "prs": prs, "arquivos_correcoes": arquivos}
    if formato == "csv":
        return _exportar_csv(saida, tabelas, resultado)
    if formato == "md":
        return _exportar_markdown(saida, resultado)
    return _exportar_json(saida, tabelas, resultado)


def _exportar_csv(saida: Path, tabelas: dict, resultado: Resultado) -> List[Path]:
    gerados = []
    for nome, dados in tabelas.items():
        if not dados:
            continue
        caminho = saida / f"{nome}.csv"
        pd.DataFrame(dados).to_csv(caminho, index=False)
        gerados.append(caminho)
    caminho = saida / "resumo.csv"
    pd.DataFrame([resultado.indicadores]).to_csv(caminho, index=False)
    gerados.append(caminho)
    return gerados


def _exportar_json(saida: Path, tabelas: dict, resultado: Resultado) -> List[Path]:
    caminho = saida / "analise.json"
    conteudo = {
        "indicadores": resultado.indicadores,
        "sinais": resultado.sinais,
        **tabelas,
    }
    caminho.write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return [caminho]


def _exportar_markdown(saida: Path, resultado: Resultado) -> List[Path]:
    linhas = ["# Resumo da analise", "", "## Indicadores", ""]
    for nome, valor in resultado.indicadores.items():
        linhas.append(f"- **{nome.replace('_', ' ')}**: {valor}")
    linhas += ["", "## Sinais de manutencao", ""]
    for sinal in resultado.sinais:
        linhas.append(f"- {sinal}")
    caminho = saida / "analise.md"
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return [caminho]
