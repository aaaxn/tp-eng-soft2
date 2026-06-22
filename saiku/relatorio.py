# geracao do resumo no terminal e exportacao dos resultados (csv/json/markdown)

import json
from pathlib import Path
from typing import List

import pandas as pd
import typer

FORMATOS = ("csv", "json")


def imprimir_resumo(repo: str, resultado: dict) -> None:
    typer.secho(f"\n Resumo da análise: {repo} ===", bold=True)

    typer.secho("\nIndicadores:", bold=True)
    for nome, valor in resultado["indicadores"].items():
        typer.echo(f"  {nome.replace('_', ' ')}: {valor}")

    typer.secho("\nSinais de manutenção:", bold=True)
    for sinal in resultado["sinais"]:
        typer.secho(f"  ! {sinal}", fg=typer.colors.YELLOW)

    _imprimir_top(
        resultado["issues_antigas"],
        "Issues abertas há mais tempo",
        ["numero", "dias_aberta", "titulo"],
    )
    _imprimir_top(
        resultado["prs_demorados"],
        "PRs mais demorados",
        ["numero", "dias_para_fechar", "titulo"],
    )
    _imprimir_top(
        resultado["arquivos_quentes"],
        "Arquivos mais alterados em correções",
        ["arquivo", "correcoes", "alteracoes"],
    )


def _imprimir_top(
    df: pd.DataFrame, titulo: str, colunas: List[str], n: int = 5
) -> None:
    if df.empty:
        return
    typer.secho(f"\n{titulo} (top {min(n, len(df))}):", bold=True)
    typer.echo(df[colunas].head(n).to_string(index=False, max_colwidth=70))


def exportar(
    saida: Path,
    formato: str,
    issues: List[dict],
    prs: List[dict],
    arquivos: List[dict],
    resultado: dict,
) -> List[Path]:
    # exporta os dados coletados e o resumo da analise no formato escolhido
    saida.mkdir(parents=True, exist_ok=True)
    tabelas = {"issues": issues, "prs": prs, "arquivos_correcoes": arquivos}
    if formato == "csv":
        return _exportar_csv(saida, tabelas, resultado)
    return _exportar_json(saida, tabelas, resultado)


def _exportar_csv(saida: Path, tabelas: dict, resultado: dict) -> List[Path]:
    gerados = []
    for nome, dados in tabelas.items():
        if not dados:
            continue
        caminho = saida / f"{nome}.csv"
        pd.DataFrame(dados).to_csv(caminho, index=False)
        gerados.append(caminho)
    caminho = saida / "resumo.csv"
    pd.DataFrame([resultado["indicadores"]]).to_csv(caminho, index=False)
    gerados.append(caminho)
    return gerados


def _exportar_json(saida: Path, tabelas: dict, resultado: dict) -> List[Path]:
    caminho = saida / "analise.json"
    conteudo = {
        "indicadores": resultado["indicadores"],
        "sinais": resultado["sinais"],
        **tabelas,
    }
    caminho.write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return [caminho]
